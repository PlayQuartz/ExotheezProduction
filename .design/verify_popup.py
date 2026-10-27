from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 page=browser.new_page(viewport={'width':1920,'height':1080})
 page.clock.install()
 wins=[2]
 failed=[False]
 urls=[]
 def api(route):
  urls.append(route.request.url)
  if failed[0]:
   route.fulfill(status=503,body='unavailable');return
  api_page=int(route.request.url.split('page=')[1])
  if api_page==0:
   teams=[{'id':str(i),'place':i+1,'points':225-i*5,'members':{'a':{'ingame_name':'Player Name '+str(i)}},'sessions':{str(j):{'place':2} for j in range(3 if i==2 else 2)}} for i in range(10)]
  else:
   teams=[{'id':'winner','place':11,'points':0,'sessions':{str(j):{'place':1} for j in range(wins[0])}}]
  route.fulfill(json={'teams':teams,'page':api_page,'total_pages':2})
 page.route('https://api.wls.gg/**',api)
 page.goto('http://127.0.0.1:5175/overlays/coupe-de-france-fortnite-2026/popup-leaderboard?id=popup-window')
 page.locator('.cdf-popup-row').nth(9).wait_for()
 assert page.locator('.cdf-popup-row.is-dead').count()==1
 assert page.locator('.cdf-popup-row').nth(2).locator('span').evaluate_all('(els)=>els.every(el=>getComputedStyle(el).opacity==="0.2")')
 assert page.locator('.cdf-game-number').count()==0
 box=page.locator('.cdf-popup').bounding_box()
 assert box['width']==300 and box['x']==1590 and abs(box['y']-136.24)<.02,box
 page.evaluate('document.fonts.ready')
 page.screenshot(path='.design/popup-browser.png',omit_background=True)
 wins[0]=3
 page.clock.fast_forward(16000)
 page.wait_for_function('document.querySelectorAll(".cdf-popup-row.is-dead").length===0')
 failed[0]=True
 page.clock.fast_forward(16000)
 assert page.locator('.cdf-popup-row').count()==10
 assert all('/popup-window?' in url for url in urls)
 browser.close()
 print('PASS: top ten, all pages, 20% eliminated text, restored after win, outage retention, window id, bounds, no game panel')
