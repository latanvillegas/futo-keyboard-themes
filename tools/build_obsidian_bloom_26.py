from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import zipfile,math,random,urllib.request
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build'/'obsidian-bloom-26';DIST=ROOT/'dist';OUT.mkdir(parents=True,exist_ok=True);DIST.mkdir(exist_ok=True)
for p in OUT.iterdir():
 if p.is_file():p.unlink()
def dl(url,path):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'});path.write_bytes(urllib.request.urlopen(req,timeout=60).read())
dl('https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/NotoSans%5Bwdth,wght%5D.ttf',OUT/'NotoSans.ttf');dl('https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/OFL.txt',OUT/'OFL-NotoSans.txt')
W,H=1440,900;bg=Image.new('RGBA',(W,H),(6,7,10,255));art=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(art)
for cx,cy,r,col in [(1180,190,220,(219,105,154,62)),(260,700,260,(105,70,210,50)),(750,500,180,(240,177,100,38))]:
 for petal in range(10):
  a=2*math.pi*petal/10;px=cx+math.cos(a)*r*.42;py=cy+math.sin(a)*r*.42;rr=r*.48;d.ellipse((px-rr,py-rr*.52,px+rr,py+rr*.52),fill=col)
 d.ellipse((cx-r*.18,cy-r*.18,cx+r*.18,cy+r*.18),fill=(255,210,160,50))
for off in range(4):d.line([(x,700-off*120-100*math.sin(x/260+off)) for x in range(-100,W+150,20)],fill=(220,178,125,30+off*8),width=3+off)
art=art.filter(ImageFilter.GaussianBlur(42));bg=Image.alpha_composite(bg,art);fine=Image.new('RGBA',(W,H),(0,0,0,0));fd=ImageDraw.Draw(fine);random.seed(2026)
for _ in range(90):
 x=random.randrange(W);y=random.randrange(H);r=random.choice([1,1,2]);fd.ellipse((x-r,y-r,x+r,y+r),fill=(255,220,180,random.randrange(25,85)))
fd.arc((980,-80,1500,430),120,280,fill=(229,183,126,90),width=3);fd.arc((-170,510,380,1040),280,80,fill=(183,135,255,70),width=3);Image.alpha_composite(bg,fine).convert('RGB').save(OUT/'obsidian-bloom-background.webp','WEBP',quality=96,method=6)
def key(name,fill,edge,inner,pressed=False,action=False,jewel=False):
 w,h,s=128,140,4;im=Image.new('RGBA',(w*s,h*s),(0,0,0,0));dr=ImageDraw.Draw(im)
 if pressed:dr.rounded_rectangle((3*s,7*s,(w-3)*s,(h-2)*s),25*s,fill=(239,155,191,40))
 dr.rounded_rectangle((8*s,11*s,(w-5)*s,(h-3)*s),23*s,fill=(0,0,0,110));dr.rounded_rectangle((7*s,7*s,(w-7)*s,(h-8)*s),23*s,fill=fill,outline=edge,width=2*s);dr.rounded_rectangle((11*s,11*s,(w-11)*s,(h-12)*s),19*s,outline=inner,width=s);dr.line((22*s,17*s,(w-22)*s,17*s),fill=(255,238,215,110),width=2*s);dr.line((15*s,30*s,15*s,(h-32)*s),fill=(255,255,255,35),width=s)
 if jewel:dr.ellipse(((w-25)*s,15*s,(w-17)*s,23*s),fill=(255,202,145,200))
 if action:dr.rounded_rectangle((25*s,(h-29)*s,(w-25)*s,(h-21)*s),4*s,fill=(255,221,174,180))
 im.resize((w,h),Image.Resampling.LANCZOS).save(OUT/name)
key('obsidian-normal.png',(13,14,19,250),(105,85,89,255),(255,225,205,35),jewel=True);key('obsidian-functional.png',(24,20,29,252),(146,101,128,255),(255,222,210,42),jewel=True);key('obsidian-action.png',(103,45,72,253),(244,169,190,255),(255,230,210,65),action=True,jewel=True);key('obsidian-pressed.png',(130,52,86,253),(255,198,213,255),(255,245,232,75),pressed=True,jewel=True);key('obsidian-popup.png',(49,34,67,253),(207,155,255,255),(255,230,250,65),jewel=True)
c={'primary':'#F1A8BE','on_primary':'#3B071C','primary_container':'#69253E','on_primary_container':'#FFD9E3','inverse_primary':'#91445E','secondary':'#D8B78E','on_secondary':'#291806','secondary_container':'#594126','on_secondary_container':'#F6DEBE','tertiary':'#C8A7FF','on_tertiary':'#2D0755','tertiary_container':'#53377A','on_tertiary_container':'#ECDFFF','error':'#FFB4AB','on_error':'#690005','error_container':'#93000A','on_error_container':'#FFDAD6','background':'#06070A','on_background':'#FFF5F5','surface':'#0A0B10','on_surface':'#FFF5F5','surface_variant':'#2D272F','on_surface_variant':'#E4D4DC','outline':'#AA929D','outline_variant':'#51454B','scrim':'#000000','inverse_surface':'#F6EDEF','inverse_on_surface':'#2D272A','surface_tint':'#F1A8BE','surface_dim':'#040508','surface_bright':'#3B3339','surface_container_lowest':'#020306','surface_container_low':'#0C0C12','surface_container':'#131218','surface_container_high':'#1C1A21','surface_container_highest':'#27232B','keyboard_surface':'#06070A','keyboard_surface_dim':'#040508','keyboard_container':'#111016','keyboard_container_variant':'#29232C','on_keyboard_container':'#FFF8F8','keyboard_press':'#F1A8BE','keyboard_container_pressed':'#873A59','on_keyboard_container_pressed':'#FFFFFF'}
lines=['name = "Obsidian Bloom 26"','author = "Latan Villegas"','id = "com.latanvillegas.obsidianbloom26"','version = 1','description = "Expert luxury botanical theme with sculpted obsidian keys and original bloom artwork."','','[options]','auto_borders = true','center_hints = false','roundedness = 0.88','scale_text = 1.04','scale_hints = 0.90','weight_text = 620','weight_hints = 520','','[colors]']+[f'{k} = "{v}"' for k,v in c.items()]+['','[options.font]','font = "NotoSans.ttf"','','[options.background]','image = "obsidian-bloom-background.webp"','opacity = 0.98','action_bar_opacity = 0.78','cropping = [0, 0, 1, 1]']
for sel,a in [('pressed','obsidian-pressed.png'),('popup','obsidian-popup.png'),('action','obsidian-action.png'),('functional','obsidian-functional.png'),('spacebar','obsidian-normal.png'),('normal','obsidian-normal.png')]:lines+=['','[[matchrules.border]]',f'selector = "{sel}"',f'asset = "{a}"']
for a in ['obsidian-normal.png','obsidian-functional.png','obsidian-action.png','obsidian-pressed.png','obsidian-popup.png']:lines+=['','[[asset.border]]',f'name = "{a}"','background_tint = "#FFFFFFFF"','foreground_tint = "#FFFFFFFF"','padding = [0.055, 0.05, 0.945, 0.95]','slicing = [0.29, 0.27, 0.71, 0.73]','gap = [0.025, 0.02, 0.975, 0.98]','target_density = 320']
(OUT/'theme.txt').write_text('\n'.join(lines)+'\n');(OUT/'CREDITS.txt').write_text('Obsidian Bloom 26\nOriginal concept, botanical artwork and sculpted key assets: Latan Villegas\nNoto Sans: Noto Project Authors, Google Fonts, SIL OFL 1.1.\n');(OUT/'LICENSE.txt').write_text('Original visual assets Copyright (c) 2026 Latan Villegas. Noto Sans remains under the included SIL Open Font License.\n');z=DIST/'obsidian-bloom-26-FUTO.zip';z.unlink(missing_ok=True)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in OUT.iterdir():
  if p.is_file():f.write(p,p.name)
print('Built',z)
