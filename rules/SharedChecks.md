# Shared Check Configuration

Summary: Rules and configuration formats for shared file-size exceptions, generated-content exclusions, and folder-child exclusions.

These rules belong to [Implementation](Implementation.md).

## Configure Shared Check Exclusions and Exceptions

When to apply: adding third-party or generated content, adding engine sidecar files, or approving an exception to the 250-line limit.

- MUST configure third-party and generated directories in the project-root `.agent-checks.json` under `exclude` when they would otherwise be checked.
- MUST configure committed third-party directories in the project-root `.folder-child-limit.json` under `third_party`. Configure engine-generated sidecar suffixes under `sidecar_suffixes` when they must not count as folder children.
- An approved exception to the 250-line limit MUST be recorded in `.agent-checks.json` under `line_exceptions`, with the repository-relative file path and a nonempty reason.
- MUST stage the configuration change with the content it governs, because the pre-commit hook reads configuration from the index.
- MUST NOT exclude authored project content merely to make a failed check pass. Fix the violation, or obtain approval for an exception permitted by the owning rule.

### Configuration Format

Both configuration files contain a JSON object. Add the needed keys to an existing file; do not replace unrelated settings.

Use repository-relative paths with `/` separators, such as `vendor/library`, not absolute paths or glob patterns.

In `.agent-checks.json`:
- `exclude` is an array of directory-path strings. Each entry excludes that directory and everything beneath it from source-line and Markdown-link checks.
- `line_exceptions` is an object mapping an exact file path to a nonempty reason string. An entry permits that file to exceed 250 lines; it does not disable Markdown-link checks.

For example, after approval of the line-count exception:

```json
{
  "exclude": ["vendor/library", "generated"],
  "line_exceptions": {
    "scripts/Parser.py": "Approved: splitting the grammar table would separate entries reviewed together."
  }
}
```

In `.folder-child-limit.json`:
- `third_party` is an array of directory-path strings. Each listed directory counts as one child of its parent, but its contents are not counted.
- `sidecar_suffixes` is an array of literal filename-ending strings, including the leading dot. For example, `.meta` excludes files whose names end in `.meta`.

```json
{
  "third_party": ["vendor/library"],
  "sidecar_suffixes": [".meta"]
}
```

Omitted keys use the checker's defaults. These examples show the value shapes; they do not authorize exclusions or exceptions.

The checkers own the accepted formats and matching behavior: `~/.agents/scripts/check_staged_files.py` and `~/.agents/scripts/folder_child_limit.py`.

For example, a committed vendor library is excluded from source checks and identified as third-party content for folder counting. By contrast, a project-owned source file exceeding 250 lines must be split by responsibility or receive an approved line-count exception; it is not third-party content.

Why: automatic checks still need project-specific scope. Recording that scope in configuration prevents agents from repeatedly encountering the same out-of-scope failures or bypassing checks to commit.
