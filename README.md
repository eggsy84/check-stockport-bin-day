# Stockport Bin Collection Skill (`stockport-bins`)

A Google Gemini **Skill** (built on the open `SKILL.md` standard) that checks live waste collection dates from [Stockport Metropolitan Borough Council](https://www.stockport.gov.uk/find-your-collection-day) so you can ask Gemini:

- *"What bin day is it?"*
- *"What bin should I put out?"*

It identifies the earliest upcoming collection date and tells you which bins (**Black bin**, **Blue bin**, **Brown bin**, and/or **Green bin**) need to go out.

---

## Repository Structure

This repository follows the open **Agent Skills** (`SKILL.md`) specification so it can be uploaded directly into your Google Gemini account or installed via the Gemini CLI:

```text
stockport-bin-skill/
├── SKILL.md                        # Required Skill manifest (YAML frontmatter + instructions)
├── scripts/
│   ├── stockport_bins.py           # Zero-dependency Python live lookup CLI script
│   └── google_apps_script.gs       # Optional Google Apps Script webhook & Calendar sync
├── tests/
│   └── test_stockport_bins.py      # Unit tests for the HTML parser & schedule logic
├── LICENSE
└── README.md
```

---

## Step 1: Find Your Stockport UPRN (Takes 30 Seconds)

Stockport Council assigns every address a unique lookup URL containing its **UPRN** (Unique Property Reference Number):

1. Go to [https://www.stockport.gov.uk/find-your-collection-day](https://www.stockport.gov.uk/find-your-collection-day) and click **Find your collection day**.
2. Enter your postcode and select your address.
3. Look at the URL in your browser's address bar:
   ```text
   https://myaccount.stockport.gov.uk/bin-collections/show/10090543805
   ```
   The number at the end (`10090543805` in this example) is your **UPRN**.

*(Before uploading or installing, replace `REPLACE_WITH_YOUR_UPRN` in [`SKILL.md`](./SKILL.md) with your UPRN, or edit it inline during upload in the Gemini app.)*

---

## Step 2: Install into Your Google Gemini Account (Web & Mobile App)

Google Gemini uses **Skills** (which replaced legacy Gems) to add modular, reusable tools to your Google account.

### Option A: Upload `SKILL.md` to the Google Gemini App
1. Open **[gemini.google.com](https://gemini.google.com)** in your browser (or open the Gemini mobile app).
2. In the left sidebar, click **Customize** (or **More → Customize**), then select **Skills**.
3. Click **Create** (or **Add**) and choose **Upload**.
4. Select [`SKILL.md`](./SKILL.md) from this repository (or upload a `.zip` of this repository — Gemini automatically reads `SKILL.md` at the root).
5. In the preview editor, replace `REPLACE_WITH_YOUR_UPRN` with your numeric Stockport UPRN (e.g. `10090543805`).
6. Click **Create** to save the skill to your Google account.

### How to Use It in Gemini
Once added to your account, you can trigger the skill in two ways:
- **Automatic Activation**: Just ask *"What bin day is it?"* or *"What bin should I put out?"* in any chat — Gemini matches your prompt against the skill's `description` and runs it automatically.
- **Slash / Mention Shortcut**: Type `/stockport-bins` (or `@stockport-bins`) in the chat box to invoke the skill directly.

---

## Step 3: Install via Gemini CLI / Agent Skills CLI (Optional)

Because this repository has a root [`SKILL.md`](./SKILL.md), you can install it directly from GitHub into the **Gemini CLI**, **Antigravity**, or any compatible Agent Skills tool:

### Using Gemini CLI
```bash
gemini skills install https://github.com/eggsy84/stockport-bin-skill.git
```

### Using Universal `skills` CLI (`npx`)
```bash
npx skills add eggsy84/stockport-bin-skill
```

### Manual Global Install
Clone this repository directly into your global Gemini skills directory:
```bash
git clone https://github.com/eggsy84/stockport-bin-skill.git ~/.gemini/skills/stockport-bins
```

---

## Step 4: Optional Nest Speaker & Google Calendar Sync (`google_apps_script.gs`)

If you also ask hands-free on a **Google Nest speaker** (*"Hey Google, what bin should I put out?"*), smart speakers cannot browse external council pages directly, but they natively read your **Google Calendar**:

1. Open **[script.google.com](https://script.google.com)** and click **New project**.
2. Paste the contents of [`scripts/google_apps_script.gs`](./scripts/google_apps_script.gs) into the editor.
3. Replace `REPLACE_WITH_YOUR_UPRN` on line 19 with your Stockport UPRN.
4. Select `setupDailyTrigger` in the toolbar dropdown and click **Run**.
   - This fetches live collection dates from Stockport Council daily and keeps `Bin Day: Put out <Bins>` events on your Google Calendar so Nest speakers, Android voice, and the Gemini app can answer immediately.

---

## Local CLI Usage & Testing

You can also run the bundled Python lookup script directly on your machine (requires Python 3.10+, zero external dependencies):

```bash
python3 scripts/stockport_bins.py --uprn <YOUR_UPRN>
```

Output as JSON:
```bash
python3 scripts/stockport_bins.py --uprn <YOUR_UPRN> --json
```

Run the unit test suite:
```bash
python3 -m unittest discover -s tests
```
