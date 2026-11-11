# Check Stockport Bin Day (`check-stockport-bin-day`)

A zero-config **Google Gemini Skill** structured according to Google's official guidance ([Write effective skills for Gemini Apps](https://support.google.com/gemini/answer/17102773)).

Once added to your Google account, you can ask Gemini:
- *"What bin day is it?"*
- *"What bin should I put out?"*
- *"When is bin day?"*

On your first ask, Gemini will guide you to grab your Stockport Council property number (**UPRN**), save it to **Gemini's Memory / Saved Info** so you never have to enter it again, and check your live [Stockport Metropolitan Borough Council](https://www.stockport.gov.uk/find-your-collection-day) collection schedule to tell you which bin(s) (**Black**, **Blue**, **Brown**, and/or **Green**) need to go out next.

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
2. **Zero-Config Onboarding via Gemini Memory**: No files need to be edited before uploading. If Gemini doesn't know your Stockport UPRN yet, it walks you through finding it and saves it to **Gemini's Memory / Saved Info** for all future conversations.
3. **Concise "Cheat Sheet" Instructions**: [`SKILL.md`](./SKILL.md) is structured into four focused sections:
   - **Step-by-Step Instructions** for checking memory, saving a new UPRN, fetching live dates, and comparing against today's UK date.
   - **Rules for Missing Information** (guided first-time setup when no UPRN is stored yet, plus fallback if the council site is unreachable).
   - **Formatting Rules** (concise <120-word bulleted output grouping same-day collections).
   - **Common Mistakes to Avoid** (never guessing dates, never omitting co-collected bins, no conversational filler).
4. **Supplemental Reference File**: [`references/stockport-bin-guide.md`](./references/stockport-bin-guide.md) stores the Stockport bin colour/contents table and UPRN lookup guide separately so [`SKILL.md`](./SKILL.md) stays lean.

---

## Step 1: Install into Your Google Gemini Account (No File Editing Required)

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

## Step 2: How to Use It in Gemini

1. Ask Gemini:
   - *"What bin day is it?"*
   - *"What bin should I put out?"*
   - *(Or type `/check-stockport-bin-day` in the chat box)*
2. **First-Time Setup**: The first time you ask, Gemini will prompt you to look up your address at [stockport.gov.uk/find-your-collection-day](https://www.stockport.gov.uk/find-your-collection-day) and paste the resulting URL (e.g. `https://myaccount.stockport.gov.uk/bin-collections/show/12345678910`) or the UPRN number at the end.
3. Gemini will **save your UPRN to its Memory** and immediately tell you which bin(s) to put out. On every future ask, it will remember your UPRN automatically.

---

## Optional: Install via Gemini CLI

```bash
gemini skills install https://github.com/eggsy84/stockport-bin-skill.git
```
