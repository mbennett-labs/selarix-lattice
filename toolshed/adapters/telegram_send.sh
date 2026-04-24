#!/usr/bin/env bash
# ==============================================================================
# telegram_send.sh — SELARIX Board Bot send adapter
# ==============================================================================
# Kind: adapter
# Status: active
# What it does: Sends a Markdown-formatted message to the SELARIX Board Telegram
#               channel via the Bot API.
# When to use it: Any agent/script that needs to push a message to Mike's unified
#                 morning feed. Primary consumer: Reporter.
# When not to use it: Do NOT use for per-agent noise (Moltbook engagement, Swarm
#                     Medic, etc.) — those have their own channels (@blocdev_bot).
#                     This channel is reserved for Reporter output.
# Dependencies: curl, jq (for safe JSON escaping)
#               Env vars: SELARIX_BOARD_BOT_TOKEN, SELARIX_BOARD_CHAT_ID
#               Both loaded from /home/selarix/.selarix.env (sourced below).
# Model compatibility: n/a (plumbing, not a model call)
# Last updated: 2026-04-24 by Claude + Mike
# ==============================================================================

set -euo pipefail

# --- Load credentials -----------------------------------------------------
# Expected in /home/selarix/.selarix.env:
#   SELARIX_BOARD_BOT_TOKEN=<bot token from NordPass "SELARIX Board Bot Token">
#   SELARIX_BOARD_CHAT_ID=6712910089
ENV_FILE="${SELARIX_ENV_FILE:-/home/selarix/.selarix.env}"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
else
  echo "ERROR: env file not found at $ENV_FILE" >&2
  exit 2
fi

: "${SELARIX_BOARD_BOT_TOKEN:?SELARIX_BOARD_BOT_TOKEN not set in $ENV_FILE}"
: "${SELARIX_BOARD_CHAT_ID:?SELARIX_BOARD_CHAT_ID not set in $ENV_FILE}"

# --- Read message from stdin or first argument ----------------------------
if [[ $# -ge 1 && "$1" != "-" ]]; then
  MESSAGE="$1"
else
  MESSAGE="$(cat)"
fi

if [[ -z "${MESSAGE// }" ]]; then
  echo "ERROR: empty message, refusing to send" >&2
  exit 3
fi

# --- Telegram message size limit ------------------------------------------
# Telegram caps Bot API sendMessage at 4096 chars. Truncate with a tail note
# rather than fail, so Reporter never goes silent on a long-message edge case.
MAX_LEN=4000  # leave headroom for the truncation notice
if [[ ${#MESSAGE} -gt $MAX_LEN ]]; then
  TAIL_NOTICE=$'\n\n⚠️ _message truncated — full digest in /var/log/selarix/reporter/_'
  MESSAGE="${MESSAGE:0:$MAX_LEN}${TAIL_NOTICE}"
fi

# --- Build payload (jq handles JSON escaping safely) ----------------------
PAYLOAD=$(jq -n \
  --arg chat_id "$SELARIX_BOARD_CHAT_ID" \
  --arg text "$MESSAGE" \
  --arg parse_mode "Markdown" \
  '{chat_id: $chat_id, text: $text, parse_mode: $parse_mode, disable_web_page_preview: true}')

# --- Send -----------------------------------------------------------------
API_URL="https://api.telegram.org/bot${SELARIX_BOARD_BOT_TOKEN}/sendMessage"

HTTP_CODE=$(curl -sS -o /tmp/telegram_send_response.json -w "%{http_code}" \
  -H "Content-Type: application/json" \
  -X POST \
  -d "$PAYLOAD" \
  "$API_URL")

if [[ "$HTTP_CODE" -ne 200 ]]; then
  echo "ERROR: Telegram API returned HTTP $HTTP_CODE" >&2
  cat /tmp/telegram_send_response.json >&2
  exit 4
fi

# Success — log minimal to stdout for cron visibility
MESSAGE_ID=$(jq -r '.result.message_id // "unknown"' /tmp/telegram_send_response.json)
echo "[telegram_send] OK — message_id=$MESSAGE_ID chars=${#MESSAGE}"
