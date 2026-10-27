from psd_tools import PSDImage
p=PSDImage.open(r'D:\Documents\Broadcast Production - Events\61. Coupe de France Fortnite 2026\PSD\Game_Number_16x9.psd')
g=next(l for l in p if l.is_group() and l.visible)
for l in g.descendants():
 if l.kind=='type' and l.text in ('01','10'): l.visible=False
im=g.composite(viewport=(1588,28,1891,105),force=True)
im.save('public/events/coupe-de-france-fortnite-2026/game-number-artwork.png')
print(im.size)
