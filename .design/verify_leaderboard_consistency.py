from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 page=browser.new_page(viewport={'width':1920,'height':1080})
 fail=[False]
 def api(route):
  if fail[0]:route.fulfill(status=503,body='error');return
  n=int(route.request.url.split('page=')[1])
  teams=[{'id':str(i),'place':i,'points':200-i,'members':{'a':{'ingame_name':'Team '+str(i)}},'sessions':{'win':{'place':1}} if i in (3,102) else {}} for i in range(n*100+1,min((n+1)*100+1,106))]
  route.fulfill(json={'page':n,'total_pages':2,'teams':teams})
 page.route('https://api.wls.gg/**',api)
 base='http://127.0.0.1:5175/overlays/coupe-de-france-fortnite-2026/leaderboard'
 page.goto(base+'?type=consistency&id=test')
 page.wait_for_function("document.querySelectorAll('.cdf-duo')[2]?.textContent==='Team 4'")
 assert page.locator('.cdf-rank').nth(2).inner_text()=='03'
 for i in range(1,11):
  page.locator('.cdf-next').click()
  page.wait_for_function(f"document.querySelector('.cdf-rank')?.textContent==='{i*10+1:02}'")
 assert page.locator('.cdf-row').count()==3
 assert page.locator('.cdf-duo').all_text_contents()==['Team 103','Team 104','Team 105']
 assert page.locator('.cdf-next').is_disabled()
 page.locator('.cdf-previous').click()
 page.wait_for_function("document.querySelector('.cdf-rank')?.textContent==='91'")
 fail[0]=True
 page.locator('.cdf-previous').click()
 page.wait_for_timeout(200)
 assert page.locator('.cdf-rank').first.inner_text()=='91'
 browser.close()
 print('PASS: consistency removal, contiguous ranks, pagination across API pages, final page, outage retention')
