# ClearCents daily-posts routine

Versioned copy of the scheduled task that writes 4 blog posts per day.

**Live task file:** `~/.claude/scheduled-tasks/clearcents-daily-posts/SKILL.md`
This file is a committed mirror for change history. Keep the two in sync manually,
or repoint the scheduled task at this path.

**Last pipeline change:** 2026-09-03 — replaced blind category topic-picking with a
Google-search competitor-gap research pipeline (steps 2a–2d) and a "beat the page to
beat" instruction in step 4. DataForSEO was evaluated and dropped (API returned 403);
the pipeline uses free WebSearch/WebFetch instead. Step 2a (own striking-distance
keywords) needs a manual GSC export at `_data/gsc-latest.csv` and is skipped when
that file is absent.

---

## SKILL.md

```markdown
---
name: clearcents-daily-posts
description: Write and push 4 ClearCents blog posts daily — with mandatory internal links to near-page-1 posts
---

Daily ClearCents blogging routine. Working directory: C:\Users\Johno\OneDrive\BLOGGING\clearcents

Write and push 4 new blog posts for today's date.

Steps:
1. Check today's date: run PowerShell `Get-Date -Format 'yyyy-MM-dd'`
2. Pick 4 topics using the RESEARCH PIPELINE below (not a blind category grab-bag).
   Still spread the 4 across: budgeting, save-money, debt-free, investing, side-hustles.

   --- TOPIC RESEARCH PIPELINE (do this before writing anything) ---

   2a. STRIKING-DISTANCE CHECK (manual — no API access).
       If a fresh Google Search Console export is pasted into this run or saved at
       _data/gsc-latest.csv, use it: list queries where clearcentslife.com ranks
       positions 8-25 with >0 impressions. Each is a page one supporting post could
       push onto page 1 — these are the HIGHEST priority topics.
       If no GSC data is available, skip 2a and rely on 2b/2c, and note in the
       output that 2a was skipped.

   2b. COMPETITOR-GAP DISCOVERY (Google search via WebSearch).
       Brainstorm ~10 candidate topics NOT already covered in _posts/ (check step 5
       first). For each finalist, run a WebSearch for the head query and read the
       first page of results:
         - Who ranks? If page 1 is ALL big finance brands (NerdWallet, Ramsey,
           Fidelity, Bankrate, Investopedia, CNBC, SoFi, government sites) → HARD,
           drop it or find a longer-tail angle.
         - If page 1 includes small/independent finance blogs, credit-union blogs,
           thin "N tips" pages, or forum/Reddit threads → WINNABLE, keep it.
       Prefer topics that (a) extend a cluster we already have (e.g. a dollar-amount
       or comparison variant of an existing post) and (b) let the new post link to
       3+ existing posts.

   2c. SHORTLIST. Pick 4 winnable topics, still spread across the 5 categories,
       ranked by: feeds an existing GSC priority (2a) > extends a ranking cluster >
       fresh winnable SERP. Hold the rest for a future run.

   2d. GET THE PAGE TO BEAT. For each of the 4, WebSearch the query, take the
       top organic non-brand result, and WebFetch it for: word count, H2 outline,
       whether it has an FAQ, and any obvious gaps or outdated figures. Pass this
       into step 4.

   --- END PIPELINE ---

3. Write each post as _posts/YYYY-MM-DD-slug.md with this front matter:
   - layout: post
   - title, date, categories, tags, description
   - image: Unsplash URL (w=800&q=80&auto=format&fit=crop)
   - permalink: /category/slug/
   - faq: 3-4 Q&A pairs
4. Each post body: H1 heading, 800-1200 words, NO filler.
   BEAT THE PAGE TO BEAT (from step 2d): cover everything the current top-ranking
   page covers, then exceed it — more specific numbers, a cleaner step sequence,
   an FAQ it lacks, current 2026 figures, a tighter intro. Match or modestly
   exceed its word count (still within 800-1200). Never copy its wording or structure.

MANDATORY INTERNAL LINKING — do this in every post, every day:

These two pages are on the verge of hitting Google page 1 (positions 11-14). Every post MUST link to at least one of them where it fits naturally:

  A. /save-money/how-to-save-1000-dollars-in-3-months/
     Link text ideas: "save your first $1,000", "build a $1,000 starter fund", "hit $1,000 saved in 3 months"
     Natural fit: any budgeting, savings, or side hustle post

  B. /budgeting/zero-based-budgeting-guide/
     Link text ideas: "give every dollar a job", "zero-based budget", "zero-based budgeting"
     Natural fit: any budgeting, paycheck-to-paycheck, or debt post

Also link to these high-impression posts whenever the topic fits (they need authority to climb from position 60-80).
(Impression/position figures below are a manual snapshot — refresh them from GSC data when step 2a has it, and swap in any new positions 8-25 pages as priority link targets.)
  - /debt-free/how-to-pay-off-credit-card-debt/  → 520 impressions, pos 77 — link from ANY debt post
  - /investing/index-funds-for-beginners/         → 79 impressions, pos 59 — link from investing posts
  - /debt-free/how-to-negotiate-with-creditors/  → 64 impressions, pos 77 — link from debt posts
  - /save-money/save-money-on-car-insurance/      → 53 impressions, pos 70 — link from save-money posts

Rule: each post should have 3-5 internal links total. At least 1 must be to post A or B above.

5. Before picking topics (step 2b), scan ALL of _posts/ — not just the last 5-10 days —
   for slugs covering the candidate topic or a close variant. Skip anything already
   covered unless the new angle is clearly distinct (e.g. a dollar-amount or
   head-to-head comparison version of an existing explainer).
6. After all 4 files are written: git add _posts/YYYY-MM-DD-*.md, git commit, git push

Do NOT touch .github/workflows/ files — those are managed separately.
GitHub Actions runs automatically at 11:00 UTC (indexing) and 11:03 UTC (Pinterest pinning).

Goal: 4 posts/day → 120/month → $2k/month AdSense by December 2026
SEO priority: push /save-money/how-to-save-1000-dollars-in-3-months/ and /budgeting/zero-based-budgeting-guide/ to page 1 through consistent internal linking.
```
