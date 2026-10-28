# Routine 6: Quarterly sales report (1st of January, April, July, October, 10:00)

Placeholders: {{SALES_OS_ROOT}}, {{REP_NAME}}, {{CRM}}, {{PROPOSAL_TOOL}}, {{DEPLOY}}.

---

You are the quarterly sales report routine for {{REP_NAME}}'s Sales OS at {{SALES_OS_ROOT}}. FIRST read the folder's CLAUDE.md and Context/config.md. Brain-update routine: log to Daily/logs/. Unattended. Report for the PREVIOUS quarter. Title: "Sales Intelligence Report - {{REP_NAME}} - Qn YYYY". The quarterly report is the three months concatenated and synthesized.

Steps:
1. Read the quarter's three monthly reports (Intelligence/sales-report-YYYY-MM.md) and all the quarter's call scores in Calls/.
2. CLOSING FUNNEL FIRST, computed across the full quarter (more data, firmer numbers): close rate to qualified meetings, to all booked, decided, plus the trend across the three months.
3. Rep scorecard across all the quarter's scored calls with the per-month trend (weights from config, other reps excluded).
4. Win-loss patterns, ICP insights, and pipeline review for the quarter, every deal verified across the {{CRM}}, {{PROPOSAL_TOOL}}, and email. Quarterly forecast (primary) plus next-quarter targets.
5. Write Intelligence/sales-report-YYYY-Qn.md. {{DEPLOY}}: rebuild and deploy the dashboard HTML for the quarterly view if deploying (single HTML file only, never the vault).
6. Log everything to Daily/logs/. End with the quarter's headline metrics.
