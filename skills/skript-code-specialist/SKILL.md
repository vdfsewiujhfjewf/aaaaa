---
name: skript-code-specialist
description: Write, review, and refactor Minecraft Skript plugin code with addon-aware patterns (e.g., SkBee/SkRayFall) and server-safe event logic. Use when requests mention Skript syntax, `.sk` files, Bukkit/Paper event scripting through Skript, command systems, gameplay mechanics, or performance-safe automation for Minecraft servers.
---

# Skript Code Specialist

## Goal
Produce production-ready Skript code that is readable, version-aware, and safe for live Minecraft servers.

## 起動（呼び出し）
- ターミナルでのアプリ起動は不要。チャットで `$<skill-name>` を明示して依頼する。
- 例: `$skript-code-specialist` + 実現したい内容。

## Workflow
1. Confirm environment assumptions before coding:
   - Minecraft server flavor/version (Paper/Spigot/Purpur).
   - Skript version.
   - Installed addons (SkBee, skript-reflect, etc.).
2. Translate user intent into a short feature spec:
   - Trigger sources (event/command/task).
   - Required permissions.
   - Persistent vs temporary data.
3. Generate `.sk` code with clear sectioning:
   - `options` for constants.
   - `command` and `function` blocks for reuse.
   - Avoid unnecessary global variables.
4. Run a static sanity pass:
   - Check indentation-sensitive blocks.
   - Check event names and expression compatibility.
   - Highlight any addon dependency explicitly.
5. Provide minimal test steps for server operators.

## Output Rules
- Default to small, composable functions.
- Prefer descriptive variable names (`{player::coins}` over `{p}` in shared code).
- Mention unsupported assumptions immediately instead of guessing syntax.
- When multiple implementations are possible, give a safe default plus one alternative.

## Reliability Guardrails
- Do not claim runtime validation unless logs were actually checked.
- Flag version-sensitive syntax with a short compatibility note.
- Prefer event-driven logic over high-frequency loops unless needed.
