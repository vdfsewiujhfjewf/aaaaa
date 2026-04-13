# Skills 起動ガイド

このリポジトリの3つの特化AI（Skill）は、アプリを起動する形式ではなく、
**チャットでスキル名を明示して呼び出す**ことで使います。

## 使い方（最短）

1. Codex/Chat環境で、このリポジトリを開く
2. 下のようにスキル名を含めて依頼する

- `$skript-code-specialist` で呼び出し
  - 例: 「`$skript-code-specialist` Paper 1.21用に、参加時に初期装備を配るskriptを書いて」
- `$javascript-code-specialist` で呼び出し
  - 例: 「`$javascript-code-specialist` Node.jsで再試行つきfetchラッパーを書いて」
- `$code-repair-specialist` で呼び出し
  - 例: 「`$code-repair-specialist` このTypeErrorの原因を切り分けて最小修正して」

## 補足

- `skript-code-specialist`: Minecraft Skript（`.sk`）の作成・改善向け
- `javascript-code-specialist`: JavaScript/TypeScript実装向け
- `code-repair-specialist`: バグ修正・原因調査向け

## 学習能力について

これらは「会話を跨いで自律学習するAI」ではありません。
継続的に賢くしたい場合は、再利用メモ・テンプレート・テストケースを
リポジトリに保存して引き継いでください。
