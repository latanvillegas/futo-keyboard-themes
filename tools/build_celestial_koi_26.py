from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import zipfile,math,urllib.request,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build'/'celestial-koi-26';DIST=ROOT/'dist';OUT.mkdir(parents=True,exist_ok=True);DIST.mkdir(exist_ok=True)
for p in OUT.iterdir():
 if p.is_file():p.unlink()
def dl(url,path):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'});path.write_bytes(urllib.request.urlopen(req,timeout=60).read())
dl('https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/NotoSans%5Bwdth,wght%5D.ttf',OUT/'CelestialSans.ttf');dl('https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/OFL.txt',OUT/'OFL-CelestialSans.txt')
W,H=1440,900;bg=Image.new('RGBA',(W,H),(5,13,31,255));layer=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(layer)
for box,col in [((-260,-180,720,700),(32,122,190,65)),((750,-250,1650,650),(106,72,190,58)),((600,400,1580,1200),(17,184,166,42))]:d.ellipse(box,fill=col)
for cx,cy in [(230,650),(1110,220),(850,690)]:
 for r in (70,120,185,260):d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(130,224,245,max(12,70-r//5)),width=3)
layer=layer.filter(ImageFilter.GaussianBlur(18));bg=Image.alpha_composite(bg,layer);art=Image.new('RGBA',(W,H),(0,0,0,0));a=ImageDraw.Draw(art)
def koi(cx,cy,scale,angle,color):
 im=Image.new('RGBA',(360,220),(0,0,0,0));q=ImageDraw.Draw(im);q.ellipse((75,70,255,150),fill=color);q.polygon([(70,110),(18,62),(38,112),(18,158)],fill=color);q.polygon([(220,80),(275,45),(252,103)],fill=color);q.polygon([(215,142),(270,177),(250,120)],fill=color);q.ellipse((224,95,234,105),fill=(5,13,31,220));im=im.resize((int(360*scale),int(220*scale)),Image.Resampling.LANCZOS).rotate(angle,expand=True,resample=Image.Resampling.BICUBIC);art.alpha_composite(im,(int(cx-im.width/2),int(cy-im.height/2)))
koi(1130,660,.85,-18,(242,173,122,70));koi(330,235,.62,155,(155,229,235,55))
for x,y,r in [(90,110,3),(410,90,4),(680,170,3),(970,90,5),(1280,330,3),(570,720,4),(1250,760,5)]:a.ellipse((x-r,y-r,x+r,y+r),fill=(220,249,255,160))
Image.alpha_composite(bg,art).convert('RGB').save(OUT/'celestial-koi-background.webp','WEBP',quality=95)
def key(name,fill,outline,glow=None,functional=False):
 S=4;w,h=128,140;im=Image.new('RGBA',(w*S,h*S),(0,0,0,0));dr=ImageDraw.Draw(im)
 if glow:dr.rounded_rectangle((3*S,5*S,125*S,138*S),30*S,fill=glow)
 pts=[(12,18),(28,9),(101,11),(119,25),(121,105),(110,128),(91,133),(31,130),(10,116),(7,40)];dr.polygon([(x*S,y*S) for x,y in pts],fill=fill);dr.rounded_rectangle((10*S,12*S,119*S,130*S),25*S,outline=outline,width=2*S);dr.arc((18*S,17*S,108*S,73*S),195,342,fill=(255,255,255,120),width=2*S)
 if functional:dr.ellipse((96*S,104*S,108*S,116*S),fill=(239,190,132,130))
 im.resize((w,h),Image.Resampling.LANCZOS).save(OUT/name)
key('pearl-normal.png',(15,38,66,232),(128,220,235,210));key('pearl-functional.png',(26,34,73,245),(166,148,231,220),functional=True);key('pearl-action.png',(34,91,107,248),(168,247,236,235),(61,230,218,35));key('pearl-pressed.png',(44,126,143,250),(205,255,247,255),(96,250,232,45));key('pearl-popup.png',(66,57,107,250),(231,183,246,240))
def icon(name,fn):
 im=Image.new('RGBA',(96,96),(0,0,0,0));fn(ImageDraw.Draw(im));im.save(OUT/name)
icon('koi-shift.png',lambda d:(d.polygon([(48,13),(18,45),(34,45),(34,73),(62,73),(62,45),(78,45)],fill='white'),d.ellipse((43,28,53,38),fill=(5,13,31,255))))
icon('koi-shifted.png',lambda d:(d.polygon([(48,10),(17,43),(33,43),(33,68),(63,68),(63,43),(79,43)],fill='white'),d.rectangle((30,77,66,84),fill='white')))
icon('koi-enter.png',lambda d:(d.line((77,22,77,56,32,56),fill='white',width=9),d.polygon([(35,37),(14,56),(35,75)],fill='white')))
icon('koi-backspace.png',lambda d:(d.polygon([(13,48),(35,25),(82,25),(82,71),(35,71)],outline='white'),d.line((44,38,65,59),fill='white',width=6),d.line((65,38,44,59),fill='white',width=6)))
icon('koi-emoji.png',lambda d:(d.ellipse((14,14,82,82),outline='white',width=7),d.ellipse((31,34,38,41),fill='white'),d.ellipse((58,34,65,41),fill='white'),d.arc((30,42,67,68),10,170,fill='white',width=5)))
badge=Image.new('RGBA',(256,256),(0,0,0,0));bd=ImageDraw.Draw(badge)
for r,alpha in [(95,180),(70,130),(45,90)]:bd.ellipse((128-r,128-r,128+r,128+r),outline=(145,231,244,alpha),width=5)
bd.arc((55,80,200,175),190,350,fill=(244,188,137,230),width=12);badge.save(OUT/'moon-water-badge.png')
c={'primary':'#A6EEF2','on_primary':'#00373B','primary_container':'#164F57','on_primary_container':'#C5F7F8','inverse_primary':'#38666A','secondary':'#C8B9F2','on_secondary':'#302653','secondary_container':'#473D6B','on_secondary_container':'#E5DEFF','tertiary':'#F1BE91','on_tertiary':'#48290E','tertiary_container':'#62401F','on_tertiary_container':'#FFDCC0','error':'#FFB4AB','on_error':'#690005','error_container':'#93000A','on_error_container':'#FFDAD6','background':'#050D1F','on_background':'#E5EAF4','surface':'#071020','on_surface':'#E5EAF4','surface_variant':'#3F484A','on_surface_variant':'#BFC8CA','outline':'#899294','outline_variant':'#3F484A','scrim':'#000000','inverse_surface':'#E5EAF4','inverse_on_surface':'#2B3038','surface_tint':'#A6EEF2','surface_dim':'#050D1F','surface_bright':'#343A45','surface_container_lowest':'#020817','surface_container_low':'#0B1527','surface_container':'#101A2C','surface_container_high':'#1A2436','surface_container_highest':'#253043','keyboard_surface':'#050D1F','keyboard_surface_dim':'#020817','keyboard_container':'#102641','keyboard_container_variant':'#252A51','on_keyboard_container':'#F5FDFF','keyboard_press':'#9DEFE8','keyboard_container_pressed':'#267C88','on_keyboard_container_pressed':'#FFFFFF'}
lines=['# Format version: 1.0','','name = "Celestial Koi 26"','author = "Latan Villegas"','id = "com.latanvillegas.celestialkoi26"','version = 1','description = "Premium celestial koi designer theme with organic pearl keys, custom icons, font, background and full assets."','','[options]','auto_borders = true','center_hints = false','roundedness = 0.92','scale_text = 1.02','scale_hints = 0.90','weight_text = 590','weight_hints = 500','','[colors]']+[f'{k} = "{v}"' for k,v in c.items()]+['','[options.font]','font = "CelestialSans.ttf"','','[options.background]','image = "celestial-koi-background.webp"','opacity = 1.0','action_bar_opacity = 0.76','cropping = [0, 0, 1, 1]']
for s,a in [('pressed','pearl-pressed.png'),('popup','pearl-popup.png'),('action','pearl-action.png'),('functional','pearl-functional.png'),('spacebar','pearl-normal.png'),('normal','pearl-normal.png')]:lines+=['','[[matchrules.border]]',f'selector = "{s}"',f'asset = "{a}"']
for s,a in [('icon shift_key_shifted','koi-shifted.png'),('icon shift_key','koi-shift.png'),('icon enter_key','koi-enter.png'),('icon action_emoji','koi-emoji.png'),('icon backspace','koi-backspace.png')]:lines+=['','[[matchrules.icon]]',f'selector = "{s}"',f'asset = "{a}"']
for a in ['pearl-normal.png','pearl-functional.png','pearl-action.png','pearl-pressed.png','pearl-popup.png']:lines+=['','[[asset.border]]',f'name = "{a}"','background_tint = "#FFFFFFFF"','foreground_tint = "#FFFFFFFF"','padding = [0.055, 0.05, 0.945, 0.95]','slicing = [0.30, 0.28, 0.70, 0.72]','gap = [0.025, 0.02, 0.975, 0.98]','target_density = 320']
for a in ['koi-shift.png','koi-shifted.png','koi-enter.png','koi-backspace.png','koi-emoji.png']:lines+=['','[[asset.icon]]',f'name = "{a}"','foreground_tint = "#FFFFFFFF"','target_density = 320']
(OUT/'theme.txt').write_text('\n'.join(lines)+'\n');(OUT/'CREDITS.txt').write_text('Celestial Koi 26\nOriginal background, border and icon artwork: Latan Villegas\nNoto Sans: The Noto Project Authors, Google Fonts, SIL OFL.\n');z=DIST/'celestial-koi-26-FUTO.zip';z.unlink(missing_ok=True)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in OUT.iterdir():
  if p.is_file():f.write(p,p.name)
print('Built',z)
