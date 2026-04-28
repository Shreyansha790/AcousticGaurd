# Why chats may not appear in Codex Desktop (and what to do)

## What is happening
If the left sidebar shows **No chats** in the Codex desktop app, it usually means one of these:

1. You are signed into a different OpenAI account/workspace than the one used in the other surface.
2. You are in a different local project context (Codex groups threads under project/folder contexts).
3. Search/filter is hiding threads.
4. Sync has not refreshed yet after sign-in/network reconnect.

## Important limitation
There is no direct "move this live chat session" button from this coding sandbox conversation into your desktop app.

Practical workaround: copy your latest prompt/summary and paste it into a new desktop thread so we can continue there.

## Fast fix checklist (2 minutes)
1. In desktop app, confirm the same account and workspace/org used in the other surface.
2. Open **Search** in the sidebar and search by a unique phrase from our earlier messages (for example: `acousticguard_live(4).html`).
3. Switch to the correct project/folder context in desktop and check Chats again.
4. If still empty, sign out/in once and reopen the app.
5. If needed, start a new thread and paste this handoff block:

```
Project: AcousticGaurd hackathon prototype
Current focus: real AI inference + judge-readable demo narrative
Last file referenced: acousticguard_live(4).html
Immediate request: continue review and edits from current prototype
```

## Why this guidance is reliable
OpenAI's Codex Academy docs describe that:
- conversation history is shown in the left sidebar,
- work is organized by threads,
- and projects are linked to local folders.

So missing chats are usually an account/context/scope mismatch rather than an HTML-file issue.
