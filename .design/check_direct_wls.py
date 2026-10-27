from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 page=browser.new_page(viewport={'width':1920,'height':1080})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:5174/overlays/coupe-de-france-fortnite-2026/leaderboard?id=0-0000-888411444641538048')
 page.locator('.cdf-row').nth(9).wait_for(timeout=20000)
 assert page.locator('.cdf-total').first.inner_text()=='276'
 assert ' - ' in page.locator('.cdf-duo').first.inner_text()
 for rank in ['11','21','31']:
  page.get_by_role('button',name='Next leaderboard page').click()
  page.wait_for_function('(rank)=>document.querySelector(".cdf-rank")?.textContent===rank',arg=rank)
 assert page.locator('.cdf-row').count()==3
 assert page.get_by_role('button',name='Next leaderboard page').is_disabled()
 page.get_by_role('button',name='Previous leaderboard page').click()
 page.wait_for_function('document.querySelector(".cdf-rank")?.textContent==="21"')
 assert not errors,errors
 print('PASS: direct v5 browser request, live names and totals, dash separators, next/previous, final partial page')
 browser.close()
