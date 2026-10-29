# File Size Limit

Summary: Rules for splitting source-code and documentation files by responsibility when they exceed the file-size limit.

These rules belong to [Implementation](Implementation.md).

Keep source-code and documentation files at or below 250 lines whenever practical.

The 250-line limit is a signal to split responsibilities, not a target to satisfy through compression.
Like the [16 child rule](Implementation.md#16-child-rule), it supports maintenance through meaningful groups. It does not limit the expanded prompt or token count.

When a file is likely to exceed 250 lines:

1. Do not reduce readability by removing comments, collapsing formatting, shortening meaningful names, combining unrelated logic, or writing denser code.
2. Do not omit necessary information merely to stay below the limit.
3. Identify distinct responsibilities, concepts, sections, or components within the file.
4. Extract those responsibilities into separate, clearly named files.
5. Keep each resulting file cohesive and understandable on its own.
6. Update imports, references, navigation, indexes, or documentation links as needed.

A file may exceed 250 lines only when splitting it would create artificial fragmentation, excessive indirection, or reduce maintainability. In that case, explain why the exception is justified before proceeding.
