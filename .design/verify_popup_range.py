from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 page=browser.new_page(viewport={'width':1920,'height':1080})
 def api(route):
  n=int(route.request.url.split('page=')[1])
  teams=[{'id':str(i),'place':i,'points':300-i,'members':{'a':{'ingame_name':'Player '+str(i)}},'sessions':{}} for i in range(n*100+1,(n+1)*100+1)]
  route.fulfill(json={'page':n,'total_pages':2,'teams':teams})
 page.route('https://api.wls.gg/**',api)
 base='http://127.0.0.1:5175/overlays/coupe-de-france-fortnite-2026/popup-leaderboard'
 for query,expected in [('?start=11&stop=20',range(11,21)),('?start=96&stop=105',range(96,106)),('?start=15&stop=18',range(15,19)),('',range(1,11))]:
  page.goto(base+query)
  page.locator('.cdf-popup-row').first.wait_for()
  assert page.locator('.cdf-popup-rank').all_text_contents()==[str(i).zfill(2) for i in expected]
 page.goto(base+'?start=21&stop=30&qualified=25')
 page.locator('.cdf-popup-qualified').wait_for()
 assert page.locator('.cdf-popup-qualified').inner_text()=='TEAM QUALIFI' + chr(201)
 rows=page.locator('.cdf-popup-row')
 assert rows.nth(4).locator('.cdf-popup-rank').inner_text()=='25'
 assert rows.nth(5).locator('.cdf-popup-rank').inner_text()=='26'
 assert rows.nth(5).bounding_box()['y']-rows.nth(4).bounding_box()['y']>67
 page.evaluate('document.fonts.ready')
 page.screenshot(path='.design/popup-qualified-browser.png',omit_background=True)
 page.goto(base+'?start=11&stop=20&qualified=25')
 page.locator('.cdf-popup-row').first.wait_for()
 assert page.locator('.cdf-popup-qualified').count()==0
 browser.close()
 print('PASS: ranks 11-20, cross-API-page range, shorter range, default 1-10')
