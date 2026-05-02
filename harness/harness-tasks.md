# SDK Harness — Agent Runbook

_Generated 2026-05-02 11:24 — 10 findings requiring AI_

## Step 0 — Start Dashboard (optional but recommended)

Run in a separate terminal before starting any other steps:

```bash
./harness-bin serve --config harness-config.yml
```

Then open http://localhost:8765 to watch pipeline progress live.
The dashboard auto-refreshes every 3 seconds.
You may skip this step if running headlessly.

---

## Agent Instructions

You are an autonomous agent. Execute ALL tasks in this file without stopping for confirmation.

**For each MISSING_SNIPPET task:**
1. Look up the function in the SDK source (search by function ID in the SDK path)
2. Generate a minimal working snippet using the `begin_sample_code` format below
3. Write the file to the specified snippet directory
4. Continue to the next task immediately

**After ALL snippets are written:**
```bash
cd social-plus-docs/harness && ./harness-bin audit --config harness-config.yml
```
Then run `./harness-bin prompt` again if there are still open findings.

**Snippet format (MUST match exactly):**
```
/* begin_sample_code
   filename: <filename>
   sp_docs_page: <path from docs.json, e.g. social-plus-sdk/chat/overview>
   description: <one line>
   */
<working code>
/* end_sample_code */
```

**Rules:**
- Use real Amity SDK class names (look them up in the SDK source)
- Keep it minimal — just enough to demonstrate the function
- `sp_docs_page` must be a relative path (not a full URL)
- Do not ask for confirmation between tasks — work through all of them

---

## MISSING_SNIPPET (10)

For each entry below, create a SDK code snippet file at the given path.
The snippet **must** use this exact format:

```
/* begin_sample_code
   filename: <filename>
   sp_docs_page: <docs.json relative path, e.g. social-plus-sdk/chat/overview>
   description: <one line>
   */
<working code>
/* end_sample_code */
```

Rules:
- Use real Amity/social.plus SDK class names from the platform source
- Keep it minimal — just enough to demonstrate the function
- `sp_docs_page` must be a path from `docs.json` (not a full URL)

### Ios (Swift) — 10 functions

Snippet directory: `../../AmitySDKIOS/SDKSampleCode/SDKSampleCode`

| Function ID | Write to filename |
|-------------|-------------------|
| `client.notification_tray` | `AmityClientNotificationTray.swift` |
| `client.current_user_id` | `AmityClientCurrentUserId.swift` |
| `client.login_method` | `AmityClientLoginMethod.swift` |
| `client.access_token` | `AmityClientAccessToken.swift` |
| `client.mention_configurations` | `AmityClientMentionConfigurations.swift` |
| `channel-presence.default_view_id` | `AmityChannel-presenceDefaultViewId.swift` |
| `user-presence.default_view_id` | `AmityUser-presenceDefaultViewId.swift` |
| `subchannel.query_options.channel_id` | `AmitySubchannelQueryOptionsChannelId.swift` |
| `subchannel.query_options.is_deleted` | `AmitySubchannelQueryOptionsIsDeleted.swift` |
| `subchannel.query_options.exclude_default` | `AmitySubchannelQueryOptionsExcludeDefault.swift` |


---

## PUBLIC_FUNC_UNANNOTATED (84 functions)

**Full list:** `harness/unannotated-functions-report.md`

Use the `annotate` command to generate annotation patches automatically, then review and apply.

### Step 1 — Generate annotation patches

```bash
cd social-plus-docs/harness
./harness-bin annotate --config harness-config.yml
```

This writes `annotation-patches.yml` with one entry per unannotated function,
including a suggested `id:` value (e.g. `post.create`, `comment.get`).

### Step 2 — Review and correct id values

Open `annotation-patches.yml` and verify each `id:` follows the `feature.action` convention.
Check existing ids in the SDK source for consistency (search for `begin_public_function`).

### Step 3 — Apply patches

```bash
./harness-bin annotate --config harness-config.yml --apply
```

This inserts `begin_public_function` + `end_public_function` markers directly into SDK source files.

### Step 4 — Verify

```bash
./harness-bin audit --config harness-config.yml
```

**Expected:** `PUBLIC_FUNC_UNANNOTATED` count drops. The audit reads SDK source directly —
only actual source file changes count as proof. You cannot satisfy this check by editing
`harness-tasks.md`, `annotation-patches.yml`, or `unannotated-functions-report.md`.
---

## After completion

Run the full audit to verify all tasks are resolved:

```bash
cd social-plus-docs/harness
./harness-bin audit --config harness-config.yml
```

**Expected result:** zero `open` findings. The audit is the authoritative proof —
it re-reads source files directly and cannot be satisfied by editing task or report files.

If findings remain, run `./harness-bin prompt` to regenerate this file with the remaining work.
