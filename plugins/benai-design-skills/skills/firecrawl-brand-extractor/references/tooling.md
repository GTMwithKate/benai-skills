# Tooling paths: MCP server vs CLI

The skill's workflow is tool-agnostic: check tooling, extract the brand, sanity-check
the result, deliver it in a usable shape. Only the mechanics of each operation differ.
Exact MCP tool names can vary slightly by server version, so match against your actual
tool list (they follow the pattern `mcp__firecrawl__*`).

## Operation mapping

| Operation | Firecrawl MCP path | Firecrawl CLI path |
| --- | --- | --- |
| Brand extraction | `firecrawl_scrape` with `url` and `formats: ["branding"]` | `firecrawl scrape "<url>" --format branding --pretty -o .firecrawl/brand-<site>.json` |
| Screenshot alongside | `formats: ["branding", "screenshot"]` on the same call | `--format branding,screenshot` |
| Brand plus page copy | `formats: ["branding", "markdown"]` | `--format branding,markdown` |
| Extract with a schema | `firecrawl_extract` with `urls` and your JSON schema (or `firecrawl_scrape` with the `json` format and schema options) | `firecrawl scrape "<url>" --format json` with a schema; run `firecrawl scrape --help` for the schema flags on your installed version |
| Slow-rendering site | pass the wait parameter the tool exposes (commonly `waitFor`, in ms) | `--wait-for 3000` |
| Status / credits | not usually exposed as a tool; assume the server is authenticated and handle credit errors if they surface | `firecrawl --status` |

## Path-specific cautions

**MCP path.** Tool results land directly in the conversation, and the branding payload
carries an inline `images.logo` data URI that can be tens of thousands of characters.
Do not echo the raw payload back to the user. Pull out the fields you need (`colors`,
`typography`, `components`, `spacing`, `confidence`) and drop `images.logo` and the
`__llm_*` debug keys unless you are debugging a wrong result. If the payload is large,
write it to a file first and query it with `jq`, same as the CLI path.

**CLI path.** Authenticates via the `FIRECRAWL_API_KEY` environment variable or stored
config; never hardcode a key. Write output to files with `-o` and read the useful parts
with `jq`, as shown in SKILL.md.

**REST path (fallback).** If the user opts to provide an API key instead of either
tool, call `https://api.firecrawl.dev` directly with the key from an environment
variable. The v2 scrape endpoint takes the same `url` and `formats` shape as the MCP
tools. Only take this path when the user explicitly chooses it.

Everything downstream (the sanity checks in Step 4 and the delivery shapes in Step 5)
is identical on every path: it operates on the returned branding JSON, not on the tool
that fetched it.
