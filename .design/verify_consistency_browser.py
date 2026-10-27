from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 page=browser.new_page(viewport={'width':1920,'height':1080})
 def api(route):
  teams=[{'id':str(i),'place':i,'points':100-i,'members':{'a':{'ingame_name':'Team '+str(i)}},'sessions':{'a':{'place':1}} if i in (3,29) else {}} for i in range(1,31)]
  route.fulfill(json={'teams':teams,'page':0,'total_pages':1})
 page.route('https://api.wls.gg/**',api)
 base='http://127.0.0.1:5175/overlays/coupe-de-france-fortnite-2026/popup-leaderboard'
 page.goto(base+'?type=consistency&start=21&stop=30&qualified=25')
 page.locator('.cdf-popup-qualified').wait_for()
 rows=page.locator('.cdf-popup-row')
 assert rows.count()==8
 assert rows.nth(2).locator('.cdf-popup-rank').inner_text()=='23'
 assert rows.nth(2).locator('.cdf-popup-name').inner_text()=='Team 24'
 assert rows.nth(2).evaluate('(el)=>el.style.marginBottom')=='24px'
 assert 'Team 29' not in page.locator('.cdf-popup-name').all_text_contents()
 page.goto(base+'?type=consistency')
 page.locator('.cdf-popup-row').nth(9).wait_for()
 assert page.locator('.cdf-popup-name').nth(2).inner_text()=='Team 4'
 page.goto(base)
 page.locator('.cdf-popup-row').nth(9).wait_for()
 assert page.locator('.cdf-popup-name').nth(2).inner_text()=='Team 3'
 page.goto(base+'?type=consistency&start=21&stop=30&qualified=22')
 page.locator('.cdf-popup-qualified').wait_for()
 assert page.locator('.cdf-popup-qualified').bounding_box()['y'] < page.locator('.cdf-popup-row').first.bounding_box()['y']
 page.goto(base+'?type=consistency&start=11&stop=20&qualified=22')
 page.locator('.cdf-popup-qualified').wait_for()
 assert page.locator('.cdf-popup-qualified').bounding_box()['y'] > page.locator('.cdf-popup-row').last.bounding_box()['y']
 browser.close()
 print('PASS: consistency filtering and ranking, cutoff 25 -> 23, normal mode unchanged')
