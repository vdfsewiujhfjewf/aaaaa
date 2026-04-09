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

### Windows (ダブルクリック起動)

`start.bat` を実行すると、以下を自動で行います。

- `.venv` 作成（初回のみ）
- 依存パッケージのインストール
- `start_config.bat` を読み込んで `voice_changer.py` を起動

設定は `start_config.bat` をメモ帳で開いて変更できます（いつでも変更可）。

男性→女性にしたい場合は、`start_config.bat` の `PRESET=male_to_female` にして `start.bat` を実行してください。

### Web 画面で設定して起動（新機能）

`start_web.bat` を実行すると Web UI が起動します。  
ブラウザで `http://127.0.0.1:5000` を開くと、以下を画面から変更できます。

- preset
- semitones
- highpass
- blocksize / channels / gain
- input / output device
- no gate

保存後に **Start** ボタンで起動、**Stop** ボタンで停止します。

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

# 男性→女性（プリセット）
python voice_changer.py --preset male_to_female

# 女性→男性（プリセット）
python voice_changer.py --preset female_to_male
```

## 4) よく使う調整

- `--semitones`: 声の高さを変更
- `--preset`: `male_to_female` / `female_to_male` / `custom`
- `--blocksize`: 小さいほど低遅延（ノイズや途切れが出る場合は上げる）
- `--gain-db`: 出力音量を調整
- `--no-gate`: ノイズゲートを無効化

`start_config.bat` の主な項目:

- `PRESET`（`male_to_female` / `female_to_male` / `custom`）
- `SEMITONES`（例: 4 / -4）
- `HIGHPASS_HZ`（例: 70 / 145）
- `BLOCKSIZE`（例: 512 / 1024）
- `CHANNELS`（通常 1）
- `GAIN_DB`（出力ゲイン）
- `INPUT_DEVICE` / `OUTPUT_DEVICE`（空なら既定デバイス）
- `EXTRA_ARGS`（例: `--no-gate`）

> `male_to_female` は「ピッチ上げ + 低域カット」による簡易変換です（AIの声質変換ではありません）。

## 5) 仮想マイクとして使う

このテンプレートは「マイク → スピーカー」までです。
Discord / OBS で使いたい場合は、OSの仮想オーディオデバイス
（BlackHole / VB-CABLE / PulseAudio null sink など）へ出力先を変更してください。

## 6) Web UI スクリプト

- `web_voice_control.py`: 設定保存 (`web_settings.json`) と Start/Stop を提供するローカルWebサーバ
- `start_web.bat`: Windows用のWeb UI 起動スクリプト
