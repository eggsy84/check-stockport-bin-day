# Check UK Bin Day (`what-bin-day-is-it`)

A zero-config **Agent Skill** for **any UK address**, powered by the **[WhenIsBins (`whenisbins.com`)](https://whenisbins.com)** MCP server (`https://whenisbins.com/mcp`).

Once installed alongside the WhenIsBins MCP server, you can ask:
- *"What bin day is it?"*
- *"What bin should I put out?"*
- *"When is bin day?"*

The agent will prompt for your UK postcode and house number on first use, query the WhenIsBins MCP server directly, and return a concise message telling you when your next collection day is and which bin(s) to put out — without you ever having to visit a website yourself.

---

## How It Works

1. **UK-Wide Coverage via the WhenIsBins MCP Server (`https://whenisbins.com/mcp`)**:
   Uses the WhenIsBins MCP tools (`find_addresses`, `get_collections`, `check_lookup`, and `get_schedule`) to look up official local council waste and recycling schedules for any UK postcode and house number.
2. **Zero-Config Onboarding via Memory**:
   You do not need to edit [`SKILL.md`](./SKILL.md) before installing. On first use, the agent asks for your UK postcode and house number and saves your resolved `property_id` to **Memory / Saved Info** so it remembers your address automatically in future chats.
3. **Direct Chat Response (No URLs to Visit)**:
   Returns a clean, structured message in chat showing your **Next Bin Day**, **Bins to Put Out**, and **Upcoming After That** — with no websites to visit and no calendar setup required.

---

## Repository Structure

```text
what-bin-day-is-it/
├── SKILL.md                          # Main skill manifest (YAML frontmatter + instructions)
├── references/
│   └── whenisbins-api-guide.md       # Reference guide: WhenIsBins MCP server & tool workflow
├── README.md                         # Setup and usage documentation
└── LICENSE                           # Repository license
```

---

## Step 1: Configure the WhenIsBins MCP Server

Add the `whenisbins` remote MCP server (`https://whenisbins.com/mcp`) to your client's MCP configuration (for example, `~/.gemini/config/mcp_config.json` in Antigravity / Gemini CLI):

```json
{
  "mcpServers": {
    "whenisbins": {
      "url": "https://whenisbins.com/mcp"
    }
  }
}
```

---

## Step 2: Install the Skill

### Option A: Gemini CLI / Antigravity
Install the skill repository directly:

```bash
gemini skills install https://github.com/eggsy84/what-bin-day-is-it.git
```

Or copy this folder into `~/.gemini/config/skills/what-bin-day-is-it/` (global) or `.agents/skills/what-bin-day-is-it/` (workspace).

---

## Step 3: How to Use It

1. Ask in any chat:
   - *"What bin day is it?"*
   - *"What bin should I put out?"*
   - *"When is bin day?"*
2. On your first ask, the agent will prompt you for your **UK postcode and house number/name**, resolve your property via the WhenIsBins MCP server, and save your details to **Memory / Saved Info**.
3. From then on, the agent replies immediately with your next collection day and which bin(s) to put out.
