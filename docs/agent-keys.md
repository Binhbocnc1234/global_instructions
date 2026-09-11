# agent-keys — API key storage

Stores every API key an agent or a skill reads. Values live encrypted in the GNOME login keyring, which the lock-screen password unlocks at login, so there is no second prompt and no key sits in a readable file.

Set up on Ubuntu 24.04, 2026-09-11.

## Commands

| Command | Does | Prints the value? |
|---|---|---|
| `agent-keys set NAME` | Prompts once and stores the key | no |
| `agent-keys list` | Says which recorded keys are present in the keyring | no |
| `agent-keys export` | Prints `export NAME=value` lines for `eval` | yes, to stdout |
| `agent-keys rm NAME` | Deletes the key and drops it from the name list | no |

`set` shows the expected shape of the value before reading it, so a wrong paste is visible before it is stored. Input is hidden and never reaches shell history. An empty value is refused.

## Where each part lives

| Path | Holds | Secret? |
|---|---|---|
| `~/.local/bin/agent-keys` | the script | no |
| `~/.config/agent-keys.list` | key **names**, one per line | no |
| `~/.local/share/keyrings/login.keyring` | the **values**, encrypted | yes |

The name list exists so `list` and `export` know what to ask the keyring for. The keyring API has no useful "enumerate by attribute" for this purpose, so the names are tracked beside it.

## Keyring schema

Each key is stored as one libsecret item with two lookup attributes:

| Attribute | Value |
|---|---|
| `service` | `agent-api-key` — fixed, identifies items this tool owns |
| `name` | the environment variable name, e.g. `EXA_API_KEY` |

The label is set to the same name, so the item is readable in Seahorse (`seahorse`, "Passwords" → "Login").

Reading one directly, without the script:

```bash
secret-tool lookup service agent-api-key name EXA_API_KEY
```

**`service` must stay `agent-api-key`.** Changing it orphans every stored key — they remain in the keyring but nothing looks them up.

## How a shell gets the keys

`~/.bashrc` ends with:

```bash
command -v agent-keys >/dev/null && eval "$(agent-keys export 2>/dev/null)"
```

`export` pings the Secret Service on D-Bus first. Without an unlocked keyring it prints nothing and exits 0, so the shell starts clean rather than erroring.

## The limit

**A session with no desktop login has no unlocked keyring**, so the keys are absent there: an SSH session, a systemd service, a cron job, a container. This follows from tying the keys to the lock-screen password and cannot be engineered away — a process that runs without the password cannot decrypt what that password protects.

Where a background job genuinely needs a key, pass it in through that job's own configuration rather than expecting the shell to supply it.

## Adding a key

```bash
agent-keys set EXA_API_KEY
source ~/.bashrc
agent-keys list
```

To teach `set` the shape of a new provider's key, add a case to `hint_for()` in the script. A key with no case falls back to a generic hint and still stores correctly.

## Rules

- Binhbocnc types the values. **An agent MUST NOT type, paste, echo, or otherwise handle a key value.** An agent MAY install the tool, add a `hint_for()` case, and wire up the sourcing.
- To check a key is set, test that the variable is non-empty or run `agent-keys list`. **MUST NOT print a value**, and MUST NOT run `agent-keys export` where its output is logged.
- Neither the script nor the name list holds a secret, so both are safe to commit. The keyring is not, and lives outside every repository.
