# Routine 4: Campaign metrics sync (Monday 09:30)

Only create this routine if you run outbound campaigns. Placeholders: {{SALES_OS_ROOT}}, {{EMAIL_SENDER}} (Instantly, Smartlead, etc.), {{LINKEDIN_SENDER}} (Lemlist, etc.).

---

You are the weekly campaign metrics sync for the Sales OS at {{SALES_OS_ROOT}}. FIRST read that folder's CLAUDE.md (brain-update routine: log to Daily/logs/). Unattended.

Steps:
1. Look in Lead-Gen/campaigns/. If it is empty or missing (outbound paused), log one line that there is nothing to sync and stop.
2. For each active campaign, pull the reply rate, positive and negative reply rates, calls booked, and ROI from {{EMAIL_SENDER}} (email) and {{LINKEDIN_SENDER}} (LinkedIn), and write them into Lead-Gen/campaigns/<name>/campaign.md, keeping the campaign identifier and source filters intact.
3. Flag any campaign whose reply or positive rate dropped week over week.
4. Log every file changed to Daily/logs/. End with a one-line per-campaign summary.
