from psd_tools import PSDImage
import json
p=PSDImage.open(r'D:\Documents\Broadcast Production - Events\61. Coupe de France Fortnite 2026\PSD\Classement_Top10_16x9.psd')
print('SIZE',p.size)
p.topil().save('.design/reference.png')
def scan(group,depth=0):
 for l in group:
  print(' '*depth, l.kind,repr(l.name),l.bbox,'visible=',l.visible, 'text='+repr(l.text) if l.kind=='type' else '')
  if l.kind=='type':
   print(' '*depth,'FONT',str(l.resource_dict.get('FontSet')), 'ENGINE',str(l.engine_dict.get('StyleRun'))[:1600])
  if l.is_group(): scan(l,depth+2)
scan(p)
