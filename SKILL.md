---
name: stockport-bins
description: >-
  Use this skill when the user asks "what bin day is it", "what bin should I put
  out", or asks about their Stockport Council bin collection schedule (Black,
  Blue, Brown, or Green bins).
---

# Stockport Council Bin Collection Skill

Determine the next bin collection date and which bin(s) need to be put out using live data from Stockport Metropolitan Borough Council.

## Configuration

- **Stockport Property UPRN**: `REPLACE_WITH_YOUR_UPRN`
  *(If still set to `REPLACE_WITH_YOUR_UPRN`, check whether the user has provided their UPRN, address, or collection URL in the conversation or in their Google Calendar; otherwise ask once for their UPRN from `https://www.stockport.gov.uk/find-your-collection-day`.)*
- **Live Collection URL**: `https://myaccount.stockport.gov.uk/bin-collections/show/<UPRN>`

## Procedure

### 1. Fetch the Live Schedule
- **In the Google Gemini App (Web / Mobile)**:
  1. Fetch the live Stockport Council property page at `https://myaccount.stockport.gov.uk/bin-collections/show/<UPRN>`.
  2. Locate each bin section on the page (**Black bin**, **Blue bin**, **Brown bin**, **Green bin**) and extract its next collection date (formatted like `Friday, 13 November 2026`).
  3. If a **Google Calendar** event prefixed with `Bin Day:` exists for the upcoming week, you may also cross-reference it.
- **In Gemini CLI / Local Agent Environments**:
  Run the bundled zero-dependency Python helper script:
  ```bash
  python3 ./scripts/stockport_bins.py --uprn <UPRN>
  ```

### 2. Identify Which Bin(s) to Put Out
1. Compare all extracted collection dates against today's date.
2. Find the earliest upcoming date (today or the next future date).
3. Group all bins that share that earliest date (typically multiple bins are collected on the same day, e.g., **Blue bin**, **Brown bin**, and **Green bin**).

### 3. Response Format
Reply concisely with:
1. **Next collection day**: State clearly whether it is **today**, **tomorrow**, or the specific day of the week and date (e.g., *Friday, 13 November 2026*).
2. **Bins to put out**: List the exact bin color(s) to put out for that collection:
   - **Black bin** (General waste)
   - **Blue bin** (Paper & cardboard)
   - **Brown bin** (Bottles, cans & plastic)
   - **Green bin** (Food & garden waste)
3. **Full upcoming schedule**: Briefly list the next collection date for any remaining bins not collected on that day.
