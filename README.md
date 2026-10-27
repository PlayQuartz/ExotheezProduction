# Exotheez production overlays

Run `npm install` and `npm run dev`. The root URL is intentionally blank. Open a direct overlay URL to display an overlay.

## vMix

Add each direct overlay URL as a browser source at **1920 x 1080**:

- `/overlays/event-x/leaderboard`
- `/overlays/event-x/game-number`
- `/overlays/event-x/popup-leaderboard`

The same URLs exist for event-y. Generic overlay backgrounds are transparent; placeholder panels have dark backgrounds. The Coupe de France leaderboard uses its full-frame PSD background. All overlays remain visible. Control visibility through vMix scenes. Smaller viewports scale the canvas proportionally from the top left. The Coupe de France full-frame leaderboard instead fills the viewport and stays centered, cropping equally at the top and bottom in wider windows (or at the sides in taller windows). At 1920 x 1080 the complete artwork remains visible.

## Events and designs

Configure events in `src/events.js`. Each event has a data URL, accent and a layout choice for each overlay type. Register future PSD components in the layout registry in `src/overlays/registry.jsx`; these can be moved into individual component folders as designs arrive. Event artwork can live under `public/events/<event-id>/`.

## Data

Sample data is in `public/data/`. Edit JSON while the dev server is running. Each event's overlays poll the same source every two seconds after a request completes, without reloading. They retain the last valid data during failures and stay transparent before the first successful response. Errors go to the browser console, never on air. Separate browser sources are not frame-synchronized.

Data shape:

```json
{"gameNumber": 3, "standings": [{"id": "team-a", "name": "Team A", "points": 84}]}
```

IDs must be unique. Standings sort by descending points, preserving source order for ties. The compact placeholder shows the top five. Scoring rules and pagination will follow the real event requirements.

The Coupe de France event uses WLS directly. Other events use the local sample JSON files. No backend or editor is included.

## Build and host

Run `npm run lint` and `npm run build`. Deploy `dist/` to a static host with page routes rewritten to `index.html`, while assets and JSON files are served normally. `npm run preview` previews the build locally. Deployed scores must be updated at the deployed data source.


## Coupe de France Fortnite 2026

Leaderboard: `/overlays/coupe-de-france-fortnite-2026/leaderboard`.

This full-frame layout preserves the supplied PSD artwork at 1920 x 1080. The background, logo, headings, and footer are raster artwork; ranks, duo names, eliminations and totals are live HTML. This event now reads live WLS results. The JSON file is retained as a sample fixture. Long duo names truncate with an ellipsis.

Microsport Bold is bundled with the event assets and loaded as a webfont for ranks, eliminations and totals; the artwork retains the original PSD lettering. The popup leaderboard uses its supplied PSD artwork with live top-ten standings.

Artwork extraction and browser QA scripts are under `.design/` (Python psd-tools/Pillow and Playwright respectively); they are development utilities and are not required to run the app. Extraction uses the supplied PSD flattened render and clears only the standings text areas, which have uniform row backgrounds.


## Live WLS leaderboard and pagination

Open `/overlays/coupe-de-france-fortnite-2026/leaderboard?id=0-0000-888411444641538048`. Change only `id` to switch leaderboards; omitting it uses the event default. The endpoint is `https://api.wls.gg/v5/leaderboards/<id>?page=<upstream-page>`.

Click the TOTAL column heading for the next ten duos and RANG for the previous ten. Navigation stops at the first/last page. A successful response commits the new page; if the request fails, the previous results stay on air. WLS returns 100 teams per API page, so the adapter selects the appropriate group of ten and requests the next API page when needed. Ranks and ordering come from WLS; player names prefer `ingame_name`, and eliminations sum `sessions[*].kills`. WLS team points are used directly, including any adjustments already reflected by the API. Refresh interval is 15 seconds after requests complete.

The game-number overlay derives the current game from winning WLS sessions across all API pages, plus one. The PSD subtitle is static artwork.

The browser fetches the WLS URL directly. There is no backend or proxy; deploy `dist/` to static hosting. Vite dev/preview are only local frontend tools.

The v5 endpoint allows cross-origin requests for the tested overlay origin. Live results are fetched directly in the browser, with no backend or proxy. If a request fails, existing results remain on air; before the first successful response, the overlay stays transparent.

## Coupe de France game number

Open `/overlays/coupe-de-france-fortnite-2026/game-number?totalGames=10` as a 1920 x 1080 browser source. The overlay preserves the supplied Game_Number_16x9.psd artwork and top-right position on a transparent canvas. Current game is the number of distinct winning matches (`sessions[*].place === 1`) across every WLS API page, plus one. Both numbers display at least two digits. Change `totalGames` in the URL to set the total. Missing, invalid, or non-positive values default to `10`. Larger totals shrink to fit the artwork. Use `id` to select the WLS window, just like the leaderboard. It refreshes every 15 seconds after requests complete and retains the last successful number on errors; before the first response it displays `01`. Add `forceCurrentGame=1` for an immediate manual override that bypasses WLS requests. Invalid overrides are ignored. The inferred game is not capped at the total. The panel is 300px wide (proportional height), 30px from the top and right of the 1920 x 1080 canvas.

Artwork extraction: `.design/export_game_number.py`. Browser verification: `.design/verify_game_number.py` (update its local URL if needed).

Example: `/overlays/coupe-de-france-fortnite-2026/game-number?id=0-0000-888411444641538048&totalGames=10&forceCurrentGame=4` displays `04 / 10`. Remove `forceCurrentGame` to resume automatic counting.

## Coupe de France popup leaderboard

Open `/overlays/coupe-de-france-fortnite-2026/popup-leaderboard?id=0-0000-888411444641538048` as a 1920 x 1080 browser source. The static panel is 300px wide, approximately 491.09px high, 30px from the right and 136.24px from the top. The game-number panel is not included. Control entry and exit with vMix scenes; there are no animations.

The top ten duos follow WLS ranking and show player names and total points. Long names truncate. Every 15 seconds after requests complete, the overlay reads all WLS API pages and counts distinct winning matches. A duo with more recorded sessions than completed winning matches has only its rank, name and points dimmed to 20%. When the win count catches up, the text returns to 100%. This is inferred status from reported results, so updates depend on WLS reporting. Existing standings remain on screen if a refresh fails. Omit `id` to use the event default.

Artwork extraction: `.design/export_popup.py`. Browser verification: `.design/verify_popup.py`.

Popup rank range: add `&start=11&stop=20` to show ranks 11 through 20, inclusive. Defaults to ranks 1?10; omitting `stop` selects ten ranks from `start`. The PSD panel supports at most ten rows, so larger requested ranges are capped at ten. Ranges can cross WLS API pages and retain elimination status.

Popup consistency mode: add `&type=consistency` to remove every team with at least one winning session, then renumber the remaining teams without gaps. `start`/`stop` select these new ranks. `qualified` is reduced by the number of distinct winning teams removed across all API pages (not the number of wins), with a minimum of zero. Example: `?type=consistency&start=21&stop=30&qualified=25` places the divider after rank 23 when two winning teams are excluded. Without this parameter, original WLS ranks are preserved.
`nFull leaderboard consistency mode: `/overlays/coupe-de-france-fortnite-2026/leaderboard?id=888411444641538048&type=consistency`. Fetches all WLS pages, removes winning teams, renumbers ranks, then paginates the remaining teams in groups of ten. Existing heading controls navigate these filtered pages. Omitting `type=consistency` keeps normal WLS rankings.
