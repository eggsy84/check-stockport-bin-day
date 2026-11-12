# WhenIsBins (`whenisbins.com`) MCP Server Reference Guide

**WhenIsBins** (`https://whenisbins.com`) provides a remote Model Context Protocol (MCP) server (`com.whenisbins/bin-collections`) that retrieves official household rubbish, recycling, food, and garden waste collection schedules across UK local authorities.

- **MCP Server Endpoint (Streamable HTTP)**: `https://whenisbins.com/mcp`
- **MCP Namespace**: `com.whenisbins/bin-collections`

---

## 1. MCP Server Configuration

To connect an MCP-compatible client (such as Antigravity, Gemini CLI, Claude Code, or Cursor) to the WhenIsBins MCP server, register the remote Streamable HTTP endpoint in `mcp_config.json`:

```json
{
  "mcpServers": {
    "whenisbins": {
      "url": "https://whenisbins.com/mcp"
    }
  }
}
```

No API key or user authentication is required for personal use.

---

## 2. MCP Tool Workflow

The `whenisbins` MCP server exposes four tools that work in sequence to resolve an address and retrieve its upcoming bin collections:

### Step 1: Resolve the Property (`find_addresses`)
Call `find_addresses` with the user's UK `postcode` (and house number/name if supported by the tool input schema):
- **What it returns**:
  - `council`: The UK local authority responsible for waste collections at that postcode.
  - `required_input`: Any additional field required by that council.
  - `candidates` / `input_options`: Matching residential addresses and their identifiers (`property_id` / `uprn`).
- **Rule**: Match the user's exact house number or house name against the returned candidates. If multiple candidates match (e.g., subdivided flats), list the matching addresses in plain text and ask the user to confirm which one is theirs before proceeding.

### Step 2: Initiate Collection Lookup (`get_collections`)
Call `get_collections` using the `postcode` and the matched `property` (`property_id` / `uprn`) from `find_addresses`:
- **What it returns**:
  - Either the completed `collections` array immediately, or an asynchronous `lookup_id` with a status indicator (e.g., `still_working` or `partial`) while the council schedule is being fetched.

### Step 3: Poll Asynchronous Lookups (`check_lookup`)
If `get_collections` returns an in-progress lookup (`still_working` or `partial`):
- Call `check_lookup` passing the `lookup_id` until the lookup status settles (`settled` / completed) and returns the full `collections` array.
- Each item in `collections` includes the bin/container name or colour, waste stream description, and next collection date.

### Step 4: Fast Repeat Lookups (`get_schedule`)
Once a user's `property_id` has been resolved and saved in Memory:
- On future requests, call `get_schedule` with the saved `property_id` to retrieve the stored collection schedule directly.
- If the cached schedule is expired or unavailable, fall back to `get_collections` (and `check_lookup` if needed) using the saved `postcode` and `property_id`.

---

## 3. Data Handling & User Experience Rules

- **Never send users to external URLs**: All address discovery and schedule lookups must happen through the MCP tools above. Never ask the user to visit `whenisbins.com` or their council website, and omit source URLs from your final response unless explicitly requested.
- **Timezone**: Always evaluate "Today" and "Tomorrow" relative to `Europe/London` local time.
- **Same-day collections**: Multiple bins are frequently collected on the same day. Always group every bin/container sharing the earliest upcoming collection date under **Bins to Put Out**.
