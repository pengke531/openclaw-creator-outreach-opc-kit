# Provider Matrix

This domain pack is designed to degrade gracefully.

## Primary providers

### Apify

Use when:

- you need public Instagram profile verification at scale
- you need follower counts, bio, profile URL, and creator/account metadata
- you want scheduled runs and API-driven batch processing

Recommended env vars:

- `APIFY_TOKEN`
- `APIFY_INSTAGRAM_PROFILE_ACTOR`

Suggested default actor:

- `apify/instagram-profile-scraper`

### Bright Data

Use when:

- Apify is unavailable
- a profile URL is already known and needs a stable re-check

Recommended env vars:

- `BRIGHTDATA_API_KEY`
- `BRIGHTDATA_INSTAGRAM_PROFILE_ENDPOINT`

## Search helpers

These are useful but optional:

- `agent-reach`
- `autoglm-browser-agent`
- `search`
- `tavily`

## Recommended fallback policy

1. Search with optional search skill.
2. Open candidate profile with browser skill when needed.
3. Verify using provider API when available.
4. If provider data and visible profile disagree, trust direct visible profile
   evidence for follower display and geography clues, then note the conflict in
   evidence.

## Non-goals

Do not rely on official Instagram Graph API as the main discovery path for this
workflow. It is better suited to known professional accounts and is not the most
practical foundation for Nepal-wide public creator discovery.
