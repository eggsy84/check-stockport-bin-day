# Stockport Council Bin Types, Cycles & UPRN Reference Guide

## 1. How to Find a Stockport Property UPRN & Initial Dates

Stockport Metropolitan Borough Council assigns every residential property a Unique Property Reference Number (**UPRN**) for waste collection schedules:

1. Open [https://www.stockport.gov.uk/find-your-collection-day](https://www.stockport.gov.uk/find-your-collection-day) and select **Find your collection day**.
2. Enter the property postcode and select the street address from the dropdown list.
3. The browser redirects to a permanent property schedule URL formatted as:
   `https://myaccount.stockport.gov.uk/bin-collections/show/<UPRN>`
4. The page displays the next collection date for each of the four bins (**Black bin**, **Blue bin**, **Brown bin**, **Green bin**).

---

## 2. Stockport Household Bin Colours, Contents & Collection Cycles

Stockport collections follow fixed repeating intervals from any known collection date for each bin:

| Bin Colour | Waste Type | Default Cycle | What Goes Inside |
| :--- | :--- | :--- | :--- |
| **Green bin** | Food & garden waste | **Every 7 days** (Weekly) | Cooked and uncooked food scraps, grass cuttings, hedge trimmings, leaves, small twigs, cut flowers. |
| **Black bin** | General household waste | **Every 14 days** (2 weeks) | Non-recyclable household rubbish, nappies, pet waste, plastic film/bags, polystyrene. |
| **Blue bin** | Paper & cardboard | **Every 28 days** (4 weeks, or 14 days if fortnightly) | Newspapers, magazines, envelopes, cardboard boxes, greetings cards (no glitter), catalogues. |
| **Brown bin** | Glass, cans & plastics | **Every 28 days** (4 weeks) | Glass bottles and jars, food tins, drink cans, aerosols, plastic bottles, foil, yogurt pots, food trays. |

---

## 3. How to Calculate Upcoming Dates from Anchor Dates

When `myaccount.stockport.gov.uk` blocks automated web crawlers, calculate each bin's next collection date from its stored **Anchor Date** in Memory:

1. Let `anchor_date` be the last known collection date for that bin, and `cycle_days` be its collection interval (`7` for Green, `14` for Black, `28` for Brown, `28` or `14` for Blue).
2. Add multiples of `cycle_days` to `anchor_date` until the resulting date is **greater than or equal to today's date** (`next_date >= today`).
   - Formula: If `today > anchor_date`, `weeks_elapsed = ceil((today - anchor_date).days / cycle_days)`, and `next_date = anchor_date + (weeks_elapsed * cycle_days)`.
3. Note: Around Christmas / New Year bank holidays, collections may shift by 1–2 days; remind the user to verify bank holiday adjustments if a collection falls on December 25, December 26, or January 1.

---

## 4. Collection Rules

- Bins must be placed at the edge of the property boundary by **7:00 AM** on the scheduled collection day (or the evening before).
- Multiple bins (for example, **Blue bin**, **Brown bin**, and **Green bin**) are frequently collected on the same day.
