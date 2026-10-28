from pathlib import Path
from PIL import Image, ImageOps
ROOT=Path(__file__).resolve().parents[1]
def extract(path,cols,rows,index,size):
 im=Image.open(path).convert('RGBA');x=index%cols;y=index//cols
 cell=im.crop((round(x*im.width/cols),round(y*im.height/rows),round((x+1)*im.width/cols),round((y+1)*im.height/rows)))
 alpha=cell.getchannel('A');bbox=alpha.point(lambda a:255 if a>=200 else 0).getbbox()
 if not bbox:raise ValueError((path,index))
 cell=cell.crop(bbox);cell.thumbnail((size-8,size-8),Image.Resampling.LANCZOS)
 out=Image.new('RGBA',(size,size));out.alpha_composite(cell,((size-cell.width)//2,(size-cell.height)//2));return out
for sheet,start in [('first_a.png',2),('first_b.png',20),('first_c.png',38)]:
 for i in range(9):extract(ROOT/'artwork'/sheet,3,3,i,48).save(ROOT/f'assets/first/{start+i*2:02}.png')
for i,sub in enumerate((56,58)):extract(ROOT/'artwork/special_master.png',2,2,i,48).save(ROOT/f'assets/first/{sub:02}.png')
for i,sub in enumerate((0,2)):extract(ROOT/'artwork/special_master.png',2,2,i+2,32).save(ROOT/f'assets/second/{sub:02}.png')
wall=Image.open(ROOT/'assets/wallpaper.bmp').convert('RGB');ImageOps.fit(wall,(300,170),Image.Resampling.LANCZOS).save(ROOT/'assets/preview/image.png')
icon=Image.open(ROOT/'assets/categories/game.png').convert('RGBA');icon.thumbnail((16,16),Image.Resampling.LANCZOS);o=Image.new('RGBA',(16,16));o.alpha_composite(icon,((16-icon.width)//2,(16-icon.height)//2));o.save(ROOT/'assets/preview/icon.png')
