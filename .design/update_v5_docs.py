from pathlib import Path
p=Path('README.md'); s=p.read_text(encoding='utf-8').replace('0-0000-897485846540742656','0-0000-888411444641538048').replace('https://www.wls.gg/api/leaderboards/', 'https://api.wls.gg/v5/leaderboards/')
a=s.index('Verified limitation:')
s=s[:a]+'''The v5 endpoint allows cross-origin requests for the tested overlay origin. Live results are fetched directly in the browser, with no backend or proxy. If a request fails, existing results remain on air; before the first successful response, the overlay stays transparent.
'''
p.write_text(s,encoding='utf-8')
p=Path('.design/check_direct_wls.py'); s=p.read_text(encoding='utf-8').replace('0-0000-897485846540742656','0-0000-888411444641538048'); p.write_text(s,encoding='utf-8')
