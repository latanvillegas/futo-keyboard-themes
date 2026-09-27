from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import zipfile,math,urllib.request
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build'/'aero-mint-26-dark';DIST=ROOT/'dist';OUT.mkdir(parents=True,exist_ok=True);DIST.mkdir(exist_ok=True)
for p in OUT.iterdir():
 if p.is_file():p.unlink()
def download(url,path):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'});path.write_bytes(urllib.request.urlopen(req,timeout=60).read())
download('https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/NotoSans%5Bwdth,wght%5D.ttf',OUT/'NotoSans.ttf');download('https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/OFL.txt',OUT/'OFL-NotoSans.txt')
W,H=1440,900;base=Image.new('RGBA',(W,H),(5,14,18,255));mesh=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(mesh)
for box,col in [((-260,-250,650,650),(25,235,190,72)),((850,-250,1610,510),(45,135,255,60)),((780,490,1580,1190),(135,75,255,42))]:d.ellipse(box,fill=col)
for i in range(7):d.line([(x,130+i*110+28*math.sin(x/150+i*.8)) for x in range(-80,W+80,24)],fill=(92,255,220,24),width=4)
mesh=mesh.filter(ImageFilter.GaussianBlur(55));bg=Image.alpha_composite(base,mesh);fine=Image.new('RGBA',(W,H),(0,0,0,0));fd=ImageDraw.Draw(fine);fd.arc((1010,65,1380,435),205,510,fill=(99,255,220,105),width=5);fd.arc((1065,120,1325,380),205,510,fill=(210,255,246,80),width=2);Image.alpha_composite(bg,fine).convert('RGB').save(OUT/'aero-mint-dark.webp','WEBP',quality=95,method=6)
def key(name,fill,edge,pressed=False,action=False):
 w,h,s=128,140,4;im=Image.new('RGBA',(w*s,h*s),(0,0,0,0));dr=ImageDraw.Draw(im)
 if pressed:dr.rounded_rectangle((4*s,7*s,(w-4)*s,(h-3)*s),30*s,fill=(68,255,211,48))
 dr.rounded_rectangle((7*s,7*s,(w-7)*s,(h-7)*s),28*s,fill=fill,outline=edge,width=2*s);dr.arc((14*s,13*s,(w-14)*s,72*s),195,340,fill=(255,255,255,82),width=2*s)
 if action:dr.rounded_rectangle((28*s,(h-27)*s,(w-28)*s,(h-20)*s),3*s,fill=(210,255,245,190))
 im.resize((w,h),Image.Resampling.LANCZOS).save(OUT/name)
key('mint-normal.png',(13,31,36,248),(52,176,157,235));key('mint-functional.png',(18,43,49,250),(70,199,177,245));key('mint-action.png',(14,125,110,252),(105,255,222,255),action=True);key('mint-pressed.png',(29,169,145,252),(154,255,233,255),pressed=True);key('mint-popup.png',(41,31,69,252),(185,139,255,255))
c={'primary':'#65F5D1','on_primary':'#002019','primary_container':'#075247','on_primary_container':'#C8FFF2','inverse_primary':'#006B5B','secondary':'#8BD7FF','on_secondary':'#001E2C','secondary_container':'#174A60','on_secondary_container':'#D4F1FF','tertiary':'#C7A7FF','on_tertiary':'#26004D','tertiary_container':'#4D3274','on_tertiary_container':'#F0E4FF','error':'#FFB4AB','on_error':'#690005','error_container':'#93000A','on_error_container':'#FFDAD6','background':'#050E12','on_background':'#FFFFFF','surface':'#081519','on_surface':'#FFFFFF','surface_variant':'#1B3338','on_surface_variant':'#E9F7F4','outline':'#83B8AE','outline_variant':'#365A53','scrim':'#000000','inverse_surface':'#E7F6F2','inverse_on_surface':'#102724','surface_tint':'#65F5D1','surface_dim':'#03090C','surface_bright':'#294147','surface_container_lowest':'#020608','surface_container_low':'#09171A','surface_container':'#0E2024','surface_container_high':'#152B30','surface_container_highest':'#1D373C','keyboard_surface':'#050E12','keyboard_surface_dim':'#03090C','keyboard_container':'#0D2226','keyboard_container_variant':'#18383D','on_keyboard_container':'#FFFFFF','keyboard_press':'#65F5D1','keyboard_container_pressed':'#1FA88F','on_keyboard_container_pressed':'#FFFFFF'}
lines=['name = "Aero Mint 26 Dark"','author = "Latan Villegas"','id = "com.latanvillegas.aeromint26dark"','version = 2','description = "Premium dark mint theme with high-contrast legends and bundled Noto Sans from Google Fonts."','','[options]','auto_borders = true','center_hints = false','roundedness = 1.0','scale_text = 1.05','scale_hints = 0.92','weight_text = 600','weight_hints = 550','','[colors]']+[f'{k} = "{v}"' for k,v in c.items()]+['','[options.font]','font = "NotoSans.ttf"','','[options.background]','image = "aero-mint-dark.webp"','opacity = 0.98','action_bar_opacity = 0.80','cropping = [0, 0, 1, 1]']
for sel,a in [('pressed','mint-pressed.png'),('popup','mint-popup.png'),('action','mint-action.png'),('functional','mint-functional.png'),('spacebar','mint-normal.png'),('normal','mint-normal.png')]:lines+=['','[[matchrules.border]]',f'selector = "{sel}"',f'asset = "{a}"']
for a in ['mint-normal.png','mint-functional.png','mint-action.png','mint-pressed.png','mint-popup.png']:lines+=['','[[asset.border]]',f'name = "{a}"','background_tint = "#FFFFFFFF"','foreground_tint = "#FFFFFFFF"','padding = [0.055, 0.05, 0.945, 0.95]','slicing = [0.30, 0.28, 0.70, 0.72]','gap = [0.025, 0.02, 0.975, 0.98]','target_density = 320']
(OUT/'theme.txt').write_text('\n'.join(lines)+'\n');(OUT/'CREDITS.txt').write_text('Aero Mint 26 Dark\nOriginal theme/background/key assets: Latan Villegas\nFont: Noto Sans — Noto Project Authors, Google Fonts, SIL OFL 1.1.\n');(OUT/'LICENSE.txt').write_text('Original visual assets Copyright (c) 2026 Latan Villegas. Noto Sans is distributed under the included SIL Open Font License.\n');z=DIST/'aero-mint-26-dark-FUTO.zip';z.unlink(missing_ok=True)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in OUT.iterdir():
  if p.is_file():f.write(p,p.name)
print('Built',z)
