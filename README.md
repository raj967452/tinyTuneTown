# Tiny Tune Town — original-content publishing workflow

This project is a **copyright-safe** automation starter for a YouTube music channel. It prepares an original-video brief, upload metadata, and a Digen job handoff from a creator-provided concept.

It deliberately does **not** download, transcribe, imitate, or rewrite material from another channel. In particular, it blocks `youtube.com/@SunriseJungleBeat` as a reference source. Use only original material or media/lyrics for which you hold a licence that permits adaptation and YouTube publishing.

## What it produces

For every approved brief, the workflow creates:

* `out/<slug>/digen-job.json` — a provider-neutral Digen handoff payload for generating an original video;
* `out/<slug>/youtube-metadata.json` — title, description, tags, hashtags, and thumbnail brief;
* `out/<slug>/review-checklist.md` — a required human review checklist.

The payload is intentionally **not submitted automatically**: Digen's public site is a JavaScript application and this repository does not assume an unpublished API. Submit the job through your authorized Digen integration after completing the rights review.

## Quick start

1. Copy the example brief and make it yours:

   ```bash
   cp briefs/example-original-song.json briefs/my-song.json
   ```

2. Replace the concept, lyrics, visual direction, and rights declaration. The lyrics must be your own or licensed for this use.

3. Build the publishing package:

   ```bash
   python3 scripts/prepare_release.py briefs/my-song.json
   ```

4. Review `out/<slug>/review-checklist.md`, generate the video in Digen using `digen-job.json`, then upload manually or through an OAuth-authorized YouTube Data API integration.

## Rights and publishing policy

Before publishing, verify that you own or have written permission for the lyrics, composition, vocals, visuals, samples, and thumbnail assets. Do not use another creator's video, channel, transcript, or lyrics as input for adaptation. Run the checklist and retain licences/permissions outside this repository.

For YouTube publishing, use your own Google OAuth credentials with the least necessary scope, keep tokens outside the repository, and publish only after a human confirms the generated result is original and accurate.

## Tests

```bash
python3 -m unittest discover -s tests -v
```
