# File Size Limit

Summary: Rules for splitting source-code and documentation files by responsibility when the pre-commit hook rejects their size.

These rules belong to [Implementation](Implementation.md). The [staged-file checker](../scripts/check_staged_files.py), run by the pre-commit hook, owns the numeric limit and counting method.

A file-size rejection is a signal to split responsibilities, not a target to satisfy through compression. Like the [16 child rule](Implementation.md#16-child-rule), this check supports maintenance through meaningful groups. The file-size check does not limit the expanded prompt or token count.

When the pre-commit hook rejects a file for its size:

1. Do not reduce readability by removing comments, collapsing formatting, shortening meaningful names, combining unrelated logic, or writing denser code.
2. Do not omit necessary information merely to pass the check.
3. Identify distinct responsibilities, concepts, sections, or components within the file.
4. Extract those responsibilities into separate, clearly named files.
5. Keep each resulting file cohesive and understandable on its own.
6. Update imports, references, navigation, indexes, or documentation links as needed.

A file may exceed the enforced size limit only when splitting it would create artificial fragmentation, excessive indirection, or reduce maintainability. In that case, explain why the exception is justified before proceeding and record the exception under [Shared Check Configuration](SharedChecks.md#configure-shared-check-exclusions-and-exceptions).

For example, split a rejected file when the file combines saving and UI responsibilities. By contrast, do not split a cohesive file merely because of its line count when the hook accepts its size.

Why: the hook can measure file size, but choosing meaningful responsibility boundaries requires judgment. Keeping numeric enforcement in the checker avoids duplicating details that the hook already enforces.
