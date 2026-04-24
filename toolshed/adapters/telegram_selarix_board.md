# Telegram: SELARIX Board Bot
Kind: adapter
Status: active
What it does: Sends messages from Lattice agents to Mike's Telegram as the SELARIX Board channel, and receives replies.
When to use it: Reporter uses this for the morning digest and reply routing. Other agents should NOT use this directly — escalations go through the Coordinator to the Reporter.
When not to use it: Routine status writes go to project status files, NOT Telegram. Telegram is human-facing output only.
Dependencies: Telegram Bot API; bot token in env (NEVER committed)
Model compatibility: all
Last updated: 2026-04-24 by Mike Bennett

---

## Identity
- Bot name: **SELARIX Board**
- Username: `@SelarixBoard_bot`
- Description: SELARIX Board — Mike's Lattice digest channel. Daily morning report. Reply routing.
- Recipient chat ID: `6712910089` (Mike's personal Telegram)
- Token storage: NordPass entry "SELARIX Board Bot Token" AND EC2 env at `$SELARIX_BOARD_BOT_TOKEN`
- Created: 2026-04-24 via @BotFather, token rotated once on day of creation

## How to invoke (send a message)
```bash
curl -sS -X POST \
  "https://api.telegram.org/bot${SELARIX_BOARD_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": 6712910089,
    "text": "SELARIX morning brief — 2026-04-25\n\nNeeds you today: ...",
    "parse_mode": "Markdown",
    "disable_web_page_preview": true
  }'
```

## How to invoke (receive replies — long-poll)
```bash
# Reporter agent polls this on wake to grab fresh replies
curl -sS "https://api.telegram.org/bot${SELARIX_BOARD_BOT_TOKEN}/getUpdates?offset=${LAST_UPDATE_ID}&timeout=5"
```

Replies come back as `message.reply_to_message.message_id` → map to the morning digest's message_id → parse into directive schema (`contract/inbox_schema.json`) → write to the appropriate project's `/inbox/`.

## Reply routing logic (Reporter's job)
- If reply contains `approve <X>` → write directive with `command: "approve"`, `target: X`
- If reply contains `kill <X>` → write directive with `command: "kill"`
- If reply contains `priority <X>` → write directive with `command: "priority"`
- Short text with no command keyword → `command: "note"`
- Ambiguous or multi-intent → Reporter asks for clarification in Telegram, does NOT write a directive

## Known failure modes
- **Rate limit:** Telegram Bot API caps at 30 msgs/sec globally and 1 msg/sec per chat. Morning digest is one message — no issue. Reply polling is cheap — no issue.
- **Bot token leak:** If token appears in chat logs, screenshots, or git, revoke immediately via @BotFather `/revoke` → new token → update NordPass + EC2 env.
- **Markdown parsing errors:** Special chars (`_`, `*`, `[`, `]`, `` ` ``) can break Markdown parse mode. Reporter should escape per Telegram MarkdownV2 spec OR use plain text.

## Adapter code location (when written)
Path: TBD. First use will create a simple curl wrapper in `/toolshed/tools/telegram_send.sh`. Hardened version in `/toolshed/adapters/telegram_client.py` on second use per "wrap on first, harden on second" rule.

## Change log
- 2026-04-24: created. Bot live. Token stored. Awaiting Reporter agent to be written in Phase 2.
