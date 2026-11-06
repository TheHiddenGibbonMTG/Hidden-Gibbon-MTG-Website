HIDDEN GIBBON JUNGLE WEBSITE — AUTOMATIC SHOWCASES

This package preserves your supplied original artwork and website layout.
No AI-generated images are used.

PUBLISHING ON GITHUB PAGES
1. Create a new public GitHub repository for the website (or use a separate
   website folder/repository), and upload ALL the contents of this folder,
   including the hidden .github folder, to the root of its main branch.
2. In repository Settings > Pages, choose Deploy from a branch, main, /(root).
3. In repository Settings > Actions > General, ensure workflow permissions
   allow Read and write permissions, so refreshes can commit JSON updates.
4. Open Actions > Refresh video and deck showcases > Run workflow once.
5. Wait for the workflow and Pages deployment to finish; open the Pages URL.

AUTOMATIC UPDATES
The GitHub Action checks public YouTube uploads every six hours and writes
showcase-data.json. Visitors see real thumbnails and titles, without a
third-party RSS converter or a YouTube API key. GitHub's schedule is best
-effort and may run late. Updates require the site to be hosted and the
workflow to run; opening index.html locally does not run GitHub Actions.

MOXFIELD LIMITATION
Moxfield does not provide a guaranteed, documented public profile feed for
this purpose. The updater attempts a public endpoint and uses real deck
metadata only if available. If blocked or changed, it retains prior data.
You can add verified individual deck URLs to featured-decks.js manually;
these remain visible even when automated discovery is unavailable.
No invented deck links or artwork are used.

GitHub software releases and apps are unchanged.
