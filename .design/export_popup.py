from psd_tools import PSDImage
p=PSDImage.open(r'D:\Documents\Broadcast Production - Events\61. Coupe de France Fortnite 2026\PSD\PopUp_Leaderboard.psd')
g=next(l for l in p if l.is_group() and l.bbox==(1588,134,1891,630))
for l in g.descendants():
 if l.kind=='type' and l.text not in ('RANG','DUO','TOTAL'):l.visible=False
g.composite(viewport=(1588,134,1891,630),force=True).save('public/events/coupe-de-france-fortnite-2026/popup-leaderboard-artwork.png')
for l in g.descendants():
 if l.kind=='shape' and l.bbox in ((1591,185,1891,232),(1588,185,1596,232)):l.visible=False
g.composite(viewport=(1588,134,1891,630),force=True).save('public/events/coupe-de-france-fortnite-2026/popup-leaderboard-plain-artwork.png')
