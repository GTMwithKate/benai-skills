---
type: check
layer: 1-universal
status: active
---

# Check: artifacts

The cheap "did the AI actually finish" check. Catch leftover junk that should never ship. These bundle into the mechanical "clean the mechanical stuff" approval. Flag and suggest.

Look for:

- Placeholder text: [brackets], {{curly}}, TODO, TK, lorem ipsum, "INSERT X HERE", "[your name]".
- Model artifacts left in: "as an AI language model," "here is the revised version," "sure, here you go," a meta-comment meant to be deleted.
- Broken structure: malformed markdown, an unclosed list, a heading with nothing under it, a table missing cells.
- Dead or placeholder links: example.com, a bare [link], an obviously broken or templated URL.

For a finding, quote the artifact and give the fix (the real value, or delete it).

## Grading

- Aligned: nothing left over.
- Drift: a stray cosmetic artifact, not embarrassing.
- Misaligned: a placeholder, model artifact, or dead link that would ship visibly.
