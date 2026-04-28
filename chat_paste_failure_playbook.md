# Chat Paste Failure Playbook ("Failed to create follow-up")

If long HTML pastes fail in chat, use this sequence:

1. **Reduce payload size**
   - Paste 80–150 lines per message instead of entire file.
2. **Send plain text first**
   - Avoid code fences on first try.
3. **Then switch to fenced blocks**
   - Use ```html only after small chunk succeeds.
4. **Number every message**
   - `Part 1/8`, `Part 2/8`, ...
5. **Wait for delivery before next part**
   - Send next chunk only after prior chunk appears in thread.

---

## Use the helper script in this repo

```bash
scripts/chunk_text.sh "acousticguard_live(4).html" 120
```

This generates `chat_chunks/` files that are easy to paste sequentially.

---

## Alternative (best reliability)
Place the file directly in this workspace and share path. Then no pasting is needed.

Example:
- `/workspace/AcousticGaurd/acousticguard_live(4).html`

Once present, I can review and edit directly.
