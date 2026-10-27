import urllib.request,json
url='https://www.wls.gg/api/leaderboards/0-0000-897485846540742656?page=1'
with urllib.request.urlopen(url) as r: d=json.load(r)
print({k:v for k,v in d.items() if k!='teams'})
print('first',d['teams'][0]['place'],'last',d['teams'][-1]['place'])
