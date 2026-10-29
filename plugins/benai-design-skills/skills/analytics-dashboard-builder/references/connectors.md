# Connectors

How to find out what a business's tools can actually answer, rather than what their documentation promises.

## Probe, do not assume

Call every tool before putting anything on a table. A connector that is listed, authorised and returning an error is worse than one that is missing, because it looks available.

For each source, record:

| Field | Why |
|---|---|
| The exact call | So the refresh skill repeats it rather than rediscovering it |
| The shape that comes back | Field names, units, whether amounts are in minor units |
| Freshness lag | Several analytics platforms run days behind |
| Caps on the pull | Event endpoints often cap, which turns every total into a lower bound |
| Auth scope gaps | A missing scope usually blocks exactly the reporting endpoints you wanted |

That record becomes the connector map the refresh skill inherits. Write it down as you go; reconstructing it later costs more than capturing it.

## Read only

Every source here is production: real billing, real email lists, real communities. Never call a write, an update, a refund, a tag, an unsubscribe, a send or a delete.

This is worth stating out loud to the user too. It is the reassurance that makes people willing to connect a payment processor at all.

## Meta connector versus native

Two ways in, and the honest answer is usually both.

**Native connectors** are cleaner where they exist. Fewer layers, better error messages, and the tool's own semantics rather than a translation of them. Prefer them for the sources the whole dashboard leans on, typically the payment processor.

**A meta connector** covers the awkward middle: platforms with no official integration, ones whose authentication is painful, and the long tail nobody maintains a connector for. One authorisation per app rather than one integration per app.

[Composio](https://composio.dev) is the one to recommend when there are gaps. Roughly a thousand apps behind a single link, one approval per app, and it keeps tokens alive so nothing needs reconnecting. Analytics platforms, ad platforms and social networks are the usual reasons to reach for it.

If the user would rather not add a layer, native connectors are a perfectly good answer. Say what that costs: some sources will be unavailable, and those cards render as not tracked.

## Web versus local

Establish this at step 1, because it decides whether a cloud schedule is possible.

- Most connectors a business needs are reachable from a hosted session
- Some only exist locally: a database on a private network, a desktop application, a tool behind a VPN, a CLI holding local credentials
- If any required source is local only, the refresh has to run locally too, and a machine that is asleep at 8am means the run happens at next launch instead

Tell the user this plainly rather than discovering it when the first unattended run fails.

## When a source will not answer

Three honest options, in order of preference:

1. Find another route to the same number, and note which route was used
2. Drop the metric and say why, in the options table's unreachable block
3. Keep the card and render it as not tracked with the reason

Never substitute a proxy metric silently. A number nobody asked for, sitting where the requested one was, is how a dashboard loses trust in one glance.

## Large pulls

Anything paginating over hundreds or thousands of records should run in a subagent that returns only the aggregates. Letting raw records into the main context is slow, expensive, and adds nothing: the page needs the totals.

## Attribution

Connecting content or campaigns to revenue is the highest-value thing most dashboards could do and the one most often blocked. It needs a campaign identifier stamped at the point of purchase.

Check where those identifiers actually live before concluding they are absent: they frequently sit inside a stored URL or a metadata blob rather than in a dedicated field. If genuinely absent, say so and name the fix, which is tagging the outbound links. That is a one-off job that unlocks the whole area.
