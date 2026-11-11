---
name: stockport-bins
description: >-
  Live lookup of Stockport Council bin collection days ("what bin day is it",
  "what bin should I put out", Black/Blue/Brown/Green bin schedule) directly
  from https://myaccount.stockport.gov.uk/bin-collections/show/<UPRN>.
---

# Stockport Council Bin Collection Skill

When the user asks **"what bin day is it"**, **"what bin should I put out"**, or asks about their Stockport bin collection schedule:

1. Check if `STOCKPORT_UPRN` is configured in the environment or passed by the user.
   - If you do not yet have their UPRN, ask the user for either:
     - Their **Stockport UPRN** (the number at the end of `https://myaccount.stockport.gov.uk/bin-collections/show/<UPRN>` after looking up their address at `https://www.stockport.gov.uk/find-your-collection-day`), or
     - The full URL of their collection page.
2. Run the live lookup script:
   ```bash
   python3 stockport_bins.py --uprn <UPRN>
   ```
3. Report clearly:
   - Which bin(s) to put out next (**Black bin**, **Blue bin**, **Brown bin**, and/or **Green bin**)
   - The day of the week and date of the next collection
   - The full upcoming schedule for all four bins
