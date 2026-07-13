#!/usr/bin/env node
/**
 * send-discord.cjs - Marketing kit CLI utility to post a message to Discord.
 *
 * Port of the dropped hooks/notifications/send-discord.sh CLI helper from the legacy toolkit
 * (epic #6 dropped shell hooks; this file restores parity per issue #12).
 *
 * Distinct from kits/core/hooks/notifications/notify.cjs - that one is a
 * hook-event router driven by stdin JSON. This one is a manual CLI helper:
 *
 *   node send-discord.cjs "your message"
 *
 * Behavior:
 *   - Reads DISCORD_WEBHOOK_URL from process.env (env-loader cascade is the
 *     event-driven router's job; this CLI mirrors the original shell helper
 *     and trusts the caller to set the env).
 *   - Posts a rich embed payload via global fetch (Node 18+).
 *   - Notifications never block the pipeline: every failure path exits 0
 *     with a stderr [!] / [X] line; success exits 0 with [OK].
 *
 * Conventions:
 *   - ASCII status markers only ([OK] / [!] / [X]) per design-principles.
 *   - No external deps; uses Node 18+ built-in fetch.
 */
'use strict';

const path = require('node:path');

const PROVIDER = 'discord';
const STOP_COLOR = 5763719; // green, matches the prior shell helper
const MAX_DESCRIPTION_CHARS = 4000; // Discord embed description limit is 4096
const FETCH_TIMEOUT_MS = 10_000;

/**
 * Build the Discord webhook payload (single embed) for a free-text message.
 *
 * @param {string} message - Caller-supplied message body.
 * @param {string} cwd     - Working dir, used as the project name footer.
 * @returns {Object} JSON-serialisable webhook body.
 */
function buildPayload(message, cwd) {
  const projectName = path.basename(cwd || '') || 'unknown';
  const now = new Date();
  let description = String(message);
  if (description.length > MAX_DESCRIPTION_CHARS) {
    description = description.slice(0, MAX_DESCRIPTION_CHARS - 3) + '...';
  }
  return {
    embeds: [
      {
        title: 'Claude Code Session Complete',
        description,
        color: STOP_COLOR,
        timestamp: now.toISOString(),
        footer: { text: `Project Name * ${projectName}` },
        fields: [
          {
            name: 'Session Time',
            value: now.toISOString().slice(11, 19),
            inline: true,
          },
          {
            name: 'Project',
            value: projectName,
            inline: true,
          },
        ],
      },
    ],
  };
}

/**
 * Post the payload to a webhook URL.
 *
 * @param {string} url
 * @param {Object} payload
 * @returns {Promise<{ok: boolean, status: number, error?: string}>}
 */
async function post(url, payload) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    if (!res.ok) {
      let bodySnippet = '';
      try {
        bodySnippet = (await res.text()).slice(0, 200);
      } catch (_e) {
        // ignore body read failure - status code is enough to signal upstream
      }
      return { ok: false, status: res.status, error: bodySnippet };
    }
    return { ok: true, status: res.status };
  } catch (err) {
    return { ok: false, status: 0, error: err && err.message ? err.message : String(err) };
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Main CLI entrypoint. Always exits 0 - notifications must not block.
 */
async function main() {
  const message = process.argv[2];
  const webhook = process.env.DISCORD_WEBHOOK_URL;

  if (!message || !String(message).trim()) {
    process.stderr.write(
      '[!] send-discord: missing message argument. Usage: send-discord.cjs "<message>"\n'
    );
    process.exit(0);
    return;
  }

  if (!webhook) {
    process.stderr.write(
      '[!] send-discord: DISCORD_WEBHOOK_URL not set - notification skipped\n'
    );
    process.exit(0);
    return;
  }

  let payload;
  try {
    payload = buildPayload(message, process.cwd());
  } catch (err) {
    process.stderr.write(`[!] send-discord: failed to build payload: ${err.message}\n`);
    process.exit(0);
    return;
  }

  const result = await post(webhook, payload);
  if (result.ok) {
    process.stdout.write(`[OK] ${PROVIDER}: notification sent\n`);
    process.exit(0);
    return;
  }
  process.stderr.write(
    `[!] ${PROVIDER}: failed (status=${result.status}) ${result.error || ''}\n`
  );
  process.exit(0);
}

main().catch((err) => {
  // Defence in depth - main should never throw, but if it does we still
  // exit 0 with a stderr marker so the caller's pipeline keeps moving.
  process.stderr.write(`[X] send-discord: unexpected error: ${err && err.message}\n`);
  process.exit(0);
});
