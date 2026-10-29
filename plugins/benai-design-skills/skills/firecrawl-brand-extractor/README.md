# firecrawl-brand-extractor

An agent skill that extracts a website's brand system (logo, color palette, typography,
spacing scale, button and component styles) using the Firecrawl CLI's `branding` scrape
format. Handles first-run setup too: installing the CLI, creating a Firecrawl account,
getting the API key, and storing it locally.

Point your coding agent at a URL and get back usable design tokens.

## Install

Drop the folder into your agent's skills directory.

**Claude Code**

```bash
# Just you, every project
cp -r firecrawl-brand-extractor ~/.claude/skills/

# Or one project only
cp -r firecrawl-brand-extractor .claude/skills/
```

**Cursor**

```bash
cp -r firecrawl-brand-extractor ~/.cursor/skills/
```

Other agents that read `SKILL.md` folders work the same way; check where yours looks for
skills. Restart the agent afterwards so it picks up the new skill.

## Use it

Just ask in plain language. The skill triggers on requests like:

- "Get me the brand colors from stripe.com"
- "Extract the design system from linear.app"
- "What fonts does this site use?"
- "Build a brand kit from https://example.com"
- "Compare our palette against these three competitors"
- "Turn this site's styling into CSS variables"

On the first run the agent will check whether the Firecrawl CLI is installed and
authenticated, and walk you through setup if it is not. You will need a Firecrawl
account; the free tier is enough, since a brand extraction costs 1 credit per page.

## What comes back

```bash
firecrawl scrape "https://stripe.com" --format branding --pretty -o brand.json
```

```json
{
  "colorScheme": "light",
  "colors": {
    "primary": "#061B31", "secondary": "#FFE0D1", "accent": "#533AFD",
    "background": "#FFFFFF", "link": "#533AFD"
  },
  "typography": {
    "fontFamilies": { "primary": "Sohne", "heading": "SF Pro Display" },
    "fontSizes": { "h1": "48px", "h2": "32px" }
  },
  "spacing": { "baseUnit": 8, "borderRadius": "0px" },
  "components": {
    "buttonPrimary": {
      "background": "#533AFD", "textColor": "#FFFFFF",
      "borderRadius": "4px", "shadow": "none"
    }
  },
  "images": { "logo": "data:image/svg+xml;...", "favicon": "https://..." },
  "personality": { "tone": "professional", "energy": "medium" },
  "confidence": { "buttons": 0.95, "colors": 0.9, "overall": 0.925 }
}
```

The agent turns that into a hex table, CSS custom properties, a design-tokens file, or a
competitor comparison, depending on what you asked for.

## Contents

| File | What is in it |
| --- | --- |
| `SKILL.md` | Main workflow: tooling check, setup gate, extraction, verification, delivery |
| `references/tooling.md` | MCP server vs CLI: the same operations on both paths |
| `references/setup.md` | CLI install, account creation, API key, troubleshooting table |
| `references/branding-format.md` | Every returned field, documented from real runs |
| `references/design-tokens.md` | CSS variables, W3C tokens, Tailwind, competitor sweeps |

## Worth knowing

The branding format is very good but heuristic in places, and the skill tells the agent
to verify rather than trust blindly:

- `confidence` scores come with every response. Under about 0.8 on colors means check it.
- `textPrimary` sometimes returns the accent color rather than the body text color.
- `fontSizes.body` can latch onto an oversized hero paragraph.
- Button specs are read off real computed styles, so they are the most reliable part of
  the payload, and `buttonPrimary.background` is often a better read on the true brand
  color than `colors.primary`.

Works with either a connected Firecrawl MCP server or the Firecrawl CLI; the skill
detects which is available. The CLI path requires Node.js and `jq` (for parsing).
Built against firecrawl-cli 1.15.2; `--format branding` needs 1.15.x or newer.
