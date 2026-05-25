# Slack MCP Server Setup Guide

This guide walks you through setting up the Slack MCP server for Zed.

## Prerequisites

You need to create a Slack App and obtain the following credentials:

1. **SLACK_BOT_TOKEN**: Starts with `xoxb-`
2. **SLACK_TEAM_ID**: Starts with `T`
3. **SLACK_CHANNEL_IDS**: Channel IDs where the bot can post (comma-separated)

## Step 1: Create a Slack App

1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Click **"Create New App"** → **"From scratch"**
3. Choose your workspace and name your app (e.g., "Zed MCP Assistant")

## Step 2: Configure OAuth Permissions

1. In your app dashboard, go to **"OAuth & Permissions"**
2. Add these **Bot Token Scopes**:
   - `chat:write` - Send messages
   - `chat:write.public` - Send messages to channels the bot isn't in
   - `channels:read` - Read channel information
   - `groups:read` - Read private channels
   - `mpim:read` - Read group messages
   - `im:read` - Read direct messages
   - `search:read` - Search messages and files
   - `users:read` - Read user information

3. Click **"Install to Workspace"** and authorize

## Step 3: Get Your Credentials

After installation, you'll need to collect:

### Bot Token
- On the **OAuth & Permissions** page
- Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### Team ID  
- On the **Basic Information** page under **App Credentials**
- Copy the **Team ID** (starts with `T`)

### Channel IDs
To get channel IDs:
1. Open Slack and go to a channel
2. Copy the channel ID from the URL or use Slack's API
3. Example: `C1234567890`

Alternatively, you can use the **List Conversations API**:
```bash
curl -H "Authorization: Bearer YOUR_BOT_TOKEN" \
  "https://slack.com/api/conversations.list"
```

## Step 4: Configure Environment Variables

Create a `.env.mcp-slack` file (not tracked by git):

```bash
# .env.mcp-slack
export SLACK_BOT_TOKEN="xoxb-your-bot-token-here"
export SLACK_TEAM_ID="T01234567"
export SLACK_CHANNEL_IDS="C01234567,C76543210"
```

**Important**: Never commit this file!

## Step 5: Configure Zed

The `.mcp.json` file is already configured. You just need to load your environment variables.

### Option A: Source before starting Zed

```bash
# Load environment variables
source .env.mcp-slack

# Then start Zed
zed .
```

### Option B: Add to shell profile

Add these lines to your `~/.bashrc` or `~/.zshrc`:

```bash
if [ -f ~/.pixelated-env.mcp-slack ]; then
  source ~/.pixelated-env.mcp-slack
fi
```

### Option C: Use Zed's settings (alternative)

If you prefer, you can configure it directly in Zed settings:
```json
{
  "context_servers": {
    "slack": {
      "settings": {
        "SLACK_BOT_TOKEN": "xoxb-your-token",
        "SLACK_TEAM_ID": "T01234567",
        "SLACK_CHANNEL_IDS": "C01234567,C76543210"
      }
    }
  }
}
```

**⚠️ Warning**: Option C exposes credentials in plain text in settings. Option A/B with environment variables is more secure.

## Step 6: Verify Setup

Test the connection by asking Zed/Claude:

> "Send a test message to Slack channel [channel name]"

Or check if the MCP server is available:
- Look for "Slack" in your available tools
- Try searching for Slack channels or messages

## Capabilities

Once connected, the Slack MCP server enables:

- **Search**: Find messages, files, members, and channels
- **Read**: Retrieve channel history and threads
- **Write**: Send messages to channels and DMs
- **Members**: Access user profiles and information
- **Channels**: List and manage conversations

## Troubleshooting

### Bot can't find channels

Ensure your bot has been added to the channels it needs to access. The bot needs to be a member of channels to read their content.

### OAuth token errors

Verify your token starts with `xoxb-` and hasn't expired. You may need to reinstall the app.

### Permission denied errors

Check that all required scopes are added in **OAuth & Permissions** and the app was reinstalled after adding new scopes.

## Security Notes

- Never commit Slack tokens to version control
- Rotate tokens periodically
- Use workspace-level restrictions if available
- Consider using a dedicated workspace for AI assistants

## References

- [Official Slack MCP Server Docs](https://modelcontextprotocol.io/introduction)
- [Slack API Overview](https://api.slack.com/)
- [MCP Server Package](https://www.npmjs.com/package/@modelcontextprotocol/server-slack)