---
name: firecrawl-brand-extractor
description: |
  Extract a website's complete brand system (logo, color palette, typography, spacing scale, button/component
  styles, brand personality) using Firecrawl's `branding` scrape format, via a connected Firecrawl MCP server or
  the Firecrawl CLI. Use this skill whenever the user wants to pull brand colors, a color palette, hex codes,
  fonts, a type scale, design tokens, a style guide, a brand kit, or a design system out of a live website.
  Triggers include "get the brand colors from", "extract the design system from", "what fonts does X use",
  "build a brand kit from this site", "clone this site's style", "pull the palette from", "reverse engineer this
  brand", "match our design to X", or any request to turn a URL into design tokens or CSS variables. Also
  handles first-time setup: installing the Firecrawl CLI, creating an account, obtaining the API key, and
  storing it locally. Do NOT use for scraping page text or articles (use a plain scrape) or for local design
  file work.
---

# Firecrawl Brand Extractor

Turn any URL into a structured brand system in one command. Firecrawl's `branding`
scrape format returns the logo, palette, fonts, type scale, spacing, and component
styles as clean JSON that maps straight onto CSS variables or design tokens.

```bash
firecrawl scrape "https://stripe.com" --format branding --pretty -o .firecrawl/brand-stripe.json
```

Costs 1 credit per page. No extra surcharge for the branding format.

## Step 1: Check your tooling

Firecrawl is reachable more than one way. Detect what this environment has before
running anything, in this order:

1. **Firecrawl MCP server connected.** Tools named like `mcp__firecrawl__*` (for
   example `firecrawl_scrape`) appear in your available tools. Use the MCP tools and
   skip Step 2; the server carries its own authentication.
2. **Firecrawl CLI installed.** `which firecrawl` or `firecrawl --version` succeeds.
   Use the CLI. It authenticates via the `FIRECRAWL_API_KEY` environment variable or
   its stored config. Continue to Step 2.
3. **Neither.** Stop and tell the user their options: install the CLI (see
   [references/setup.md](references/setup.md)), connect the Firecrawl MCP server, or
   provide an API key so you can call the REST API at `https://api.firecrawl.dev`
   directly. Ask which they want. Never fail silently and never guess.

The command examples in this skill are written in CLI syntax for concreteness. On the
MCP path, the workflow, sanity checks, and delivery guidance are identical; translate
each command using the operation mapping in
[references/tooling.md](references/tooling.md).

## Step 2: CLI path only - check setup before anything else

MCP path: skip this step. On the CLI path, always run this first and do not attempt
an extraction until it passes.

```bash
firecrawl --status
```

A healthy result looks like this:

```
  🔥 firecrawl cli v1.15.2

  ● Authenticated via FIRECRAWL_API_KEY
  Concurrency: 0/100 jobs (parallel scrape limit)
  Credits: 500,000 remaining
```

| What you see | What to do |
| --- | --- |
| Version, `Authenticated`, and credits remaining | Setup is good. Go to Step 3. |
| `command not found: firecrawl` | Not installed. Go to [references/setup.md](references/setup.md). |
| Version prints but not authenticated, or `401` / `Unauthorized` | No API key yet. Go to [references/setup.md](references/setup.md). |
| `Credits: 0` | Out of credits. The user needs to top up at firecrawl.dev/pricing. Stop and tell them. |

[references/setup.md](references/setup.md) covers the whole first-run path: installing
the CLI, creating a Firecrawl account, getting the API key, and saving it locally so
every future run just works.

## Step 3: Extract the brand

Write output to a file rather than dumping it into the conversation. The branding
payload is large and includes an inline logo that can be tens of thousands of
characters.

```bash
mkdir -p .firecrawl
firecrawl scrape "<url>" --format branding --pretty -o .firecrawl/brand-<site>.json
```

Then read the useful parts with `jq` instead of reading the whole file:

```bash
# The palette
jq '.branding.colors' .firecrawl/brand-<site>.json

# Fonts and type scale
jq '.branding.typography' .firecrawl/brand-<site>.json

# Buttons, radius, shadows
jq '.branding.components, .branding.spacing' .firecrawl/brand-<site>.json

# Everything except the bulky logo data and debug keys
jq '.branding | del(.images.logo, .__llm_logo_reasoning, .__llm_button_reasoning, .__llm_metadata)' .firecrawl/brand-<site>.json

# How much to trust the result
jq '.branding.confidence' .firecrawl/brand-<site>.json
```

Always scrape the **homepage** unless the user names a specific page. Homepages carry
the primary CTA button and the full nav, which is where the palette and component
styles are cleanest. A blog post or docs page often yields a washed-out subset.

For the full field reference with real example output, see
[references/branding-format.md](references/branding-format.md).

## Step 4: Sanity-check before you hand it over

The branding format uses heuristics plus an LLM pass, so it is very good but not
infallible. Check these three things every time, and say plainly what you verified.

1. **Read `confidence`.** It returns `buttons`, `colors`, and `overall` scores. Below
   about 0.8 on colors, treat the palette as a draft and verify visually.
2. **Watch for a mislabeled `textPrimary`.** On real runs this field sometimes returns
   the accent or link color rather than the body text color. If `textPrimary` equals
   `accent` or `link`, and especially if it is a saturated brand color rather than a
   near-black or near-white, flag it as suspect.
3. **Distrust an odd `fontSizes.body`.** The extractor can latch onto an oversized hero
   paragraph. A `body` size at or above 24px usually means it sampled the wrong element.

When any check fails, grab a screenshot in the same run and compare against it:

```bash
firecrawl scrape "<url>" --format branding,screenshot --pretty -o .firecrawl/brand-<site>.json
```

Multiple formats always return JSON, so the screenshot arrives as a URL inside the
payload rather than as an image file.

## Step 5: Deliver it in a usable shape

Ask what the output is for, or infer it from the request. Do not just paste raw JSON at
the user.

| They want | Give them |
| --- | --- |
| "the brand colors" | A short table of hex values with role labels, plus a note on anything low-confidence |
| A design system or brand kit | CSS custom properties or a tokens file. See [references/design-tokens.md](references/design-tokens.md) |
| To match or clone a site's look | Tokens plus the component specs (radius, shadow, button fills) |
| A competitor comparison | One extraction per site, then a side-by-side table. See [references/design-tokens.md](references/design-tokens.md) |

## Common variations

**Several sites at once.** Scrapes run concurrently up to the limit shown by
`firecrawl --status`:

```bash
firecrawl scrape "https://a.com" --format branding -o .firecrawl/brand-a.json &
firecrawl scrape "https://b.com" --format branding -o .firecrawl/brand-b.json &
firecrawl scrape "https://c.com" --format branding -o .firecrawl/brand-c.json &
wait
```

**A JS-heavy or slow-rendering site.** Give it time to paint before sampling styles:

```bash
firecrawl scrape "<url>" --format branding --wait-for 3000 -o .firecrawl/brand.json
```

**Brand plus page copy together.** Useful when the user also wants the voice and
messaging, not just the visuals:

```bash
firecrawl scrape "<url>" --format branding,markdown --pretty -o .firecrawl/brand-full.json
```

**A site behind a cookie wall or region gate.** Try a country code first:

```bash
firecrawl scrape "<url>" --format branding --country US -o .firecrawl/brand.json
```

## Notes and limits

- The logo in `images.logo` is often a `data:image/svg+xml` URI containing the entire
  inline SVG rather than a hosted URL. It is usable directly in an `<img src>` or
  CSS `url()`. Never print it into the conversation. To save it as a file, decode it
  rather than echoing it.
- `images.favicon` and `images.ogImage` are normal URLs and are the safer bet when you
  need a raster asset.
- `designSystem.framework` returns `custom` for most hand-built sites. It is a weak
  signal, not a real framework detection.
- `personality` (tone, energy, target audience) is an LLM inference about the brand. It
  is helpful as a starting point for voice work and should not be presented as fact.
- Keys prefixed `__llm_` are debug output explaining why a given logo or button was
  chosen. Useful when a result looks wrong, otherwise strip them.
- Always quote URLs. The shell treats `?` and `&` as special characters.
- Add `.firecrawl/` to `.gitignore`.

## Other formats on the same command

`--format` accepts: `markdown`, `html`, `rawHtml`, `links`, `images`, `screenshot`,
`summary`, `changeTracking`, `json`, `attributes`, `branding`. A single format returns
raw content; two or more return JSON. Run `firecrawl scrape --help` for the full option
list, and `firecrawl --help` for other commands (`search`, `map`, `crawl`, `agent`,
`interact`).

## References

- [references/tooling.md](references/tooling.md) - MCP vs CLI: the same operations on both paths
- [references/setup.md](references/setup.md) - install the CLI, create the account, get and store the API key
- [references/branding-format.md](references/branding-format.md) - every field, with real example output
- [references/design-tokens.md](references/design-tokens.md) - convert to CSS variables and tokens, run competitor sweeps
