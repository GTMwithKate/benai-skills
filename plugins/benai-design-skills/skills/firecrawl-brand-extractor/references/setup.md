# Setup: CLI, Account, and API Key

Everything needed to get from a machine with nothing installed to a working
`firecrawl scrape --format branding` run. Work through it in order and stop as soon as
`firecrawl --status` reports an authenticated client with credits.

## The fast path

One command installs the CLI globally, opens the browser to sign in or create an
account, stores the credentials, and installs the Firecrawl skills:

```bash
npx -y firecrawl-cli@latest init --browser
```

The `--browser` flag is the right choice when an agent is driving, because it avoids an
interactive prompt the agent cannot answer. The user completes sign-in in their browser
and the CLI captures the key on its own.

This is safe to re-run at any time. Use it when the CLI is missing, stale, or only
half-configured.

Verify:

```bash
firecrawl --status
```

If that shows a version, `Authenticated`, and a credit balance, setup is done. Skip to
the smoke test at the bottom.

## Step 1: Install the CLI

Skip if `firecrawl --version` already prints a version.

```bash
npm install -g firecrawl-cli
```

Requires Node.js. If `npm` is missing, install Node from nodejs.org or via a version
manager (`nvm`, `fnm`, `volta`) before continuing.

Update an existing install:

```bash
npm update -g firecrawl-cli
```

### If `firecrawl: command not found` after installing

1. Confirm npm's global bin directory is on `PATH`: `npm bin -g`
2. Fall back to invoking through npx: `npx firecrawl-cli@latest --status`
3. If npx works and the global binary does not, add the npm global bin to `PATH` in
   `~/.zshrc` or `~/.bashrc`, then open a new shell.

Every command in this skill works with `npx firecrawl-cli@latest` in place of
`firecrawl` if the global binary cannot be fixed.

## Step 2: Create the account and get the API key

Two routes. Prefer the browser route.

### Route A: Browser sign-in (recommended)

```bash
firecrawl config -b
```

This opens firecrawl.dev in the default browser. The user signs in, or creates a free
account if they do not have one, and authorizes the CLI. The key is written to the
CLI's own credential store. Nobody has to copy or paste a key, and the key never
appears in the chat transcript.

Free accounts include a starter credit allowance, which is plenty for brand
extractions at 1 credit per page.

### Route B: Paste an existing key manually

Use this when the user already has a key, or when no browser is available (a remote
server, a container, CI).

Where the key lives: firecrawl.dev → sign in → **API Keys** in the dashboard. Keys
begin with `fc-`.

**Have the user run this command themselves.** Do not ask them to paste the key into
the conversation, and do not type it on their behalf. Keys pasted into a chat end up
in the transcript and in any logs downstream.

```bash
firecrawl config --api-key "fc-YOUR-KEY-HERE"
```

Alternatively they can export it as an environment variable, which the CLI reads
automatically:

```bash
export FIRECRAWL_API_KEY="fc-YOUR-KEY-HERE"
```

To make that permanent, they should append the same line to `~/.zshrc` or
`~/.bashrc`.

## Step 3: Store the key locally for a project

`firecrawl config` already persists credentials for CLI use, so this step is only
needed when project code (a script, an app, a notebook) also has to read the key.

```bash
firecrawl env
```

This pulls the stored `FIRECRAWL_API_KEY` into `.env` in the current directory. Useful
options:

```bash
firecrawl env --file .env.local   # write somewhere else
firecrawl env --overwrite         # replace an existing FIRECRAWL_API_KEY entry
```

Then make sure the file is never committed:

```bash
grep -qxF '.env' .gitignore || echo '.env' >> .gitignore
grep -qxF '.firecrawl/' .gitignore || echo '.firecrawl/' >> .gitignore
```

If the key ever does get committed or shared, rotate it in the Firecrawl dashboard.
Revoking and reissuing takes seconds.

Self-hosted Firecrawl deployments also need a base URL:

```bash
firecrawl config --api-url "https://firecrawl.your-domain.com"
```

Or as `FIRECRAWL_API_URL` in the environment or `.env`.

## Step 4: Smoke test

Prove that install, auth, and the branding format all work together with one real
request against a site with a distinctive brand:

```bash
mkdir -p .firecrawl
firecrawl scrape "https://stripe.com" --format branding --pretty -o .firecrawl/setup-check.json
jq '.branding.colors, .branding.confidence' .firecrawl/setup-check.json
```

A working setup returns a palette of hex values and a confidence block. That confirms
the CLI is installed, the key is valid, credits are available, and the branding format
is reachable on the account.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `command not found: firecrawl` | Not installed, or npm global bin missing from `PATH`. See Step 1. |
| `401` / `Unauthorized` / `Invalid API key` | No key, or a revoked one. Re-run `firecrawl config -b`. |
| `Credits: 0` or a payment-required error | Out of credits. Top up at firecrawl.dev/pricing. Nothing in the skill can work around this. |
| Browser login never completes | Fall back to Route B with a key from the dashboard. |
| `--format branding` rejected as an unknown format | CLI is too old. Run `npm update -g firecrawl-cli`, then confirm `firecrawl --version` is at least 1.15.x. |
| Empty or near-empty `branding` object | The page likely blocked the render. Retry with `--wait-for 3000`, and if it still fails, try `--country US`. |
| Works in one shell, fails in another | The key was exported for one session only. Persist it via `firecrawl config` or a shell rc file. |

## Once setup passes

Return to [SKILL.md](../SKILL.md) and run the extraction from Step 2.
