# Stockport Bin Collection Skill for Google Gemini (`check-stockport-bin-day`)

A custom **Google Gemini Skill** structured according to Google's official guidance ([Write effective skills for Gemini Apps](https://support.google.com/gemini/answer/17102773)).

Once added to your Google account, you can ask Gemini:
- *"What bin day is it?"*
- *"What bin should I put out?"*
- *"When is bin day?"*

Gemini will check your live [Stockport Metropolitan Borough Council](https://www.stockport.gov.uk/find-your-collection-day) collection schedule and tell you which bin(s) (**Black**, **Blue**, **Brown**, and/or **Green**) need to go out next.

---

## Repository Structure

```text
stockport-bin-skill/
├── check-stockport-bin-day/              # <-- Select THIS folder when uploading to Google Gemini
│   ├── SKILL.md                          # Main skill manifest (YAML frontmatter + instructions)
│   └── references/
│       └── stockport-bin-guide.md        # Reference guide for Stockport bin colours & UPRN lookup
├── SKILL.md                              # Root manifest for GitHub / Gemini CLI installation
├── LICENSE
└── README.md
```

### Alignment with Google's Official Skill Guidelines
Per [support.google.com/gemini/answer/17102773](https://support.google.com/gemini/answer/17102773), this skill is designed around:
1. **Action-Oriented Naming & Routing Metadata**: Uses a lowercase, hyphenated action-verb name (`check-stockport-bin-day`) and an explicit trigger `description` so Gemini activates the skill automatically when you ask about your bins.
2. **Concise "Cheat Sheet" Instructions**: Structured into four clear sections:
   - **Step-by-Step Instructions** for accuracy-critical date lookup and comparison.
   - **Rules for Missing Information** (how to handle an unconfigured UPRN or unreachable page).
   - **Formatting Rules** (concise <120-word layout grouping same-day bins).
   - **Common Mistakes to Avoid** (never guessing dates, never omitting co-collected bins).
3. **Clean Reference Packaging**: Includes `references/stockport-bin-guide.md` using only supported `.md` files (with zero hidden `.git` metadata or script files inside `check-stockport-bin-day/`).

---

## Step 1: Find Your Stockport UPRN (Takes 30 Seconds)

Stockport Council assigns every address a unique schedule URL ending in its **UPRN** (Unique Property Reference Number):

1. Open [https://www.stockport.gov.uk/find-your-collection-day](https://www.stockport.gov.uk/find-your-collection-day) and click **Find your collection day**.
2. Enter your postcode and select your address.
3. Look at the URL in your browser's address bar:
   ```text
   https://myaccount.stockport.gov.uk/bin-collections/show/10090543805
   ```
   The number at the end (`10090543805` in this example) is your **UPRN**.
4. Open [`check-stockport-bin-day/SKILL.md`](./check-stockport-bin-day/SKILL.md) and replace `REPLACE_WITH_YOUR_UPRN` on line 12 with your number (or edit it inline in Gemini after uploading).

---

## Step 2: Install into Your Google Gemini Account

1. Go to **[gemini.google.com](https://gemini.google.com)**.
2. In the left sidebar, select **Customize** (or **More → Customize**), then click **Skills**.
3. Click **Create** (or **Add**) and select **Upload**.
4. Choose the **`check-stockport-bin-day`** subfolder inside this repository:
   ```text
   /Users/eggsy/Developer/stockport-bin-skill/check-stockport-bin-day
   ```
   *(Select the `check-stockport-bin-day` subfolder rather than the top-level repository folder so the hidden `.git` directory and `LICENSE` file are not included in the upload.)*
5. Ensure `REPLACE_WITH_YOUR_UPRN` is set to your Stockport UPRN, then click **Create**.

---

## Step 3: How to Use It in Gemini

- **Automatic Trigger**: Ask *"What bin day is it?"* or *"What bin should I put out?"* in any Gemini chat.
- **Slash / Mention Command**: Type `/check-stockport-bin-day` (or `@check-stockport-bin-day`) in the prompt box to invoke the skill directly.

---

## Optional: Install via Gemini CLI

```bash
gemini skills install https://github.com/eggsy84/stockport-bin-skill.git
```
