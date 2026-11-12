# Check UK Bin Day (`check-stockport-bin-day`)

A zero-config **Google Gemini Skill** for **any UK address**, structured according to Google's official guidance ([Write effective skills for Gemini Apps](https://support.google.com/gemini/answer/17102773)) and powered by **[WhenIsBins (`whenisbins.com`)](https://whenisbins.com)**.

Once added to your Google account, you can ask Gemini:
- *"What bin day is it?"*
- *"What bin should I put out?"*
- *"When is bin day?"*

Gemini will return a concise message telling you when your next collection day is and which bin(s) to put out.

---

## How It Works

1. **UK-Wide Coverage via WhenIsBins (`whenisbins.com`)**:
   Uses [WhenIsBins](https://whenisbins.com) (`https://whenisbins.com/v1/guide` and `https://whenisbins.com/mcp`) to look up official local council waste and recycling schedules for any UK postcode and address.
2. **Zero-Config Onboarding via Gemini Memory**:
   You do not need to edit [`SKILL.md`](./SKILL.md) before uploading. On first use, Gemini asks for your UK postcode and house number (or your initial schedule from `whenisbins.com`) and saves your details to **Gemini's Memory / Saved Info** so it remembers them automatically in every future chat.
3. **Direct Chat Response**:
   Returns a clean, structured message in chat showing your **Next Bin Day**, **Bins to Put Out**, and **Upcoming After That** — with no calendar setup required.

---

## Repository Structure

```text
check-stockport-bin-day/
├── SKILL.md                          # Main skill manifest (YAML frontmatter + instructions)
├── references/
│   └── whenisbins-api-guide.md       # Reference guide: WhenIsBins /v1 API & schedule math
├── README.md                         # Setup and usage documentation
└── LICENSE                           # Repository license
```

*(Note: If you rename the repository folder to `check-bin-day` or `check-uk-bin-day`, update `name:` on line 2 of `SKILL.md` to match the folder name before uploading to Gemini.)*

---

## Step 1: Install into Your Google Gemini Account

1. Go to **[gemini.google.com](https://gemini.google.com)**.
2. In the left sidebar, select **Customize** (or **More → Customize**), then click **Skills**.
3. Click **Create** (or **Add**) and select **Upload**.
4. Upload the skill using either method:
   - **Upload `SKILL.md` & Reference File**: Select [`SKILL.md`](./SKILL.md), then attach [`references/whenisbins-api-guide.md`](./references/whenisbins-api-guide.md) under reference files.
   - **Upload as a `.zip`**: Package only `SKILL.md` and `references/` (excluding `.git` and `LICENSE`, which Gemini rejects as unsupported file types):
     ```bash
     zip -r check-stockport-bin-day.zip SKILL.md references/ -x "*.DS_Store"
     ```
     Then upload `check-stockport-bin-day.zip` in the Gemini upload dialog.
5. Click **Create**.

---

## Step 2: How to Use It in Gemini

1. Ask Gemini in any chat:
   - *"What bin day is it?"*
   - *"What bin should I put out?"*
   - *"When is bin day?"*
2. On your first ask, Gemini will ask for your UK postcode and house number/address and save your schedule details to **Gemini's Memory / Saved Info**.
3. From then on, Gemini replies immediately with your next collection day and which bin(s) to put out.

---

## Optional: Install via Gemini CLI

```bash
gemini skills install https://github.com/eggsy84/stockport-bin-skill.git
```
