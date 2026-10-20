# Global Shorts Automation

A free-first starter project for creating original, vertical English movie/entertainment Shorts for the existing **Knowledge Review** channel (@knowledgereview8309).

## Current status

- [x] Content strategy defined in `CONTENT_STRATEGY.md`.
- [x] Python renderer added for original text-card videos with English narration.
- [x] GitHub Actions workflow added to render daily and on manual request.
- [x] Five initial source-noted Jurassic Park scripts are in `content/queue.json`.
- [ ] Run the workflow and inspect the generated MP4s; the workflow has not yet been confirmed successful.
- [ ] Configure YouTube OAuth securely and test an unlisted upload.
- [ ] Add an upload ledger, retry/error reporting, and duplicate protection before enabling scheduled public publishing.
- [ ] Expand the approved queue with researched scripts across different films/topics.

**Important:** This repository currently renders videos; it does **not** upload or publish to YouTube. Five queued scripts are a starter batch, not a promise of 4–6 new videos every day. The scheduled render currently re-renders approved queue items; it does not create fresh researched scripts automatically. No public uploads have started.

## Run it

1. Open **Actions → Render approved Shorts → Run workflow**.
2. Wait for the run to finish.
3. Open the run and download the `rendered-shorts` artifact.
4. Review narration, wording, pacing, spelling, factual accuracy, and visual quality before publishing.

The renderer reads `content/queue.json`. Each item needs `id`, `title`, `review_status: "approved"`, `source_notes`, and a `scenes` array; each scene needs a `text` field. Items not marked approved are skipped.

## Free services and limits

The workflow uses GitHub Actions on a public repository, Python, FFmpeg, Pillow, and Edge TTS. Free services and unofficial endpoints can change, fail, or impose limits. Edge TTS relies on an online service and is not guaranteed to be continuously available. This project does not promise uninterrupted operation or guaranteed virality.

## Editorial and copyright rules

- Use original commentary and original graphics; do not download or republish movie scenes, trailers, posters, or other creators' Shorts as the core video.
- Verify factual claims and record sources before marking a script approved.
- Clearly label interpretations/theories. Never invent quotes, facts, or sources.
- Do not commit API keys, OAuth tokens, passwords, or secrets to this repository.
- Do not automate public uploads until the channel owner authorizes YouTube access, an unlisted test succeeds, duplicate prevention and failure handling are implemented, and every video is reviewed for accuracy and rights.

See [CONTENT_STRATEGY.md](CONTENT_STRATEGY.md) for the channel plan. The separate [YouTube agent skills project](https://github.com/Jakeschincariol/chatgpt-youtube-agent-skill) is a writing assistant, not a full automatic publisher.
