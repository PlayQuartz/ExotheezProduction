from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 page=browser.new_page(viewport={'width':1920,'height':1080})
 requests=[]
 wins=[0]
 def api(route):
  requests.append(route.request.url)
  route.fulfill(json={'page':0,'total_pages':1,'teams':[{'sessions':{str(i):{'place':1} for i in range(wins[0])}}]})
 page.route('https://api.wls.gg/**',api)
 base='http://127.0.0.1:5175/overlays/coupe-de-france-fortnite-2026/game-number'
 for count,expected in [(0,'01'),(1,'02'),(4,'05')]:
  wins[0]=count
  page.goto(base+'?id=test-window&totalGames=4')
  page.wait_for_function(f"document.querySelector('.cdf-game-current')?.textContent === '{expected}'")
  assert page.locator('.cdf-game-total').inner_text()=='04'
 assert all('/test-window?' in url for url in requests)
 before=len(requests)
 page.goto(base+'?id=test-window&totalGames=10&forceCurrentGame=4')
 page.evaluate('document.fonts.ready')
 assert page.locator('.cdf-game-current').inner_text()=='04'
 assert len(requests)==before
 box=page.locator('.cdf-game-number').bounding_box()
 assert box['x']==1590 and box['y']==30 and box['width']==300,box
 page.screenshot(path='.design/game-number-browser.png',omit_background=True)
 browser.close()
 print('PASS: automatic wins + 1, window id, padded totals, manual override without API, HUD bounds')
