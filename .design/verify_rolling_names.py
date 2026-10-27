from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 page=browser.new_page(viewport={'width':1920,'height':1080})
 payload={'page':0,'total_pages':1,'teams':[{'id':str(i),'place':i+1,'points':100,'members':{'a':{'ingame_name':name}},'sessions':{}} for i,name in enumerate(['Short','Long player name one - Another very long player name'])]}
 page.route('https://api.wls.gg/**',lambda route:route.fulfill(json=payload))
 base='http://127.0.0.1:5175/overlays/coupe-de-france-fortnite-2026/popup-leaderboard'
 page.goto(base)
 page.locator('.is-rolling').wait_for()
 assert page.locator('.is-rolling').count()==1
 track=page.locator('.is-rolling .cdf-popup-name-track')
 assert track.evaluate('(el)=>getComputedStyle(el).animationName')=='cdf-name-roll'
 track.evaluate('(el)=>el.getAnimations()[0].currentTime=5000')
 assert track.evaluate('(el)=>getComputedStyle(el).transform')!='matrix(1, 0, 0, 1, 0, 0)'
 page.goto(base+'?rollNames=0')
 page.locator('.cdf-popup-row').nth(1).wait_for()
 assert page.locator('.is-rolling').count()==0
 browser.close()
 print('PASS: only long names roll, animation moves, static option')
