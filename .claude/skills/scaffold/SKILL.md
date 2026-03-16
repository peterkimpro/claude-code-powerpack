---
name: scaffold
description: Scaffold a new module, feature, or component following existing project patterns. Invoke with a name and brief description.
disable-model-invocation: true
---

Scaffold: $ARGUMENTS

Steps:

1. Read 2-3 existing similar files in the codebase to understand the exact patterns used (naming, exports, imports, file structure).

2. Create the new file(s) following those patterns precisely — do not introduce new conventions.

3. If the project has an index/barrel file or a registry, add the new module there.

4. Create a corresponding test file following the test patterns in the codebase. Add at minimum:
   - One test that verifies the module exists and exports correctly
   - One test for the primary happy path

5. Run the type checker and linter to confirm no errors:
   ```bash
   # adjust commands to match this project's stack
   ```

6. Report what was created and what still needs to be implemented (stub TODOs).
