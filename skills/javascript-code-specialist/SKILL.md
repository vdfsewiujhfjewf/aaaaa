---
name: javascript-code-specialist
description: Design and implement JavaScript solutions for browser, Node.js, and full-stack workflows with strong readability, testing, and maintainability. Use when requests involve JavaScript/TypeScript coding, refactoring, debugging, API integration, async control flow, frontend behavior, or backend service logic.
---

# JavaScript Code Specialist

## Goal
Deliver robust JavaScript implementations that are clear, testable, and aligned with the target runtime.

## 起動（呼び出し）
- チャットで `$<skill-name>` を明示して依頼する。
- 例: `$javascript-code-specialist` + 実現したい内容。

## Workflow
1. Identify runtime and constraints:
   - Browser vs Node.js vs edge/runtime platform.
   - Module system (ESM/CJS).
   - Allowed dependencies and build tooling.
2. Convert the request into explicit acceptance criteria.
3. Implement with predictable structure:
   - Pure functions first.
   - Side effects isolated near boundaries (I/O, network, DOM).
   - Consistent error handling and input validation.
4. Add or update tests when possible (unit/integration).
5. Summarize tradeoffs and known limitations.

## Coding Rules
- Prefer modern syntax (`const`/`let`, optional chaining, nullish coalescing where useful).
- Avoid hidden mutation unless performance-critical and documented.
- Use JSDoc or types when ambiguity could cause misuse.
- Keep functions focused; split once a function handles multiple concerns.

## Performance and Safety
- Avoid blocking patterns in Node.js hot paths.
- Be explicit about async boundaries and error propagation.
- Sanitize untrusted input before rendering or persistence.
