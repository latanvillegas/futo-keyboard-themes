from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import math,random,zipfile,urllib.request
R=Path(__file__).resolve().parents[1];O=R/'build'/'nova-flora-atelier-26';D=R/'dist';O.mkdir(parents=True,exist_ok=True);D.mkdir(exist_ok=True)
for p in O.iterdir():
 if p.is_file(): p.unlink()
def dl(u,p): p.write_bytes(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read())
dl('https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/NotoSans%5Bwdth,wght%5D.ttf',O/'NovaDisplay.ttf');dl('https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/OFL.txt',O/'OFL-NotoSans.txt')
W,H=1600,1000;bg=Image.new('RGBA',(W,H),(7,8,18,255));m=Image.new('RGBA',(W,H));d=ImageDraw.Draw(m)
for b,c in [((-300,-220,850,780),(74,95,255,62)),((900,-260,1850,620),(0,224,190,50)),((650,470,1750,1350),(255,73,164,44)),((-350,600,650,1350),(255,178,76,28))]:d.ellipse(b,fill=c)
bg=Image.alpha_composite(bg,m.filter(ImageFilter.GaussianBlur(70)));a=Image.new('RGBA',(W,H));q=ImageDraw.Draw(a);cx,cy=1270,250
for i in range(8):
 t=math.radians(i*45);x=cx+math.cos(t)*105;y=cy+math.sin(t)*105;q.ellipse((x-78,y-42,x+78,y+42),fill=(222,129,224,26),outline=(244,184,239,55),width=2)
q.ellipse((cx-38,cy-38,cx+38,cy+38),fill=(255,209,132,55))
for r in (145,220,310):q.arc((cx-r,cy-r,cx+r,cy+r),195,500,fill=(152,237,232,max(25,100-r//5)),width=3)
for j in range(4):q.line([(x,690+j*55+42*math.sin(x/170+j)) for x in range(-50,W+50,16)],fill=(174,203,255,25+j*8),width=5)
random.seed(2626)
for _ in range(110):
 x=random.randrange(W);y=random.randrange(H);r=random.choice([1,1,2,2,3]);q.ellipse((x-r,y-r,x+r,y+r),fill=(245,244,255,random.randrange(30,120)))
Image.alpha_composite(bg,a).convert('RGB').save(O/'nova-flora-background.webp','WEBP',quality=96,method=6)
def key(n,f,e,deco=None,press=False):
 im=Image.new('RGBA',(256,280));d=ImageDraw.Draw(im)
 if press:d.rounded_rectangle((4,5,252,278),56,fill=(98,255,227,46))
 d.polygon([(20,43),(48,19),(201,20),(237,50),(242,206),(218,255),(181,268),(57,264),(18,233),(13,82)],fill=f);d.rounded_rectangle((20,24,236,256),47,outline=e,width=4);d.arc((34,31,220,139),196,342,fill=(255,255,255,112),width=4)
 if deco=='petal':
  for t in range(0,360,90):
   x=205+math.cos(math.radians(t))*15;y=218+math.sin(math.radians(t))*15;d.ellipse((x-11,y-8,x+11,y+8),fill=(255,135,207,165))
  d.ellipse((199,212,211,224),fill=(255,226,157,230))
 elif deco=='leaf':d.ellipse((17,147,72,204),fill=(76,228,187,145));d.line((34,190,63,159),fill=(235,255,248,190),width=4)
 elif deco=='orb':d.ellipse((186,35,226,75),outline=(151,239,255,220),width=5);d.ellipse((197,46,215,64),fill=(211,176,255,190))
 elif deco=='star':
  pts=[]
  for i in range(10):
   t=-math.pi/2+i*math.pi/5;rr=22 if i%2==0 else 9;pts.append((209+math.cos(t)*rr,218+math.sin(t)*rr))
  d.polygon(pts,fill=(255,219,151,190))
 elif deco=='circuit':d.line((25,80,53,80,53,112,77,112),fill=(112,239,226,125),width=4);d.ellipse((20,75,30,85),fill=(170,255,244,200));d.ellipse((72,107,82,117),fill=(170,255,244,200))
 im.save(O/n)
A=[('nova-default.png',(15,22,48,242),(98,185,226,225),None),('nova-petal.png',(25,21,53,247),(231,125,202,230),'petal'),('nova-leaf.png',(14,32,48,247),(90,226,188,230),'leaf'),('nova-orb.png',(23,24,62,248),(155,143,242,235),'orb'),('nova-star.png',(39,27,54,248),(238,177,113,230),'star'),('nova-circuit.png',(15,29,56,248),(85,220,216,230),'circuit'),('nova-functional.png',(28,30,67,250),(151,145,228,230),None),('nova-action.png',(31,99,104,252),(143,255,229,245),'orb'),('nova-pressed.png',(43,139,132,252),(198,255,242,255),None),('nova-popup.png',(68,43,95,252),(239,156,219,245),'petal'),('nova-space.png',(18,43,61,250),(110,223,211,230),'circuit')]
for n,f,e,x in A:key(n,f,e,x,n=='nova-pressed.png')
Image.new('RGBA',(256,280)).save(O/'nova-blank.png')
def icon(n,fn):im=Image.new('RGBA',(192,192));fn(ImageDraw.Draw(im));im.save(O/n)
icon('nova-enter.png',lambda d:(d.line((151,40,151,110,66,110),fill='white',width=16),d.polygon([(70,70),(24,110),(70,151)],fill='white')));icon('nova-shift.png',lambda d:(d.polygon([(96,20),(32,86),(63,86),(63,145),(129,145),(129,86),(160,86)],fill='white'),d.ellipse((87,54,105,72),fill=(17,26,55,255))));icon('nova-shifted.png',lambda d:(d.polygon([(96,18),(31,83),(63,83),(63,137),(129,137),(129,83),(161,83)],fill='white'),d.rectangle((58,154,134,169),fill='white')));icon('nova-delete.png',lambda d:(d.polygon([(24,96),(68,49),(164,49),(164,143),(68,143)],outline='white'),d.line((88,75,131,118),fill='white',width=12),d.line((131,75,88,118),fill='white',width=12)));icon('nova-emoji.png',lambda d:(d.ellipse((27,27,165,165),outline='white',width=13),d.ellipse((62,68,76,82),fill='white'),d.ellipse((116,68,130,82),fill='white'),d.arc((59,84,134,140),10,170,fill='white',width=10)))
c={'primary':'#9CEFE3','on_primary':'#003731','primary_container':'#145149','on_primary_container':'#B9F8EE','inverse_primary':'#356A62','secondary':'#C8B8F5','on_secondary':'#302653','secondary_container':'#493E6C','on_secondary_container':'#E6DEFF','tertiary':'#F4B3D7','on_tertiary':'#4B1437','tertiary_container':'#66304F','on_tertiary_container':'#FFD8EC','error':'#FFB4AB','on_error':'#690005','error_container':'#93000A','on_error_container':'#FFDAD6','background':'#070812','on_background':'#E9E7F2','surface':'#090B18','on_surface':'#E9E7F2','surface_variant':'#45464F','on_surface_variant':'#C7C5D0','outline':'#91909A','outline_variant':'#45464F','scrim':'#000000','inverse_surface':'#E9E7F2','inverse_on_surface':'#2D303A','surface_tint':'#9CEFE3','surface_dim':'#070812','surface_bright':'#373842','surface_container_lowest':'#03040C','surface_container_low':'#0D0F1D','surface_container':'#121423','surface_container_high':'#1C1E2D','surface_container_highest':'#272938','keyboard_surface':'#070812','keyboard_surface_dim':'#04050E','keyboard_container':'#111831','keyboard_container_variant':'#28264C','on_keyboard_container':'#FCFAFF','keyboard_press':'#9CEFE3','keyboard_container_pressed':'#338B7E','on_keyboard_container_pressed':'#FFFFFF'}
L=['# Format version: 1.0','','name = "Nova Flora Atelier 26"','author = "Latan Villegas"','id = "com.latanvillegas.novafloraatelier26"','version = 1','description = "Premium bio-futurist designer theme with positional artwork, label-specific keys, high-density assets, custom icons, font and background."','','[options]','auto_borders = true','center_hints = false','roundedness = 1','scale_text = 1.02','scale_hints = 0.94','weight_text = 580','weight_hints = 510','','[colors]']+[f'{k} = "{v}"' for k,v in c.items()]+['','[options.font]','font = "NovaDisplay.ttf"','','[options.background]','image = "nova-flora-background.webp"','opacity = 1','action_bar_opacity = 0.66','cropping = [0, 0, 1, 1]']
rules=[('pressed functional row 0 col 0','nova-pressed.png'),('pressed label b','nova-pressed.png'),('pressed label o','nova-pressed.png'),('pressed label f','nova-pressed.png'),('popup','nova-popup.png'),('morekeysbox','nova-functional.png'),('morekey','nova-blank.png'),('normal label b','nova-petal.png'),('normal label o','nova-orb.png'),('normal label f','nova-leaf.png'),('normal row 1 col -1','nova-star.png'),('normal row 1 col -2','nova-petal.png'),('normal rowmod 1 2 colmod 3 5','nova-leaf.png'),('normal rowmod 0 2 colmod 4 5','nova-orb.png'),('normal rowmod 1 2 colmod 3 9','nova-circuit.png'),('normal rowmod 0 2 colmod 2 9','nova-star.png'),('stickyon','nova-popup.png'),('spacebar pressed','nova-pressed.png'),('spacebar','nova-space.png'),('action pressed','nova-pressed.png'),('action','nova-action.png'),('functional row -1 col 0 pressed','nova-pressed.png'),('functional pressed','nova-pressed.png'),('functional row -1 col 0','nova-action.png'),('functional popup','nova-popup.png'),('functional','nova-functional.png'),('normal popup','nova-popup.png'),('pressed','nova-pressed.png'),('normal','nova-default.png')]
for s,a in rules:L+=['','[[matchrules.border]]',f'selector = "{s}"',f'asset = "{a}"']
for s,a in [('icon delete_key','nova-delete.png'),('icon action_emoji','nova-emoji.png'),('icon shift_key_shifted','nova-shifted.png'),('icon shift_key','nova-shift.png'),('icon enter_key','nova-enter.png')]:L+=['','[[matchrules.icon]]',f'selector = "{s}"',f'asset = "{a}"']
for n,_,_,_ in A:
 L+=['','[[asset.border]]',f'name = "{n}"','background_tint = "#FFFFFFFF"','foreground_tint = "#FFFFFFFF"','padding = [0, 0, 0, 0]','slicing = [0.31, 0.31, 0.68, 0.68]','gap = [1, 1, 1, 1]','target_density = 640']
L+=['','[[asset.border]]','name = "nova-blank.png"','background_tint = "#FFFFFFFF"','foreground_tint = "#FFFFFFFF"','padding = [0, 0, 0, 0]','slicing = [0, 0, 1, 1]','gap = [1, 1, 1, 1]','target_density = 640']
for a in ['nova-enter.png','nova-shift.png','nova-shifted.png','nova-delete.png','nova-emoji.png']:L+=['','[[asset.icon]]',f'name = "{a}"','target_density = 640']
(O/'theme.txt').write_text('\n'.join(L)+'\n');(O/'CREDITS.txt').write_text('Nova Flora Atelier 26\nOriginal theme design, background, borders and icons: Latan Villegas.\nNoto Sans: The Noto Project Authors, Google Fonts, SIL OFL.\n');z=D/'nova-flora-atelier-26-FUTO.zip';z.unlink(missing_ok=True)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in O.iterdir():
  if p.is_file():f.write(p,p.name)
print('Built',z)
