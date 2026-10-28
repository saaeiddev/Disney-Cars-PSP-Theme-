#!/usr/bin/env python3
"""Build indexed GIM images and use LibPSPThemes to assemble a standard PTF."""
import io, json, shutil, struct, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageFilter, ImageChops
ROOT=Path(__file__).resolve().parents[1]
LIB=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/tmp/cars-libptf')
def block(t,size,next):return struct.pack('<HHIII',t,0,size,next,16)
def image_block(t,fmt,order,w,h,bpp,pixels,level):
 b=bytearray(64+len(pixels))
 for off,val in [(0,0x30),(4,fmt),(6,order),(8,w),(10,h),(12,bpp),(14,16),(16,8),(18,2),(40,level),(42,1),(44,3),(46,1)]:struct.pack_into('<H',b,off,val)
 for off,val in [(24,0x30),(28,0x40),(32,64+len(pixels)),(36,0),(48,0x40)]:struct.pack_into('<I',b,off,val)
 b[64:]=pixels;return block(t,16+len(b),16+len(b))+b
def wrap(blocks):
 pic=block(3,16+sum(map(len,blocks)),16)+b''.join(blocks)
 root=block(2,16+len(pic),16)+pic
 return b'MIG.00.1PSP\0\0\0\0\0'+root
def gim(im,indexed=True):
 im=im.convert('RGBA');w,h=im.size
 if not indexed:return wrap([image_block(4,3,0,w,h,32,im.tobytes(),1)])
 q=im.quantize(colors=256,method=Image.Quantize.FASTOCTREE);palette=bytes(q.getpalette('RGBA')); pix=q.tobytes()
 # 16 x 8 swizzled tiles, the PSP P8 layout used by PTF Studio.
 assert w%16==0 and h%8==0
 tiled=bytes(pix[(ty*8+y)*w+(tx*16+x)] for ty in range(h//8) for tx in range(w//16) for y in range(8) for x in range(16))
 return wrap([image_block(5,3,0,256,1,32,palette,2),image_block(4,5,1,w,h,8,tiled,1)])
def glow(im,size):
 mask=im.convert('RGBA').getchannel('A'); canvas=Image.new('L',(size,size));canvas.paste(mask,((size-mask.width)//2,(size-mask.height)//2));
 blur=canvas.filter(ImageFilter.GaussianBlur(3)); alpha=ImageChops.subtract(blur,canvas.point(lambda x:round(x*.75))).point(lambda x:round(x*.8/8)*8)
 out=Image.new('RGBA',(size,size),(255,255,255,0));out.putalpha(alpha);return out

def main():
 if not (LIB/'ptf.py').is_file():sys.exit('Pass path to a LibPSPThemes checkout')
 with tempfile.TemporaryDirectory() as tmp:
  d=Path(tmp)/'Disney_Cars_PSP_Theme';d.mkdir(); categories={str(i):{} for i in range(5)}
  def add(obj,sub,img,indexed=True):
   fname=f'{obj}_{sub:04}.gim';(d/fname).write_bytes(gim(img,indexed));categories[str(obj)][str(sub)]={'file_type':5,'file_name':fname,'file_comp':2}
  wall=Image.open(ROOT/'assets/wallpaper.bmp').convert('RGB');wall.save(d/'1_0000.bmp');categories['1']['0']={'file_type':4,'file_name':'1_0000.bmp','file_comp':2}
  add(0,0,Image.open(ROOT/'assets/preview/icon.png'));add(0,1,Image.open(ROOT/'assets/preview/image.png'),False);categories['0']['2']={'file_type':-1,'file_data':12,'file_length':4,'file_comp':0}
  for sub,name in [(1,'settings'),(2,'photo'),(3,'music'),(4,'video'),(5,'tv'),(6,'game'),(7,'network'),(8,'extras')]:add(2,sub,Image.open(ROOT/f'assets/categories/{name}.png'))
  for sub in range(2,60,2):
   im=Image.open(ROOT/f'assets/first/{sub:02}.png').convert('RGBA'); add(3,sub,im); focus=glow(im,64);focus.save(ROOT/f'assets/first/{sub+1:02}_focus.png'); add(3,sub+1,focus)
  for sub in (0,2):
   im=Image.open(ROOT/f'assets/second/{sub:02}.png').convert('RGBA');add(4,sub,im);focus=glow(im,48);focus.save(ROOT/f'assets/second/{sub+1:02}_focus.png');add(4,sub+1,focus)
  index={'name':'Disney Cars','file_name':'DISNEY_CARS','psp_version':'6.20','version':'1.0','value8':8,'categories':categories}
  (d/'index.json').write_text(json.dumps(index,indent=2));subprocess.run([sys.executable,str(LIB/'ptf.py'),str(d)],check=True)
  out=ROOT/'build/Disney_Cars_PSP_Theme.ptf';shutil.copyfile(str(d)+'.ptf',out);print('Built',out,out.stat().st_size)
if __name__=='__main__':main()
