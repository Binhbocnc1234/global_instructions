# File Size Limit

Summary: Rules for splitting source-code and documentation files by responsibility when they exceed the file-size limit.

These rules belong to [Implementation](Implementation.md).

Keep source-code and documentation files at or below 18,000 characters whenever practical. Count Unicode code points, including whitespace and newline characters, not UTF-8 bytes. A file containing exactly 18,000 characters meets the limit; a file containing 18,001 exceeds it.

The character limit is a signal to split responsibilities, not a target to satisfy through compression. Like the [16 child rule](Implementation.md#16-child-rule), it supports maintenance through meaningful groups. It does not limit the expanded prompt or token count.

When a file is likely to exceed the character limit:

1. Do not reduce readability by removing comments, collapsing formatting, shortening meaningful names, combining unrelated logic, or writing denser code.
2. Do not omit necessary information merely to stay below the limit.
3. Identify distinct responsibilities, concepts, sections, or components within the file.
4. Extract those responsibilities into separate, clearly named files.
5. Keep each resulting file cohesive and understandable on its own.
6. Update imports, references, navigation, indexes, or documentation links as needed.

A file may exceed the character limit only when splitting it would create artificial fragmentation, excessive indirection, or reduce maintainability. In that case, explain why the exception is justified before proceeding and record the exception under [Shared Check Configuration](SharedChecks.md#configure-shared-check-exclusions-and-exceptions).

For example, split a file above the limit when the file combines saving and UI responsibilities. By contrast, a file with more than 250 lines but fewer than 18,000 characters does not need splitting merely because of its line count.

Why: physical line counts depend on language and formatting; a character limit gives source code and documentation the same text-size budget while keeping meaningful responsibilities as the reason to split.
