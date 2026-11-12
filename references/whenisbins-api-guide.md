# WhenIsBins (`whenisbins.com`) UK Bin Collection API Reference Guide

**WhenIsBins** (`https://whenisbins.com`) is a UK-wide service and AI agent API built by Public Digital that retrieves official household rubbish, recycling, food, and garden waste collection schedules across UK local authorities.

- **API Guide**: `https://whenisbins.com/v1/guide`
- **OpenAPI Docs**: `https://whenisbins.com/v1/docs`
- **MCP Server**: `https://whenisbins.com/mcp`

---

## 1. API Lookup Workflow (`https://whenisbins.com/v1`)

### Step 1: Discover the Council & Property (`GET /v1/addresses`)
Query the address discovery endpoint with a URL-encoded UK postcode:
```text
GET https://whenisbins.com/v1/addresses?postcode=<URL_ENCODED_POSTCODE>
```
**What it returns**:
- `council`: The UK local authority responsible for waste collections at that postcode.
- `required_input`: Any additional field required by that council (e.g., property selection or house number).
- `candidates` / `input_options`: The list of matching residential addresses and their identifiers (`property_id` / `uprn`).

**Rule**: Match the user's exact house number/street name against `candidates`. If ambiguous or missing, show the matching candidates and ask the user to confirm their address before proceeding.

---

### Step 2: Create or Retrieve a Schedule Lookup (`POST /v1/lookups` & `GET /v1/lookups/{lookup_id}`)
Initiate a lookup for the matched property:
```bash
POST https://whenisbins.com/v1/lookups
Content-Type: application/json
Idempotency-Key: <UUID>

{
  "postcode": "<POSTCODE>",
  "property": "<PROPERTY_ID>"
}
```
**Polling & Snapshot**:
- Poll `GET https://whenisbins.com/v1/lookups/{lookup_id}/wait` (or `GET https://whenisbins.com/v1/lookups/{lookup_id}`) until the status completes.
- The response returns a `collections` array containing each waste stream/bin colour, container description, and upcoming collection date, along with the official council source link.

---

## 2. Calculating Upcoming Dates from Saved Schedule Memory

When a user's schedule (`collections` dates and repeat intervals, such as weekly `7` days, fortnightly `14` days, 3-weekly `21` days, or 4-weekly `28` days) is already saved in **Gemini Memory / Saved Info** and a live `POST` call cannot be made from the current interface:

1. Check if `GET https://whenisbins.com/v1/lookups/{lookup_id}` is available using a saved `lookup_id`.
2. Otherwise, for each bin/container stored in Memory, roll its last known `anchor_date` forward by its `cycle_days` (`7`, `14`, `21`, or `28` days) until `next_date >= today` (Europe/London time):
   - `cycles_elapsed = ceil((today - anchor_date).days / cycle_days)`
   - `next_date = anchor_date + (cycles_elapsed * cycle_days)`
