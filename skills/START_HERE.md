# Skills 起動ガイド

このリポジトリの3つの特化AI（Skill）は、アプリを起動する形式ではなく、
**チャットでスキル名を明示して呼び出す**ことで使います。

## まず結論（質問への回答）

- **「ターミナルで起動すればいいの？」**  
  スキル自体はターミナル起動不要です（チャットで呼び出し）。
- **「別アプリで開きたい」**  
  そのための **ダウンロード専用Web** を追加しました。必要なZIPをブラウザから落として別アプリに渡せます。

## ダウンロード専用Webの使い方

1. ターミナルで起動:

```bash
python3 skills/download-web/app.py
```

2. ブラウザで開く:

- `http://127.0.0.1:8787`

3. 欲しいZIPを選んでダウンロード:

- 全部まとめて: `all.zip`
- 個別: `skript-code-specialist.zip` / `javascript-code-specialist.zip` / `code-repair-specialist.zip`

## チャットでの呼び出し（通常利用）

- `$skript-code-specialist` で呼び出し
  - 例: 「`$skript-code-specialist` Paper 1.21用に、参加時に初期装備を配るskriptを書いて」
- `$javascript-code-specialist` で呼び出し
  - 例: 「`$javascript-code-specialist` Node.jsで再試行つきfetchラッパーを書いて」
- `$code-repair-specialist` で呼び出し
  - 例: 「`$code-repair-specialist` このTypeErrorの原因を切り分けて最小修正して」

## 学習能力について

これらは「会話を跨いで自律学習するAI」ではありません。
継続的に賢くしたい場合は、再利用メモ・テンプレート・テストケースを
リポジトリに保存して引き継いでください。
