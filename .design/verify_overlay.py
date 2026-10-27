from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 page=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
 errors=[]
 page.on('pageerror',lambda e: errors.append(str(e)))
 url='http://127.0.0.1:5174/overlays/coupe-de-france-fortnite-2026/leaderboard'
 page.goto(url)
 page.locator('.cdf-row').nth(9).wait_for()
 page.screenshot(path='.design/leaderboard-browser.png',omit_background=True)
 assert page.locator('.cdf-row').count()==10
 assert page.locator('.cdf-total').first.inner_text()=='180'
 # Simulate a valid live update including a long name, then a data outage.
 data={'gameNumber':2,'standings':[{'id':'updated','name':'VERY LONG PLAYER NAME / ANOTHER LONG PLAYER NAME '*4,'eliminations':0,'points':999}]}
 page.route('**/data/coupe-de-france-fortnite-2026.json',lambda route: route.fulfill(json=data))
 page.wait_for_function("document.querySelector('.cdf-total')?.textContent === '999'")
 assert page.locator('.cdf-eliminations').first.inner_text()=='0'
 assert page.locator('.cdf-duo').evaluate('(el) => el.scrollWidth > el.clientWidth')
 page.unroute('**/data/coupe-de-france-fortnite-2026.json')
 page.route('**/data/coupe-de-france-fortnite-2026.json',lambda route: route.fulfill(status=503,body='Unavailable'))
 page.wait_for_timeout(2500)
 assert page.locator('.cdf-total').first.inner_text()=='999'
 page.set_viewport_size({'width':1280,'height':720})
 assert page.locator('.canvas').evaluate('(el) => Math.round(el.getBoundingClientRect().width)')==1280
 page.goto('http://127.0.0.1:5174/')
 assert page.locator('a[href="/overlays/coupe-de-france-fortnite-2026/leaderboard"]').count()==1
 assert not errors,errors
 print('PASS: 10 rows, sample scores, live updates, zero eliminations, long-name clipping, outage retention, scaling, directory link, no browser errors')
 browser.close()
