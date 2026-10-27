from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(channel='chrome',headless=True)
 page=b.new_page()
 page.route('https://api.wls.gg/**',lambda r:r.fulfill(status=503,body='Unavailable'))
 page.goto('http://127.0.0.1:5174/overlays/coupe-de-france-fortnite-2026/leaderboard')
 page.locator('.cdf-row').nth(9).wait_for()
 assert page.locator('.cdf-rank').all_text_contents()==[str(i).zfill(2) for i in range(1,11)]
 assert page.locator('.cdf-duo').all_text_contents()==['Player Name']*10
 assert page.locator('.cdf-eliminations').all_text_contents()==['0']*10
 assert page.locator('.cdf-total').all_text_contents()==['0']*10
 page.unroute('https://api.wls.gg/**')
 page.route('https://api.wls.gg/**',lambda r:r.fulfill(json={'teams':[],'page':0,'total_pages':1}))
 page.reload()
 page.locator('.cdf-row').nth(9).wait_for()
 assert page.locator('.cdf-duo').all_text_contents()==['Player Name']*10
 print('PASS: unavailable and empty API show 10 placeholder rows with zero scores')
 b.close()
