# Stockport Bin Collection Skill for Google Gemini

This project provides a live lookup from [Stockport Council's Bin Collection Finder](https://www.stockport.gov.uk/find-your-collection-day) (`https://myaccount.stockport.gov.uk/bin-collections/show/<UPRN>`) so you can ask Gemini **"what bin day is it"** or **"what bin should I put out"** across your Google account (Phone, Web, Nest speaker, and CLI).

---

## Step 1: Find Your Stockport UPRN (Takes 30 seconds)

Stockport Council gives every address a direct lookup URL using its **UPRN** (Unique Property Reference Number):

1. Open [https://www.stockport.gov.uk/find-your-collection-day](https://www.stockport.gov.uk/find-your-collection-day) and click **Find your collection day**.
2. Enter your postcode and choose your address.
3. Look at the URL in your browser's address bar:
   ```text
   https://myaccount.stockport.gov.uk/bin-collections/show/10090543805
   ```
   The number at the end (`10090543805` in this example) is your **UPRN**.

---

## Step 2: Connect to Your Google Account (Phone, Web & Nest Speaker)

Because Google sunset legacy third-party "Conversational Actions" on Google Assistant, there are **two ways** to use this live lookup on your Google Account depending on which devices you use:

### Option A: Live On-Demand Lookup in the Gemini App (Phone & Web) via a Custom Gem
Gemini in the web and mobile app can read your live Stockport Council page or your live Google Apps Script webhook on demand:

1. Open [gemini.google.com/gems](https://gemini.google.com/gems) and click **New Gem**.
2. Name it **Bin Day Checker** (or add the instruction to your **Saved Info** at [gemini.google.com/saved-info](https://gemini.google.com/saved-info) so you don't even have to select a Gem!).
3. Paste this into **Saved Info** or the Gem instructions (replacing `<YOUR_UPRN>`):
   ```text
   Whenever I ask "what bin day is it" or "what bin should I put out", fetch the live schedule from https://myaccount.stockport.gov.uk/bin-collections/show/<YOUR_UPRN> and tell me which bins (Black, Blue, Brown, Green) have the earliest upcoming collection date and what day they need to go out.
   ```

### Option B: Live Webhook + Voice Support for Nest Speakers & Google Assistant (`google_apps_script.gs`)
Nest smart speakers and hands-free voice ("Hey Google, what bin should I put out?") cannot browse arbitrary external websites directly, **but** they have native access to your Google Account via **@Google Calendar** and **Google Home Routines**:

1. Open [script.google.com](https://script.google.com) on your Google Account and click **New project**.
2. Copy the contents of [`google_apps_script.gs`](./google_apps_script.gs) into the editor.
3. Replace `REPLACE_WITH_YOUR_UPRN` on line 19 with your UPRN.
4. **For a live on-demand HTTP Webhook URL**:
   - Click **Deploy → New deployment → Web app**.
   - Set **Execute as**: `Me` and **Who has access**: `Anyone`.
   - Calling `<YOUR_WEB_APP_URL>?format=text` performs a **live scrape of Stockport Council on demand** and returns:
     `Your next bin collection is on Friday, 13 November 2026. You should put out your Blue bin and Brown bin.`
5. **For hands-free Nest Speaker / Android Voice ("What bin day is it?")**:
   - In the Apps Script toolbar, select `setupDailyTrigger` from the function dropdown and click **Run**.
   - This runs inside your Google account, fetches the live page from Stockport Council, and keeps `Bin Day: Put out <Bins>` events on your Google Calendar so Gemini on your phone, watch, or Nest speaker answers *"What bin day is it?"* or *"What bin should I put out?"* immediately.

---

## Step 3: Local Live CLI & Antigravity Skill (`stockport_bins.py`)

You can also run the live Python lookup script directly on your Mac:

```bash
python3 /Users/eggsy/Developer/stockport-bin-skill/stockport_bins.py --uprn <YOUR_UPRN>
```

Or output structured JSON:
```bash
python3 /Users/eggsy/Developer/stockport-bin-skill/stockport_bins.py --uprn <YOUR_UPRN> --json
```
