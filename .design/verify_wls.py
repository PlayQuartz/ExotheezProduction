from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 page=browser.new_page(viewport={'width':1920,'height':1080})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 requests=[]
 page.on('request',lambda r:requests.append(r.url) if 'https://www.wls.gg/api/leaderboards/' in r.url else None)
 page.goto('http://127.0.0.1:5174/overlays/coupe-de-france-fortnite-2026/leaderboard?id=0-0000-897485846540742656')
 page.locator('.cdf-row').nth(9).wait_for(timeout=30000)
 assert page.locator('.cdf-rank').first.inner_text()=='01'
 assert page.locator('.cdf-total').first.inner_text()=='479'
 assert page.locator('.cdf-duo').first.inner_text()!='JOUEUR / JOUEUR'
 assert page.get_by_role('button',name='Previous leaderboard page').is_disabled()
 page.get_by_role('button',name='Next leaderboard page').click()
 page.wait_for_function("document.querySelector('.cdf-rank')?.textContent === '11'")
 page.get_by_role('button',name='Previous leaderboard page').click()
 page.wait_for_function("document.querySelector('.cdf-rank')?.textContent === '01'")
 for rank in range(11,102,10):
  page.get_by_role('button',name='Next leaderboard page').click()
  page.wait_for_function('(rank) => Number(document.querySelector(".cdf-rank")?.textContent) === rank',arg=rank)
 assert any('page=1' in url for url in requests)
 page.evaluate('document.fonts.ready')
 page.screenshot(path='.design/leaderboard-live-page-11.png')
 assert not errors,errors
 # The id parameter must change the actual upstream request.
 page.goto('http://127.0.0.1:5174/overlays/coupe-de-france-fortnite-2026/leaderboard?id=test-other-id')
 page.wait_for_timeout(500)
 assert any('/test-other-id?page=0' in url for url in requests)
 print('PASS: live API names/scores, next and previous, ranks 101+ across upstream page boundary, id override, no browser errors')
 browser.close()
