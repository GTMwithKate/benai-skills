# Template Catalog

Six visual structures. Each pairs a shape (what it looks like) with a communicative purpose (what the viewer takes away). Pick by the message, not by aesthetics. All color and type values come from the token map resolved in Step 1 of SKILL.md.

## 1. Stacked List

**Visual:** Vertical cards stacked top-to-bottom, connected by downward arrows. One item per row. Optionally numbered, optionally bottom-to-top for level progressions.

**Communicates:** Sequential importance, ordered reasoning, "here are N reasons." The vertical stack implies a single-track argument the viewer follows linearly.

**When to use:**
- Listing advantages or reasons ("Why you need X")
- Ordered best practices ("Step 1, 2, 3...")
- Level progressions ("Level 1 through Level 7", stacked bottom-to-top with upward arrows)

**Structure:** Title, then for each item: shadow rectangle + content card + label, arrow down, repeat. Cards share identical width, height, and x position. Rotate card fills through `--accent-1..N` in order.

**Layout guidance:** Cards ~400-500px wide, ~80px tall, uniform vertical gap. 3-5 items is the sweet spot; 6-7 needs a taller canvas and tighter cards. Each item can carry a short title plus a one-line description separated by a divider.

---

## 2. Grid Columns

**Visual:** 2-3 vertical columns side by side, each with its own flow or list. Parallel structure across columns.

**Communicates:** "The same pattern repeats across different contexts." Not contrast; repetition. The viewer sees identical logic applied in multiple domains.

**When to use:**
- Same concept applied to different audiences ("Individual vs Company use cases")
- Parallel workflows ("three deployment paths that follow the same shape")
- Multiple proof tracks supporting one thesis

**Structure:** Title, then N columns of [shadow + card + label] with arrows inside each column. Columns follow identical internal structure to emphasize the parallel.

**Layout guidance:** Give each column its own accent theme (column 1 tinted `--accent-1`, column 2 `--accent-2`, and so on) or rotate accents per row consistently across all columns. An optional low-emphasis background panel (a tint of `--surface` toward the column accent, or the accent at reduced strength) groups each column. 2-3 columns max; more gets crowded.

---

## 3. Cycle / Loop

**Visual:** Cards arranged in a circular or rectangular loop, arrows forming a closed circuit. The last step feeds back into an earlier step.

**Communicates:** "This is an ongoing process, not a one-time event." The loop-back arrow is the signature element; without it this is just a linear flow.

**When to use:**
- Iterative processes ("Plan, Build, Test, Iterate, repeat")
- Research or experiment cycles ("Hypothesize, Test, Evaluate, Decide, loop")
- System interaction flows where output returns as input

**Structure:** Title, cards in a circuit (a 4-card rectangle is the workhorse: top-left, top-right, bottom-right, bottom-left), solid arrows clockwise, return path closes the loop. Use a **dashed** arrow for feedback/return paths to distinguish them from the primary flow.

**Layout guidance:** Color-code stages with the accent rotation so the eye tracks position in the cycle. A short subtitle under the title ("the more you iterate, the better it gets") reinforces the loop message.

---

## 4. Layered / Concentric

**Visual:** Nested circles (onion), nested rings, or a pyramid/iceberg with horizontal layers. Inner = core, outer = periphery.

**Communicates:** "There is a core surrounded by layers." The innermost layer is the most fundamental or hidden; each outer ring adds scope or visibility. The key message is centrality.

**When to use:**
- Frameworks with priorities ("optimize for the core first, then the next ring, then the edge")
- Architecture from the inside out ("engine at the core, capabilities around it, integrations at the edge")
- Reveal/iceberg ("what people see vs what is really there": a pyramid split by a horizontal waterline)

**Structure:** Title, then nested ellipses centered on one point. Draw outer first, inner last. Each ring gets its own accent from the rotation (innermost = `--accent-1`). Arrows point outward from each ring to labels beside the diagram.

**Layout guidance:** Keep ring labels near the top edge of each ring where the band is widest. The iceberg variant is a triangle crossed by a horizontal line, with "visible" and "hidden" zone labels on the left.

---

## 5. Side-by-Side Comparison

**Visual:** Two entities left and right with matching attribute rows. Check and cross marks, color coding, a "vs" divider in the center.

**Communicates:** "Two options; look at how they differ." Unlike grid columns (parallel sameness), comparison highlights differences and tradeoffs, attribute by attribute.

**When to use:**
- Feature comparisons
- Architecture or approach tradeoffs
- Any A-vs-B decision the viewer must make

**Structure:** Title + "vs" label centered. Left group [shadow + panel + attribute rows], right group mirrored: same number of rows, same sizes, matching y positions so attributes align across the divide.

**Layout guidance:** Color-code sides semantically: the favored or positive side in the accent your brand uses for success/positive, the limited side in the accent used for caution/negative (ask the user which accents carry those roles if the design system does not say). Use ✅ / ❌ icons on rows for instant scanning. Optional: a spectrum line at the bottom showing where each option falls.

---

## 6. Tree / Breakdown

**Visual:** A top node branching downward into child nodes. Strict tree (one parent, N children) or nested breakdown (parent contains children as sub-rows with side-branching descriptions).

**Communicates:** "This thing is made of these parts" or "this category splits into these types." Composition and classification: the viewer understands what belongs inside what.

**When to use:**
- Explaining what something is (component tree)
- Anatomy/decomposition (a system broken into its files or modules)
- Classification/taxonomy ("X comes in these three kinds")
- Structural containment ("A contains B which contains C")

**Structure:** Title, parent node (visually larger or in the strongest accent), branching arrows downward, child nodes, optional sub-branches. ~100px vertical spacing per level.

**Layout guidance:** Arrows flow downward: top = whole, bottom = parts. Use accent grouping to mark categories (all children of one branch share a fill). Side labels can annotate an axis (e.g. a vertical "public to private" scale) without cluttering the tree.

---

## Cross-reference: structure x purpose

| Purpose | Best structure | Runner-up |
|---|---|---|
| Advantages / why | Stacked List | Grid Columns (if N parallel proofs) |
| Best practices / steps | Stacked List (numbered) | Cycle (if the steps repeat) |
| Levels / progression | Stacked List (bottom-to-top) | Layered (if levels nest) |
| Use cases per audience | Grid Columns | Side-by-Side (if contrasting) |
| Repeating process | Cycle / Loop | Stacked List (if it truly ends) |
| How a system works | Cycle / Loop (with feedback) | Tree (if static composition) |
| Framework with priorities | Layered / Concentric | Stacked List |
| Visible vs hidden | Layered (iceberg) | Side-by-Side |
| A vs B decision | Side-by-Side Comparison | Grid Columns (if no winner implied) |
| Anatomy / what is it | Tree / Breakdown | Stacked List (if flat) |
| Categories / types | Tree / Breakdown (classification) | Grid Columns |
