# Real-time Voice Changer (Python minimal template)

マイク入力をリアルタイムで加工して、そのままスピーカーへ出力する最小構成です。

## 1) セットアップ

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

> Linux の場合は PortAudio が必要です（例: `sudo apt install portaudio19-dev`）。

### Windows (PowerShell)

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements.txt
```

> `python3` と `source` は PowerShell では使えません。  
> PowerShell では `py -3` / `python` と `Activate.ps1` を使います。

## 2) デバイス確認

```bash
python voice_changer.py --list-devices
```

> Windows で実行場所が違うと `PathNotFound` になります。  
> 先に `cd` でこの README があるフォルダ（`requirements.txt` がある場所）へ移動してください。

## 3) 実行例

```bash
# 少し高い声（+4 semitones）
python voice_changer.py --semitones 4

# 低い声（-4 semitones）
python voice_changer.py --semitones -4

# 遅延優先（PC性能次第）
python voice_changer.py --blocksize 512

# 入出力デバイス指定（IDでも名前でも可）
python voice_changer.py --input-device 1 --output-device 3
```

## 4) よく使う調整

- `--semitones`: 声の高さを変更
- `--blocksize`: 小さいほど低遅延（ノイズや途切れが出る場合は上げる）
- `--gain-db`: 出力音量を調整
- `--no-gate`: ノイズゲートを無効化

## 5) 仮想マイクとして使う

このテンプレートは「マイク → スピーカー」までです。
Discord / OBS で使いたい場合は、OSの仮想オーディオデバイス
（BlackHole / VB-CABLE / PulseAudio null sink など）へ出力先を変更してください。
