# csharp-lsp-auto

C# code intelligence for Claude Code, pinned to the solution in the workspace root.

## Why this exists instead of the official `csharp-lsp`

The official plugin runs `csharp-ls` with no arguments. `csharp-ls` then searches for a
solution **recursively**. In a Unity project that search reaches into `Library/`, where it
finds decoy solutions:

    Library\PackageCache\com.unity.services.cloudcode@.../Template~/Solution.sln
    Library\VP\mppm3e2eda3e\mppm3e2eda3e.slnx      <- Multiplayer Play Mode clone
    ChessUnity.slnx                                <- the real one

Measured on ChessUnity: `csharp-ls` chose the Multiplayer Play Mode clone. The server starts
and looks healthy while answering from the wrong workspace.

## How it works

`csharp-ls-auto.cmd` looks for a solution in the workspace root only:

- exactly one `*.slnx` -> `csharp-ls -s <that>`
- otherwise exactly one `*.sln` -> `csharp-ls -s <that>`
- otherwise -> plain `csharp-ls`, unchanged behavior

`Library/` can never win, because subdirectories are not searched. Projects without a root
solution behave exactly as they do with the official plugin.

## Requirements

- `csharp-ls` (`dotnet tool install --global csharp-ls`), .NET SDK 6.0+
- `csharp-ls-auto.cmd` in `%USERPROFILE%\.dotnet\tools` (already on PATH)

## Measured on ChessUnity (128-project Unity solution)

    workspace load     ~40s cold, ~10s warm, once per session
    hover              bool BoardUtils.IsGameOver()
    documentSymbol     96 symbols
    references         3 (correctly excluding nameof(GameState.IsGameOver))
    diagnostics        delivered

## Note on `command: "cmd"`

The server is launched as `cmd /c csharp-ls-auto.cmd` rather than naming the `.cmd`
directly, because Node refuses to spawn `.cmd` files without a shell.
