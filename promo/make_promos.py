# Renders real in-game screenshots with Chromium, then adds Persian text with PIL.
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random,os
ROOT=os.path.dirname(os.path.abspath(__file__))+'/..'
SC={
1:"""()=>{ZOOM=1.45;start(6);document.getElementById('eb').click();G.sl=25;G.slots[0]=4;G.found=1;upd();
 const g=G.gh[0],gx=g.x/TS|0,gy=g.y/TS|0,d=bfs(gx,gy);let best=null;
 for(let j=1;j<G.W-1;j++)for(let i=1;i<G.W-1;i++){const v=d[j*G.W+i];if(v==2&&i==gx&&(!best||j<gy))best=[i,j]}
 if(!best)for(let j=1;j<G.W-1;j++)for(let i=1;i<G.W-1;i++)if(d[j*G.W+i]==2)best=[i,j];
 G.px=(best[0]+.5)*TS;G.py=(best[1]+.5)*TS;G.fx=Math.sign(gx-best[0]);G.fy=Math.sign(gy-best[1]);if(!G.fx&&!G.fy)G.fy=1;G.py+=14;G.gh=[g];g.ch=true;G.t=1.3;G.bat=.8;
 run=false;draw()}""",
2:"""async()=>{ZOOM=1.7;start(4);document.getElementById('eb').click();G.sl=25;G.gh=[];const o=G.objs.find(o=>o.k=='d');G.px=(o.x+.5)*TS;G.py=o.y*TS+54;G.fx=0;G.fy=1;G.found=0;G.slots=[];upd();G.bat=.9;doSearch();await new Promise(r=>setTimeout(r,520));}""",
3:"""()=>{ZOOM=1.5;start(7);document.getElementById('eb').click();const o=G.objs.find(o=>o.w=='w');hide(o);o.hop=.5;
 const g=G.gh[0],d=bfs(o.x,o.y);let best=null;for(let j=1;j<G.W-1;j++)for(let i=1;i<G.W-1;i++){const v=d[j*G.W+i];if(j==o.y&&v==1)best=[i,j]}
 if(!best)for(let j=1;j<G.W-1;j++)for(let i=1;i<G.W-1;i++)if(d[j*G.W+i]==1)best=[i,j];
 g.x=g.tx=(best[0]+.5)*TS;g.y=g.ty=(best[1]+.5)*TS;G.gh=[g];G.slots[0]=7;G.slots[2]=2;G.found=2;upd();G.t=2.1;G.fx=0;G.fy=1;run=false;document.getElementById('msg').textContent='';draw()}""",
4:"""async()=>{ZOOM=1.4;start(8);document.getElementById('eb').click();G.gh=[];G.slots[1]=3;G.found=1;upd();G.bat=.6;scare(6000);await new Promise(r=>setTimeout(r,520));}"""}
TXT={1:("از خانه نفرین‌شده فرار کن","هیولا همین نزدیکی است…"),2:("هر کشو یک راز دارد","رقم‌های کد در را پیدا کن"),3:("در کمد قایم شو","تا هیولا پیدایت نکند"),4:("او صدایت را شنید!","۱۰ مرحله وحشت — کاملاً آفلاین")}
LAL=os.path.abspath(ROOT)+'/www/fonts/Lalezar-Regular.ttf'
FONT=LAL if os.path.exists(LAL) else '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
print('font:',FONT)
def fit(d,text,size,maxw):
    while True:
        f=ImageFont.truetype(FONT,size,layout_engine=ImageFont.Layout.RAQM)
        w=d.textlength(text,font=f,direction='rtl',language='fa')
        if w<=maxw or size<30:return f,w
        size-=4
def fa(im,text,y,size,fill,glow=(220,0,0)):
    d=ImageDraw.Draw(im);f,w=fit(d,text,size,980);cx=im.width//2
    g=Image.new('RGBA',im.size,(0,0,0,0));gd=ImageDraw.Draw(g);gd.text((cx,y),text,font=f,fill=glow+(255,),anchor='mt',direction='rtl',language='fa',stroke_width=6)
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)));im.alpha_composite(g.filter(ImageFilter.GaussianBlur(4)))
    d=ImageDraw.Draw(im);d.text((cx,y),text,font=f,fill=(0,0,0,255),anchor='mt',direction='rtl',language='fa',stroke_width=8,stroke_fill=(0,0,0,255))
    d.text((cx,y),text,font=f,fill=fill+(255,),anchor='mt',direction='rtl',language='fa')
    return w,f.size
def drips(im,y,w):
    random.seed(int(y)+int(w));d=ImageDraw.Draw(im);cx=im.width//2
    for _ in range(7):
        x=cx+random.randint(int(-w/2),int(w/2));l=random.randint(26,80);d.rounded_rectangle([x-4,y,x+4,y+l],radius=4,fill=(150,0,0,255));d.ellipse([x-7,y+l-6,x+7,y+l+8],fill=(150,0,0,255))
def shade(im):
    W,H=im.size;m=Image.linear_gradient('L').resize((W,H))
    top=Image.new('RGBA',im.size,(0,0,0,255));top.putalpha(m.transpose(Image.FLIP_TOP_BOTTOM).point(lambda v:int(max(0,v-110)*1.7)));im.alpha_composite(top)
    bot=Image.new('RGBA',im.size,(0,0,0,255));bot.putalpha(m.point(lambda v:int(max(0,v-150)*2.4)));im.alpha_composite(bot)
with sync_playwright() as p:
    b=p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);ctx=b.new_context(viewport={'width':540,'height':960},device_scale_factor=2,has_touch=True,is_mobile=True)
    for n,js in SC.items():
        pg=ctx.new_page();pg.goto('file://'+os.path.abspath(ROOT)+'/www/index.html');pg.wait_for_timeout(400);pg.evaluate(js);pg.wait_for_timeout(120)
        pg.screenshot(path=f'/tmp/shot{n}.png');pg.close()
    b.close()
logo=Image.open(ROOT+'/logo.png').convert('RGBA').resize((150,150),Image.LANCZOS)
for n in SC:
    im=Image.open(f'/tmp/shot{n}.png').convert('RGBA').resize((1080,1920),Image.LANCZOS);shade(im)
    t,s=TXT[n];w,sz=fa(im,t,185,104,(236,40,40));drips(im,185+sz+14,w);fa(im,s,375,58,(240,222,200),(120,0,0))
    m=Image.new('L',(150,150),0);ImageDraw.Draw(m).rounded_rectangle([0,0,149,149],radius=32,fill=255);im.paste(logo,(80,1700),m)
    fa(im,'خانه نفرین شده',1730,70,(236,40,40));fa(im,'برای اندروید',1820,40,(240,222,200),(100,0,0))
    im.convert('RGB').save(f'{ROOT}/promo/promo{n}.png')
print('ok')
