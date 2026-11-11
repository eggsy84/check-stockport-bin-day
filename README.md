# Check Stockport Bin Day (`check-stockport-bin-day`)

A zero-config **Google Gemini Skill** structured according to Google's official guidance ([Write effective skills for Gemini Apps](https://support.google.com/gemini/answer/17102773)).

Once added to your Google account, you can ask Gemini:
- *"What bin day is it?"*
- *"What bin should I put out?"*
- *"When is bin day?"*

---

## Why This Skill Uses Hybrid Live-Fetch + Memory Anchor Dates

Stockport Council's portal (`myaccount.stockport.gov.uk/bin-collections/show/<UPRN>`) uses bot/firewall rules and `noindex` headers that frequently block automated AI web crawlers — even when the link opens fine in your personal browser.

To make responses **fast and 100% reliable**, this skill uses a two-layer approach:
1. **Live Fetch (When Accessible)**: Gemini checks `https://myaccount.stockport.gov.uk/bin-collections/show/<UPRN>` and refreshes your saved schedule in **Gemini's Memory / Saved Info**.
2. **Instant Anchor-Date Calculation (When Crawler Is Blocked)**: Because Stockport bin collections follow fixed repeating intervals from any known collection date (**Green**: every 7 days, **Black**: every 14 days, **Brown**: every 28 days, **Blue**: every 28 or 14 days), Gemini stores one snapshot of your 4 bin dates in **Memory** and calculates your upcoming collections mathematically whenever `myaccount.stockport.gov.uk` blocks automated crawlers.

---

## Repository Structure

```text
check-stockport-bin-day/
├── SKILL.md                          # Main skill manifest (YAML frontmatter + instructions)
├── references/
│   └── stockport-bin-guide.md        # Reference guide: bin colours, cycle math & UPRN lookup
├── README.md                         # Setup and usage documentation
└── LICENSE                           # Repository license
```

---

## Step 1: Install into Your Google Gemini Account

1. Go to **[gemini.google.com](https://gemini.google.com)**.
2. In the left sidebar, select **Customize** (or **More → Customize**), then click **Skills**.
3. Click **Create** (or **Add**) and select **Upload**.
4. Upload the skill using either method:
   - **Upload `SKILL.md` & Reference File**: Select [`SKILL.md`](./SKILL.md), then attach [`references/stockport-bin-guide.md`](./references/stockport-bin-guide.md) under reference files.
   - **Upload as a `.zip`**: Package only `SKILL.md` and `references/` (excluding `.git` and `LICENSE`, which Gemini rejects as unsupported file types):
     ```bash
     zip -r check-stockport-bin-day.zip SKILL.md references/ -x "*.DS_Store"
     ```
     Then upload `check-stockport-bin-day.zip` in the Gemini upload dialog.
5. Click **Create**.

---

## Step 2: One-Time Onboarding in Chat

1. Ask Gemini: *"What bin day is it?"* (or type `/check-stockport-bin-day`).
2. Gemini will prompt you to open [stockport.gov.uk/find-your-collection-day](https://www.stockport.gov.uk/find-your-collection-day) and paste:
   - Your property URL (e.g. `https://myaccount.stockport.gov.uk/bin-collections/show/10090543805`), **and**
   - A quick copy-paste (or screenshot) of the 4 upcoming bin dates displayed on that page.
3. Gemini saves both your **UPRN** and those **4 Anchor Dates** into **Gemini's Memory / Saved Info**. From that point on, every time you ask *"What bin should I put out?"*, Gemini answers immediately — even if Stockport Council's firewall blocks web crawlers.
