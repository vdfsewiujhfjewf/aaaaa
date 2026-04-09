#!/usr/bin/env python3
"""Minimal real-time voice changer (microphone -> speakers)."""

from __future__ import annotations

import argparse
import queue
import sys
from dataclasses import dataclass
from typing import Optional

import numpy as np
import sounddevice as sd
from pedalboard import Compressor, Gain, HighpassFilter, NoiseGate, Pedalboard, PitchShift


@dataclass(frozen=True)
class VoicePreset:
    semitones: float
    highpass_hz: float
    gain_db: float
    description: str


PRESETS: dict[str, VoicePreset] = {
    "custom": VoicePreset(semitones=0.0, highpass_hz=70.0, gain_db=0.0, description="manual settings"),
    # Approximation presets (not AI voice conversion)
    "male_to_female": VoicePreset(
        semitones=4.5,
        highpass_hz=145.0,
        gain_db=1.5,
        description="raise pitch and reduce low frequencies for feminine tone",
    ),
    "female_to_male": VoicePreset(
        semitones=-4.0,
        highpass_hz=70.0,
        gain_db=0.0,
        description="lower pitch for masculine tone",
    ),
}


def build_board(semitones: float, highpass_hz: float, gain_db: float, use_gate: bool) -> Pedalboard:
    effects = [
        PitchShift(semitones=semitones),
        HighpassFilter(cutoff_frequency_hz=highpass_hz),
        Compressor(threshold_db=-18.0, ratio=3.0, attack_ms=5.0, release_ms=80.0),
        Gain(gain_db=gain_db),
    ]
    if use_gate:
        effects.insert(2, NoiseGate(threshold_db=-45.0, ratio=8.0, attack_ms=5.0, release_ms=60.0))
    return Pedalboard(effects)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Real-time voice changer")
    parser.add_argument("--samplerate", type=int, default=48000, help="Audio sample rate")
    parser.add_argument("--blocksize", type=int, default=1024, help="Block size (smaller = lower latency)")
    parser.add_argument("--channels", type=int, default=1, choices=[1, 2], help="Input/output channels")
    parser.add_argument("--semitones", type=float, default=4.0, help="Pitch shift amount in semitones")
    parser.add_argument("--highpass-hz", type=float, default=70.0, help="High-pass filter cutoff in Hz")
    parser.add_argument("--gain-db", type=float, default=0.0, help="Output gain in dB")
    parser.add_argument(
        "--preset",
        default="custom",
        choices=sorted(PRESETS.keys()),
        help="Voice preset (male_to_female / female_to_male / custom)",
    )
    parser.add_argument("--no-gate", action="store_true", help="Disable noise gate")
    parser.add_argument("--input-device", default=None, help="Input device id or name")
    parser.add_argument("--output-device", default=None, help="Output device id or name")
    parser.add_argument("--list-devices", action="store_true", help="Print device list and exit")
    return parser.parse_args()


def resolve_device_arg(value: Optional[str]) -> Optional[int | str]:
    if value is None:
        return None
    value = value.strip()
    if value.isdigit():
        return int(value)
    return value


def main() -> int:
    args = parse_args()

    if args.list_devices:
        print(sd.query_devices())
        return 0

    input_device = resolve_device_arg(args.input_device)
    output_device = resolve_device_arg(args.output_device)

    preset = PRESETS[args.preset]
    semitones = args.semitones
    highpass_hz = args.highpass_hz
    gain_db = args.gain_db

    if args.preset != "custom":
        semitones = preset.semitones
        highpass_hz = preset.highpass_hz
        gain_db = preset.gain_db

    board = build_board(
        semitones=semitones,
        highpass_hz=highpass_hz,
        gain_db=gain_db,
        use_gate=not args.no_gate,
    )

    q: queue.Queue[np.ndarray] = queue.Queue(maxsize=8)

    def callback(indata: np.ndarray, outdata: np.ndarray, frames: int, time, status) -> None:  # type: ignore[override]
        if status:
            print(f"Audio status: {status}", file=sys.stderr)

        # sounddevice gives float32 samples in shape (frames, channels)
        chunk = np.ascontiguousarray(indata.T)  # pedalboard expects (channels, samples)

        try:
            processed = board(chunk, sample_rate=args.samplerate, reset=False)
        except Exception as exc:  # keep stream alive if one block fails
            print(f"Processing error: {exc}", file=sys.stderr)
            processed = chunk

        # ensure output shape (frames, channels)
        out = processed.T
        if out.shape[0] != frames:
            # guard against plugins returning wrong frame counts
            out = np.resize(out, (frames, args.channels))
        outdata[:] = out.astype(np.float32, copy=False)

        # optional level meter payload
        if not q.full():
            q.put_nowait(outdata.copy())

    print("Starting real-time voice changer...")
    print("Press Ctrl+C to stop.")
    print(
        f"sample_rate={args.samplerate}, blocksize={args.blocksize}, channels={args.channels}, "
        f"preset={args.preset}, semitones={semitones:+.1f}, highpass_hz={highpass_hz:.1f}, "
        f"gain_db={gain_db:+.1f}, gate={'off' if args.no_gate else 'on'}"
    )

    with sd.Stream(
        samplerate=args.samplerate,
        blocksize=args.blocksize,
        channels=args.channels,
        dtype="float32",
        device=(input_device, output_device),
        callback=callback,
    ):
        try:
            while True:
                _ = q.get(timeout=0.5)
        except KeyboardInterrupt:
            print("\nStopped.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
