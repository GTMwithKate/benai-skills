# Wireframe

Before writing any code, present the layout as a monospace box-drawing wireframe in a fenced code block.

## Why

It is the cheapest review round available. The user sees the real hierarchy, the card proportions and the length of the copy while all of it is still free to change. Describing a layout in prose gets agreement that evaporates the moment they see the page.

It also exposes two faults that are invisible in a description: cards of unequal height in the same row, and labels too long for the box they sit in.

## The format

```
REVENUE ---------------------------------------------------------------
+-------------------------------+------------------+----------------+
|  MRR                   6 col  | PAYING MEMBERS 3 | NEW MEMBERS  3 |
|                               |                  |                |
|  $ _ _ , _ _ _                |       ___        |      __        |
|  ###############.......  __%  |                  |                |
|  of $100,000 target           |  distinct        |  last 24h      |
|                               |  customers       |  7d avg __     |
+-------------------------------+------------------+----------------+

RETENTION -------------------------------------------------------------
+------------------+------------------+-------------------------------+
| MONTHLY CHURN  3 | CANCELLATIONS  3 | CHURN BY TENURE        6 col  |
|                  |                  | 0-1 mo  #########  __%        |
|      __._%       |   24h  __        | 1-3 mo  ######     __%        |
|   target 10%     |    7d  __        | 3-6 mo  ###        __%        |
|                  |   30d  __        | 6+ mo   ##         __%        |
+------------------+------------------+-------------------------------+
```

What makes it work:

- A header strip carrying the date and one freshness stamp per source
- A rule per section with the section name on it, so the bands read at a glance
- Column spans written in each box, so the grid is explicit
- Bars and sparklines drawn with block characters
- Shaded or distinct blocks for missing data, so a gap never reads as a real zero
- Note lines sitting inside the box they belong to

## Two rules

**No invented numbers.** Leave placeholders visibly blank, as underscores. A mocked figure gets believed, then quoted, then defended.

**Draw it landscape.** If it does not fit the width of a code block it will not fit a screen either, and that is useful information now rather than after the build.

## Iterate

Expect two or three rounds. Cheap rounds. Move to code only once the user says the picture is right.
