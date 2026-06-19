---
name: ctr-optimization
description: Meta title optimization using Google Search Console data. When user request meta title optimization for one or more page , run page_keywords.py to pull gsc query data, analyze keyword level ctr and postion then generate data driven title tag recommendation
---
# CTR OPTIMIZATION - META TITLE OPTIMIZER


## Overview 
Trigger this skill when a user asks to optimize meta titles for any page. The workflow: pull real GSC keyword data for the target page(s), analyze which queries drive click and impressions, and recommend title tag changes backed by search performance data.

## When to use 
- User says: optimize the meta title for this page 
- User says: this page has low ctr, fix the title 
- User says: improve my title tags based on GSC data 

## Process

### Step 1:

pull keyword-lvelv gsc data for the specific page . use `--exact` for single url to match the path pattern

```python 
python .opencode/skills/ctr-optimization/resource/page_keywords.py "<site>" "<page-url-path>" --exact -o kw.csv
```


**Output:** `kw`, `impressions`, `clicks`, `ctr`, `avg_position`, `page`

### Step 2: Analyze the GSC Data

Find the top keywords that cumulatively account for **>40% of clicks**. If clicks are too low (e.g., fewer than ~5 total clicks), fall back to impressions — use **>40% of impressions** instead. These are the queries driving most of the page's traffic — the title must serve them.

For each of these top keywords:

- **Check the page title** — Are the core words or entities from the keyword present?
  - If the keyword contains a word or entity missing from the title, add it.
  - Example: keyword "structured data schema markup guide" but title says "Meta Tags Guide" → add "structured data" and "schema markup" to the title.
- **CTR > 20%** → The title is working well for this query. Note what it does right (keyword placement, hook, tone, structure) and replicate that pattern.
- **CTR < 5% despite top-5 position** → The title likely doesn't signal relevance for this query. Prioritize adding the missing keyword/entity.

### Step 3: Determine Title Changes

Collect all missing words and entities from the top keywords. The new title should incorporate these while keeping the existing high-CTR signals intact.

### Step 4: Generate Title Recommendations (HTML Output)

Create an HTML file for each analyzed page with 2-3 title options. Include the top queries table and proposed titles side by side.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Meta Title Optimization — /page-path</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #1a1a2e; background: #f8f9fa; }
    h1 { font-size: 1.5rem; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }
    h2 { font-size: 1.1rem; color: #555; font-weight: 500; margin-top: 28px; }
    .current-title { background: #fff3cd; border: 1px solid #ffc107; border-radius: 6px; padding: 12px 16px; margin: 10px 0; font-size: 1rem; word-break: break-word; }
    table { width: 100%; border-collapse: collapse; margin: 12px 0 24px; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
    th { background: #1a1a2e; color: white; padding: 10px 12px; text-align: left; font-size: 0.85rem; }
    td { padding: 10px 12px; border-bottom: 1px solid #eee; font-size: 0.9rem; }
    tr:hover { background: #f1f3f5; }
    .ctr-good { color: #2b8a3e; font-weight: 600; }
    .ctr-poor { color: #c92a2a; font-weight: 600; }
    .options { display: flex; flex-direction: column; gap: 10px; margin: 12px 0; }
    .option { background: white; border: 1px solid #dee2e6; border-radius: 6px; padding: 12px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    .option-label { font-weight: 600; color: #1a7f37; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
    .option-title { font-size: 1rem; margin: 0; }
    .note { background: #e7f5ff; border-left: 4px solid #339af0; padding: 10px 14px; margin: 16px 0; border-radius: 0 6px 6px 0; font-size: 0.9rem; color: #1864ab; }
    .missing { background: #fff0f0; border-left: 4px solid #e03131; padding: 10px 14px; margin: 16px 0; border-radius: 0 6px 6px 0; font-size: 0.9rem; }
    .footer { margin-top: 32px; font-size: 0.8rem; color: #868e96; border-top: 1px solid #dee2e6; padding-top: 12px; text-align: center; }
  </style>
</head>
<body>

  <h1>🔍 Meta Title Optimization</h1>
  <p style="color: #868e96;">Generated from GSC data (last 90 days)</p>

  <h2>Page</h2>
  <p><code>/blog/guide-to-schema-markup</code></p>

  <h2>Current Title</h2>
  <div class="current-title"><strong>Guide to Schema Markup | Brand</strong></div>

  <h2>Top Queries Driving &gt;50% of Traffic</h2>
  <table>
    <thead>
      <tr><th>Query</th><th>Impressions</th><th>Clicks</th><th>CTR</th><th>Avg Position</th></tr>
    </thead>
    <tbody>
      <tr><td>schema markup guide</td><td>4,200</td><td>88</td><td class="ctr-poor">2.1%</td><td>4.3</td></tr>
      <tr><td>structured data seo</td><td>3,100</td><td>12</td><td class="ctr-poor">0.4%</td><td>5.1</td></tr>
      <tr><td>what is schema markup</td><td>2,800</td><td>252</td><td class="ctr-good">9.0%</td><td>2.8</td></tr>
      <tr><td>schema markup example</td><td>1,900</td><td>418</td><td class="ctr-good">22.0%</td><td>1.6</td></tr>
      <tr><td>json-ld structured data</td><td>1,400</td><td>14</td><td class="ctr-poor">1.0%</td><td>6.2</td></tr>
    </tbody>
  </table>

  <h2>Missing Words / Entities in Title</h2>
  <div class="missing">
    <strong>Missing from current title:</strong> "structured data", "JSON-LD", "example"<br>
    <strong>Top queries contain these but the title doesn't</strong> — adding them can improve relevance signals and CTR.
  </div>

  <h2>Proposed Title Options</h2>
  <div class="options">
    <div class="option">
      <div class="option-label">✦ Option 1 (Recommended)</div>
      <p class="option-title"><strong>Schema Markup Guide: Structured Data Examples for Higher CTR</strong></p>
      <p style="margin:4px 0 0; font-size:0.85rem; color:#555;">Adds "structured data" and "examples" — covers top queries missed by current title.</p>
    </div>
    <div class="option">
      <div class="option-label">✦ Option 2</div>
      <p class="option-title"><strong>What Is Schema Markup? A Guide to Structured Data &amp; JSON-LD</strong></p>
      <p style="margin:4px 0 0; font-size:0.85rem; color:#555;">Targets the "what is" intent directly; includes "JSON-LD".</p>
    </div>
    <div class="option">
      <div class="option-label">✦ Option 3</div>
      <p class="option-title"><strong>Schema Markup Guide: How to Add Structured Data (With Examples)</strong></p>
      <p style="margin:4px 0 0; font-size:0.85rem; color:#555;">Action-oriented, includes "with examples" — matches high-CTR query.</p>
    </div>
  </div>

  <div class="note">
    <strong>Note:</strong> "schema markup example" already has 22% CTR — Option 1 and 3 preserve this strength by keeping "examples" visible.
  </div>

  <div class="footer">Generated by GSC CTR Optimizer Skill</div>
</body>
</html>
```

Save this as `<page-slug>-title-options.html` and present it to the user.

### Step 5: Include Key Optimization Rules

- **Length:** 50-60 characters (avoid truncation in SERP)
- **Front-load:** Primary keyword in the first 30 characters
- **Hook:** Add numbers, questions, power words, or a clear benefit
- **Intent match:** Informational → guide/tips/how-to. Transactional → best/buy/compare
- **Brand:** Place at the end or omit if unnecessary

## Optimization Playbook

### Title Formula Reference

| Intent | Formula | Example |
|--------|---------|---------|
| Informational | `[Keyword]: [Benefit/Hook]` | "SEO Guide: 10 Proven Strategies for 2025" |
| Listicle | `[Number] [Adjective] [Keyword]` | "7 Best SEO Tools for Small Business Owners" |
| How-to | `How to [Verb] [Keyword] [Outcome]` | "How to Write Meta Titles That Get Clicks" |
| Transactional | `[Keyword] — [Best/Review/Compare]` | "Best Keyword Research Tools — Reviewed & Compared" |
| Question | `[Question]? [Answer Hook]` | "What Is Schema Markup? A Beginner's Guide" |

### Common Fixes

| Existing Pattern | Problem | Fix |
|------------------|---------|-----|
| `"Product Name | Brand"` | No hook, no value prop | Add benefit or use case |
| `"Blog Post Title"` | Missing target keyword | Front-load the primary query |
| `"Guide to X — Brand"` | Keyword at end, truncated in SERP | Move keyword to front |
| `"X: Everything You Need to Know"` | Vague, no differentiator | Add number or specific outcome |

## Verification

After title changes are implemented:

- [ ] Wait 2-4 weeks for Google to re-crawl and re-evaluate
- [ ] Re-run `page_keywords.py` for the same page and compare CTR
- [ ] Check that position didn't drop significantly
- [ ] Confirm impressions remained stable or improved
- [ ] Document the before/after to build a pattern library

## Red Flags

- Don't suggest titles that mislead or don't match page content
- Don't change titles weekly — Google needs time to re-index
- Don't strip brand from the title if brand recognition drives clicks
- Don't optimize for a keyword the page has no content for
- Don't recommend titles purely based on position — consider intent and relevance first
