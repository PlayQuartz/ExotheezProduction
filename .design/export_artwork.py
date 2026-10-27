from psd_tools import PSDImage
from pathlib import Path
p=PSDImage.open(r'D:\Documents\Broadcast Production - Events\61. Coupe de France Fortnite 2026\PSD\Classement_Top10_16x9.psd')
out=Path('public/events/coupe-de-france-fortnite-2026'); out.mkdir(parents=True,exist_ok=True)
# Keep the original flattened artwork and erase only the editable text areas
# using each row's uniform background, preserving all original textures/effects.
im=p.topil().convert('RGB')
from PIL import ImageDraw
draw=ImageDraw.Draw(im)
table=list(p)[2]
for row in list(table)[3:]:
 for layer in row:
  if layer.kind=='type':
   x0,y0,x1,y1=layer.bbox
   color=im.getpixel((1200,(y0+y1)//2))
   draw.rectangle((x0-1,y0-1,x1+1,y1+1),fill=color)
im.save(out/'leaderboard-artwork.png',optimize=True)
print('Exported',im.size)
