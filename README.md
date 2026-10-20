# Global Shorts Automation

A free-first starter project for creating original, vertical English movie/entertainment Shorts for the existing **Knowledge Review** channel.

## Current status

- [x] Content strategy defined in `CONTENT_STRATEGY.md`.
- [x] Python renderer added for original text-card videos with English narration.
- [x] GitHub Actions workflow added to run daily and on manual request.
- [ ] Research and approve source-backed scripts in `content/queue.json`.
- [ ] Test output quality and fix any workflow issues.
- [ ] Configure YouTube OAuth securely and test a private/unlisted upload.
- [ ] Enable scheduled publishing only after testing, duplicate checks, and upload status tracking.

**Important:** This is the first working foundation, not a completed auto-publisher. The content queue is intentionally empty, so the workflow will not produce a video until approved scripts are added. It does not upload to YouTube yet. Daily 4–6 uploads are a target to test, not a guarantee.

## Run it

1. Add researched items to `content/queue.json`.
2. Each item must include `id`, `title`, `review_status: "approved"`, `source_notes`, and a `scenes` array. Each scene needs a `text` field.
3. Open **Actions → Render approved Shorts → Run workflow** to test it.
4. Download the `rendered-shorts` artifact from the completed workflow run.

Example queue item structure:

```json
{
  "items": [
    {
      "id": "example-001",
      "title": "A movie fact worth checking",
      "review_status": "approved",
      "source_notes": [
        "Official production/interview source: https://example.com/source"
      ],
      "scenes": [
        {"text": "Here is the opening hook."},
        {"text": "Here is the verified context."},
        {"text": "Here is the takeaway."}
      ]
    }
  ]
}
```

The example above is a structure example only; do not publish it as a factual script. Replace the example source with real, checked sources.

## Free services and limits

The workflow uses GitHub Actions on a public repository, Python, FFmpeg, Pillow, and Edge TTS. Free services and unofficial endpoints can change, fail, or impose limits. This project does not promise uninterrupted operation or guaranteed virality. The narration service may be unavailable in some runs.

## Editorial and copyright rules

- Use original commentary and original graphics; do not download or republish movie scenes/trailers or other creators' Shorts as the core video.
- Verify factual claims and record sources before marking a script approved.
- Clearly label interpretations/theories. Never invent quotes, facts, or sources.
- Do not commit API keys, OAuth tokens, passwords, or secrets to this repository.
- Do not automate public uploads until private/unlisted upload testing, duplicate prevention, and failure handling are implemented.

See [CONTENT_STRATEGY.md](CONTENT_STRATEGY.md) for the channel plan. The separate [YouTube agent skills project](https://github.com/Jakeschincariol/chatgpt-youtube-agent-skill) is a writing assistant, not a full automatic publisher.
