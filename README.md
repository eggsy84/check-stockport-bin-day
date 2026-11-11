# Check Stockport Bin Day (`check-stockport-bin-day`)

A custom **Google Gemini Skill** structured according to Google's official guidance ([Write effective skills for Gemini Apps](https://support.google.com/gemini/answer/17102773)).

Once added to your Google account, you can ask Gemini:
- *"What bin day is it?"*
- *"What bin should I put out?"*
- *"When is bin day?"*

Gemini will check your live [Stockport Metropolitan Borough Council](https://www.stockport.gov.uk/find-your-collection-day) collection schedule and tell you which bin(s) (**Black**, **Blue**, **Brown**, and/or **Green**) need to go out next.

---

## Repository Structure

```text
check-stockport-bin-day/
├── SKILL.md                          # Main skill manifest (YAML frontmatter + instructions)
├── references/
│   └── stockport-bin-guide.md        # Reference guide for Stockport bin colours & UPRN lookup
├── README.md                         # Setup and usage documentation
└── LICENSE                           # Repository license
```

### Alignment with Google's Official Skill Guidelines
Per [support.google.com/gemini/answer/17102773](https://support.google.com/gemini/answer/17102773), this skill is designed around:
1. **Matching Directory & Action-Verb Name**: Both the skill directory and the `name` field in [`SKILL.md`](./SKILL.md) use the lowercase, hyphenated action-verb identifier `check-stockport-bin-day`, paired with an explicit trigger `description` so Gemini activates the skill automatically when you ask about your bins.
2. **Concise "Cheat Sheet" Instructions**: [`SKILL.md`](./SKILL.md) is structured into four focused sections:
   - **Step-by-Step Instructions** for resolving your property URL, fetching live dates, and comparing against today's UK date.
   - **Rules for Missing Information** (how to handle an unconfigured UPRN or unreachable council page).
   - **Formatting Rules** (concise <120-word bulleted output grouping same-day collections).
   - **Common Mistakes to Avoid** (never guessing dates, never omitting co-collected bins, no conversational filler).
3. **Supplemental Reference File**: [`references/stockport-bin-guide.md`](./references/stockport-bin-guide.md) stores the Stockport bin colour/contents table and UPRN lookup guide separately so [`SKILL.md`](./SKILL.md) stays lean.

---

## Step 1: Find Your Stockport UPRN (Takes 30 Seconds)

Stockport Council assigns every address a permanent schedule URL ending in its **UPRN** (Unique Property Reference Number):

1. Open [https://www.stockport.gov.uk/find-your-collection-day](https://www.stockport.gov.uk/find-your-collection-day) and click **Find your collection day**.
2. Enter your postcode and select your address.
3. Look at the URL in your browser's address bar:
   ```text
   https://myaccount.stockport.gov.uk/bin-collections/show/10090543805
   ```
   The number at the end (`10090543805` in this example) is your **UPRN**.
4. Open [`SKILL.md`](./SKILL.md) and replace `REPLACE_WITH_YOUR_UPRN` on line 12 with your number (or edit it inline in Gemini after uploading).

---

## Step 2: Install into Your Google Gemini Account

1. Go to **[gemini.google.com](https://gemini.google.com)**.
2. In the left sidebar, select **Customize** (or **More → Customize**), then click **Skills**.
3. Click **Create** (or **Add**) and select **Upload**.
4. Upload the skill using either method:
   - **Upload `SKILL.md` & Reference File**: Select [`SKILL.md`](./SKILL.md), then attach [`references/stockport-bin-guide.md`](./references/stockport-bin-guide.md) under reference files.
   - **Upload as a `.zip` or Folder**: Package only `SKILL.md` and `references/` (excluding `.git` and `LICENSE`, which Gemini rejects as unsupported file types):
     ```bash
     zip -r check-stockport-bin-day.zip SKILL.md references/ -x "*.DS_Store"
     ```
     Then upload `check-stockport-bin-day.zip` in the Gemini upload dialog.
5. Verify that `REPLACE_WITH_YOUR_UPRN` is set to your Stockport UPRN, then click **Create**.

---

## Step 3: How to Use It in Gemini

- **Automatic Trigger**: Ask *"What bin day is it?"*, *"What bin should I put out?"*, or *"When is bin day?"* in any Gemini chat.
- **Slash / Mention Command**: Type `/check-stockport-bin-day` (or `@check-stockport-bin-day`) in the prompt box to invoke the skill directly.

---

## Optional: Install via Gemini CLI

```bash
gemini skills install https://github.com/eggsy84/stockport-bin-skill.git
```
