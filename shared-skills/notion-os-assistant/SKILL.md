---
name: notion-os-assistant
description: "Notion OS Assistant for Ben AI's second brain / operating system, hosted in Notion. Use whenever the user asks about projects, tasks, active work, meetings, decisions, notes, daily log, people, teammates, contacts, company context (strategy, ICP, brand, pain points), departments, processes, or anything about my OS, my second brain, the workspace, or what is on my plate. Reads and writes through the Notion connector."
---

# Notion OS Assistant — Ben AI

This skill operates Ben AI's OS, which lives in **Notion**. The data is in databases;
this file is the router. Operate entirely through the **Notion connector** (search / fetch /
create-pages / update-page / create-view) — there are no local files.

## First, every session
1. `fetch` the master index page — **CLAUDE.md**: https://app.notion.com/p/37b1124570fe81e5b2d4ff25fa8497a3 — to load the live
   conventions + database map.
2. Then query only the database you need. Don't scan the whole workspace.

## Routing table
| If the request is about… | Database | data_source_id |
|---|---|---|
| company/you facts — strategy, ICP, brand, pain points | 📌 Context | df7497e0-f34b-4d0e-ac1c-36e828e609d8 |
| projects / active work / status | 🚀 Projects | cefeee2d-4fa6-450e-bb6f-cfc904e27662 |
| meetings / decisions / competitor or market notes | 🧠 Intelligence | 30029304-e13c-44a3-bb14-f6c667e1c841 |
| daily log / what I did / today | 🗓️ Daily | bc868da7-aef4-4572-a9a2-2531463f03df |
| people / teammates / contacts | 👥 People | c2dc34a4-fe5a-4da9-bdf5-989f08aebfda |
| prompts / frameworks / saved links | 📚 Resources | e2fcbd9b-f225-4770-a286-b2f23d26adec |
| departments / org units | 🏢 Departments | 9b1f5842-c7ac-4454-b41c-0f14397e85bd |
| SOPs / processes | ⚙️ Processes | ec90a892-eb66-41c9-bb5f-153702a524e4 |

## How to read
- Search within a database: connector search scoped to its `data_source_url`
  (`collection://<data_source_id>`), or `fetch` a specific page by URL.
- Filter by property; never read everything.

## Capture rules (writing)
- New meeting / decision / competitor / market note → row in **Intelligence**, link Project + People.
- New project → row in **Projects** (Status, Owner, Deadline); Overview / Current Status / Next Steps in the body.
- Each working day → row in **Daily**.
- New person → row in **People** (Type, Reports to).
- New long-form company/you fact → row in **Context** (set Category; body holds the detail).
- Writing a URL property → use the key `userDefined:URL`.
- Relations need both rows to exist; link by page URL.

## Rules
- Operate via the Notion connector only; this OS has no local files.
- Fetch CLAUDE.md first each session; it is the source of conventions.
- Preserve specificity (real names, numbers, dates). Omit empty fields — never write placeholders.
- Home page: https://app.notion.com/p/37b1124570fe81458d5cc00aa4a3361f
