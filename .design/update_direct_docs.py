from pathlib import Path
p=Path('README.md'); s=p.read_text(encoding='utf-8')
s=s.replace('The live data source is still to be chosen; no backend or editor is included yet. A future API or Sheets adapter should return this same shape. Keep credentials on a backend, not in the browser app.', 'The Coupe de France event uses WLS directly. Other events use the local sample JSON files. No backend or editor is included.')
a=s.index('The same-origin proxy runs automatically')
s=s[:a]+'''The browser fetches the WLS URL directly. There is no backend or proxy; deploy `dist/` to static hosting. Vite dev/preview are only local frontend tools.

Verified limitation: WLS currently returns no Access-Control-Allow-Origin header for the tested overlay origin, so standard browsers block this direct request with CORS. WLS must allow the deployed overlay origin for live data to load in a standard browser. Until the first valid response, the overlay remains transparent; failed updates retain any previously loaded data.
'''
p.write_text(s,encoding='utf-8')
# Remove obsolete proxy-specific development scripts.
for name in ['verify_wls_production.py','update_wls_docs.py']:
 p=Path('.design')/name
 if p.exists(): p.unlink()
p=Path('.design/verify_wls.py'); s=p.read_text(encoding='utf-8'); s=s.replace("'/api/wls/'", "'https://www.wls.gg/api/leaderboards/'"); p.write_text(s,encoding='utf-8')
