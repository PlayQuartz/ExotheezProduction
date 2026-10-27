from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 page=browser.new_page(viewport={'width':1920,'height':1080})
 page.goto('http://127.0.0.1:5174/overlays/coupe-de-france-fortnite-2026/leaderboard')
 page.locator('.cdf-row').nth(9).wait_for()
 page.evaluate('document.fonts.ready')
 assert page.evaluate('document.fonts.check(\'700 31px "Microsport Bold"\')')
 assert page.evaluate('Array.from(document.fonts).some(f => f.family === "Microsport Bold" && f.status === "loaded")')
 page.screenshot(path='.design/leaderboard-microsport.png')
 print('PASS: Microsport Bold webfont loaded in browser')
 browser.close()
