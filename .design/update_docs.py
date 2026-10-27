from pathlib import Path
p=Path('src/App.jsx'); s=p.read_text(encoding='utf-8')
s=s.replace('These layouts use sample data and will be replaced with your PSD designs.', 'Layouts use sample data. The Coupe de France leaderboard uses your PSD artwork; other layouts are placeholders.')
a=s.index('<p>1920'); b=s.index('</p>',a)
s=s[:a]+'<p>1920 x 1080 / Event-specific layouts'+s[b:]
s=s.replace('{label} ?', '{label} / Open')
a=s.index('<footer>'); b=s.index('</footer>',a)
s=s[:a]+'<footer>Sample data / Polls every 2 seconds / Control visibility in vMix'+s[b:]
p.write_text(s,encoding='utf-8')
p=Path('README.md'); s=p.read_text(encoding='utf-8'); a=s.index('**1920'); b=s.index('**',a+2); s=s[:a]+'**1920 x 1080'+s[b:]
s+='''

## Coupe de France Fortnite 2026

Leaderboard: `/overlays/coupe-de-france-fortnite-2026/leaderboard`.

This full-frame layout preserves the supplied PSD artwork at 1920 x 1080. The background, logo, headings, and footer are raster artwork; ranks, duo names, eliminations and totals are live HTML. Scores are illustrative sample values, not event results. Edit `public/data/coupe-de-france-fortnite-2026.json` for now; optional `eliminations` must be a nonnegative integer. The top ten are selected by total points; ties preserve source order. Long duo names truncate with an ellipsis.

Microsport Bold is pending from the user. Ranks and scores currently use a fallback font; the artwork retains the original PSD lettering. Other overlay types for this event still use the generic placeholders.

Artwork extraction and browser QA scripts are under `.design/` (Python psd-tools/Pillow and Playwright respectively); they are development utilities and are not required to run the app. Extraction uses the supplied PSD flattened render and clears only the standings text areas, which have uniform row backgrounds.
'''
p.write_text(s,encoding='utf-8')
