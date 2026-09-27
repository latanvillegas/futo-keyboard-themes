from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import urllib.request, zipfile, shutil, math, random

ROOT=Path(__file__).resolve().parents[1]; BUILD=ROOT/'build'; DIST=ROOT/'dist'; DIST.mkdir(exist_ok=True)
THEMES=[
 dict(slug='luxury-ivory',name='Luxury Ivory',accent='#A47745',bg='#F3EBDD',fg='#241B14',font='PlayfairDisplay.ttf',fonturl='https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf',ofl='playfairdisplay',style='ivory'),
 dict(slug='neo-tokyo-2026',name='Neo Tokyo 2026',accent='#FF315C',bg='#07080D',fg='#F7F8FF',font='ZenKakuGothicNew-Regular.ttf',fonturl='https://raw.githubusercontent.com/google/fonts/main/ofl/zenkakugothicnew/ZenKakuGothicNew-Regular.ttf',ofl='zenkakugothicnew',style='tokyo'),
 dict(slug='botanical-atelier',name='Botanical Atelier',accent='#6E8B61',bg='#F0EBDD',fg='#243026',font='CormorantInfant-Regular.ttf',fonturl='https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantinfant/CormorantInfant%5Bwght%5D.ttf',ofl='cormorantinfant',style='botanical'),
 dict(slug='liquid-titanium',name='Liquid Titanium',accent='#A7C3D4',bg='#090B0D',fg='#F2F7FA',font='Manrope.ttf',fonturl='https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/Manrope%5Bwght%5D.ttf',ofl='manrope',style='titanium'),
 dict(slug='candy-y2k',name='Candy Y2K',accent='#FF74C8',bg='#241536',fg='#FFF5FC',font='DynaPuff.ttf',fonturl='https://raw.githubusercontent.com/google/fonts/main/ofl/dynapuff/DynaPuff%5Bwdth,wght%5D.ttf',ofl='dynapuff',style='candy')]

def hx(s): s=s.lstrip('#'); return tuple(int(s[i:i+2],16) for i in (0,2,4))
def blend(a,b,t): return tuple(round(a[i]*(1-t)+b[i]*t) for i in range(3))
def bgimg(t,out):
 W,H=1440,900; b=hx(t['bg']); a=hx(t['accent']); im=Image.new('RGB',(W,H),b); ov=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(ov)
 if t['style']=='ivory':
  for x in range(0,W,90): d.line((x,0,x+350,H),fill=(*a,12),width=2)
  d.rectangle((85,70,92,H-70),fill=(*a,125)); d.rectangle((110,70,113,H-70),fill=(80,55,35,60))
 elif t['style']=='tokyo':
  for x in range(0,W,120): d.line((x,0,x,H),fill=(*a,18),width=2)
  for y in range(0,H,90): d.line((0,y,W,y),fill=(65,190,255,15),width=2)
  d.ellipse((930,100,1320,490),fill=(*a,75)); d.line((0,690,W,420),fill=(60,205,255,80),width=5)
 elif t['style']=='botanical':
  for cx,cy,r in [(180,180,120),(1180,670,180),(900,180,90)]:
   d.arc((cx-r,cy-r,cx+r,cy+r),200,520,fill=(*a,95),width=8); d.line((cx,cy,cx+r//2,cy+r),fill=(*a,70),width=5)
 elif t['style']=='titanium':
  for x,y,r,c in [(260,230,250,(110,145,165)),(1120,580,330,(180,200,210)),(800,50,180,(90,120,145))]: d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,42))
  ov=ov.filter(ImageFilter.GaussianBlur(45)); d=ImageDraw.Draw(ov); d.arc((130,80,1320,850),190,345,fill=(*a,80),width=8)
 else:
  cols=[(255,116,200),(113,221,255),(255,225,95),(184,128,255)]
  random.seed(2026)
  for _ in range(28):
   x=random.randrange(W);y=random.randrange(H);r=random.randrange(18,70);c=random.choice(cols);d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,45),outline=(*c,95),width=3)
 Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB').save(out/'background.webp','WEBP',quality=94,method=6)

def border(out,name,fill,outline,style):
 w,h,s=128,140,4; im=Image.new('RGBA',(w*s,h*s),(0,0,0,0));d=ImageDraw.Draw(im); box=(7*s,7*s,(w-7)*s,(h-7)*s); rad={'tokyo':7,'titanium':22,'candy':30}.get(style,16)*s
 d.rounded_rectangle(box,rad,fill=fill,outline=outline,width=2*s)
 if style in ('titanium','candy'): d.line((22*s,18*s,(w-22)*s,18*s),fill=(255,255,255,100),width=2*s)
 im.resize((w,h),Image.Resampling.LANCZOS).save(out/name)

def build(t):
 out=BUILD/t['slug']; shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True); a=hx(t['accent']); b=hx(t['bg']); light=sum(b)>450
 bgimg(t,out)
 normal=blend(b,a,.08 if not light else .04); functional=blend(b,a,.17); action=blend(b,a,.52); pressed=blend(b,a,.68); popup=blend(b,a,.28)
 for n,c in [('normal.png',normal),('functional.png',functional),('action.png',action),('pressed.png',pressed),('popup.png',popup)]: border(out,n,(*c,248),(*a,245),t['style'])
 urllib.request.urlretrieve(t['fonturl'],out/t['font']); urllib.request.urlretrieve(f"https://raw.githubusercontent.com/google/fonts/main/ofl/{t['ofl']}/OFL.txt",out/f"OFL-{t['ofl']}.txt")
 fg=t['fg']; accent=t['accent']; kc='#%02X%02X%02X'%normal; kv='#%02X%02X%02X'%functional; kp='#%02X%02X%02X'%pressed
 lines=['# FUTO Keyboard Theme Configuration',f'name = "{t["name"]}"','author = "Latan Villegas"',f'id = "com.latanvillegas.{t["slug"].replace("-","")}"','version = 1',f'description = "Generation 2 advanced FUTO theme: {t["name"]}."','', '[options]','auto_borders = true','center_hints = false','roundedness = 0.9','scale_text = 1.02','scale_hints = 0.92','weight_text = 500','weight_hints = 500','', '[colors]',f'primary = "{accent}"',f'on_primary = "{fg}"',f'primary_container = "{kv}"',f'on_primary_container = "{fg}"',f'secondary = "{accent}"',f'on_secondary = "{fg}"',f'secondary_container = "{kc}"',f'on_secondary_container = "{fg}"',f'tertiary = "{accent}"',f'on_tertiary = "{fg}"',f'tertiary_container = "{kv}"',f'on_tertiary_container = "{fg}"',f'background = "{t["bg"]}"',f'on_background = "{fg}"',f'surface = "{t["bg"]}"',f'on_surface = "{fg}"',f'surface_variant = "{kc}"',f'on_surface_variant = "{fg}"',f'outline = "{accent}"',f'outline_variant = "{kv}"','scrim = "#000000"',f'keyboard_surface = "{t["bg"]}"',f'keyboard_surface_dim = "{t["bg"]}"',f'keyboard_container = "{kc}"',f'keyboard_container_variant = "{kv}"',f'on_keyboard_container = "{fg}"',f'keyboard_press = "{accent}"',f'keyboard_container_pressed = "{kp}"',f'on_keyboard_container_pressed = "{fg}"','', '[options.font]',f'font = "{t["font"]}"','', '[options.background]','image = "background.webp"','opacity = 1.0','action_bar_opacity = 0.84','cropping = [0, 0, 1, 1]']
 for sel,asset in [('pressed','pressed.png'),('popup','popup.png'),('action','action.png'),('functional','functional.png'),('spacebar','normal.png'),('normal','normal.png')]: lines += ['','[[matchrules.border]]',f'selector = "{sel}"',f'asset = "{asset}"']
 for asset in ['normal.png','functional.png','action.png','pressed.png','popup.png']: lines += ['','[[asset.border]]',f'name = "{asset}"','background_tint = "#FFFFFFFF"','foreground_tint = "#FFFFFFFF"','padding = [0.055, 0.05, 0.945, 0.95]','slicing = [0.28, 0.28, 0.72, 0.72]','gap = [0.02, 0.02, 0.98, 0.98]','target_density = 320']
 (out/'theme.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8'); (out/'CREDITS.txt').write_text(f"{t['name']}\nTheme design and original visual assets: Latan Villegas\nTypography asset: {t['font']} from Google Fonts; original authors and OFL preserved in the included OFL file.\n",encoding='utf-8'); (out/'LICENSE.txt').write_text('Theme design and original visual assets: Copyright (c) 2026 Latan Villegas. Permission is granted to use, copy, modify and redistribute with attribution. Third-party components retain their original licenses.\n',encoding='utf-8')
 z=DIST/f"{t['slug']}-FUTO.zip";z.unlink(missing_ok=True)
 with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
  for p in out.iterdir():
   if p.is_file():f.write(p,p.name)
 print(z)
for t in THEMES: build(t)
