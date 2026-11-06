# Hidden Gibbon MTG — Official Website

A professional static GitHub Pages website using **the creator’s original artwork**. No AI-generated imagery is included.

## Publish (one-time)

1. On GitHub, create a **public** repository named `Hidden-Gibbon-MTG-Website` under `TheHiddenGibbonMTG` (do not initialize it with a README).
2. Extract this ZIP. Upload **the contents of `Hidden_Gibbon_Jungle_Website`** (not the enclosing folder) to the new repository. Make sure `.github/workflows/refresh-showcases.yml` is included. GitHub's browser uploader may hide dot-folders; if so upload the workflow using **Add file → Create new file** and name it `.github/workflows/refresh-showcases.yml`, pasting the included text.
3. Go to **Settings → Pages → Build and deployment → Deploy from a branch**, choose `main` and `/ (root)`, then Save.
4. Go to **Actions → Refresh video and deck showcases → Run workflow** for the first refresh. Check the run logs. The schedule runs every six hours after that.
5. In **Settings → Actions → General**, ensure workflows have read/write repository permissions if commits fail. The workflow needs `contents: write` to save the refreshed JSON.

Site URL after deployment: `https://thehiddengibbonmtg.github.io/Hidden-Gibbon-MTG-Website/`

## Automatic content

- **YouTube**: Official channel RSS feed, with yt-dlp public channel-page fallback. The workflow stores the latest 15 videos in `showcase-data.json` and uses real YouTube thumbnail URLs. No API key is needed. Network access is required for the GitHub Actions runner.
- **Moxfield**: A best-effort public API lookup. Moxfield does not guarantee this endpoint or access. If unavailable, the page displays a clean deck-library link rather than pretending placeholder cards are real decks. Add verified individual deck links to `featured-decks.js` if desired.
- The site reads `showcase-data.json` when loaded; GitHub Actions refreshes the file on schedule. Simply opening `index.html` locally does not run the workflow.

## Files

`index.html` — main website; `assets/` — original creator artwork; `featured-decks.js` — optional hand-picked real deck links; `update_showcases.py` — metadata fetcher; `.github/workflows/refresh-showcases.yml` — scheduled refresh.

## Limitations

YouTube and Moxfield may change their public access policies. The update script preserves the last successful data if a later refresh fails. The site itself remains functional. Public deck auto-refresh cannot be guaranteed until tested against Moxfield from GitHub Actions.
