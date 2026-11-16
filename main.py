import json as j,os,urllib.request as r
M=90000
V=(0,100,320,330,500,900,0)
KN=(-33,-31,-18,-14,14,18,31,33);BD=(-17,-15,15,17);RD=(-16,-1,1,16)
DR=(0,0,KN,BD,RD,BD+RD,BD+RD)
Q=[s for s in range(128)if not s&0x88]
R=[""if s&0x88 else"abcdefgh"[s&7]+str(8-(s>>4))for s in range(128)]
I={R[s]:s for s in Q}
B=[0]*256;S=1;C=0;E=-1;K=[116,4]
def e(f,t,p=0):return f|(t<<7)|(p<<14)
def u(m):return R[m&127]+R[(m>>7)&127]+("nbrq"[(m>>14)-2]if(m>>14)else"")
def F(f):
 global B,S,C,E
 p=f.split();B=[0]*256;q=0
 for c in p[0]:
  if c=="/":q+=8
  elif c.isdigit():q+=int(c)
  else:
   d="PNBRQK".find(c.upper())+1;B[q]=d if c.isupper() else-d
   if d==6:K[c>='a']=q
   q+=1
 S=1 if p[1]=="w" else-1;s=p[2];C=sum(1<<"KQkq".index(c)for c in s if c in"KQkq")
 E=I[p[3]]if p[3]!="-"else-1
def A(q,y):
 for o in(15,17):
  t=q+o*y
  if not t&0x88 and B[t]==y:return 1
 for d,v in tuple((d,2)for d in KN)+tuple((d,6)for d in BD+RD):
  t=q+d
  if not t&0x88 and B[t]==v*y:return 1
 for d in BD+RD:
  t=q+d
  while not t&0x88:
   z=B[t]
   if z:
    if z*y in(5,3 if d in BD else 4):return 1
    break
   t+=d
 return 0
def G(s,c=False):
 m=[]
 for q in Q:
  p=B[q]
  if p*s<=0:continue
  b=abs(p)
  if b==1:
   d=-16*s
   for o in(d,d-1,d+1):
    t=q+o
    if t&0x88:continue
    z=B[t]
    if(o==d and z==0 and not c)or(o!=d and((z*s<0 and abs(z)!=6)or t==E)):
     for r in((5,4,3,2)if t<8 or t>=112 else(0,)):m.append(e(q,t,r))
     if o==d and(q>>4)==(7+5*s)//2 and B[q+2*d]==0:m.append(e(q,q+2*d))
  else:
   for d in DR[b]:
    t=q+d
    while not t&0x88:
     z=B[t]
     if z==0:
      if not c:m.append(e(q,t))
     elif z*s<0 and abs(z)!=6:m.append(e(q,t));break
     else:break
     if b in(2,6):break
     t+=d
   if b==6 and not c:
    h=116 if s==1 else 4
    if q==h and not A(h,-s):
     if C&(1 if s==1 else 4)and B[h+1]==0 and B[h+2]==0 and B[h+3]==4*s and not A(h+1,-s)and not A(h+2,-s):m.append(e(h,h+2))
     if C&(2 if s==1 else 8)and B[h-1]==0 and B[h-2]==0 and B[h-3]==0 and B[h-4]==4*s and not A(h-1,-s)and not A(h-2,-s):m.append(e(h,h-2))
 return m
def Z(o):
 global S,C,E
 f=o&127;t=(o>>7)&127;r=(o>>14)&7;p=B[f];w=B[t];y=t;g=C;h=E
 if abs(p)==1 and t==E and w==0:y=t+16*p;w=B[y];B[y]=0
 B[t]=(r if r else abs(p))*((p>0)*2-1);B[f]=0
 if abs(p)==6:
  K[p<0]=t;C&=~3 if p>0 else~12
  if abs(t-f)==2:
   a=t+1 if t>f else t-2;b=t-1 if t>f else t+1;B[b]=B[a];B[a]=0
 for q,b in((119,1),(112,2),(7,4),(0,8)):
  if f==q or t==q:C&=~b
 E=(f+t)//2 if abs(p)==1 and abs(t-f)==32 else-1;S=-S
 return(o,w,y,g,h)
def Y(o):
 global S,C,E
 o,w,y,g,h=o;f=o&127;t=(o>>7)&127;p=B[t]
 if abs(p)==6:
  K[p<0]=f
  if abs(t-f)==2:
   a=t-1 if t>f else t+1;b=t+1 if t>f else t-2;B[b]=B[a];B[a]=0
 B[f]=(p>0)*2-1 if((o>>14)&7)else p;B[t]=0
 if w:B[y]=w
 C,E=g,h;S=-S
def X():
 s=0
 for q in Q:
  p=B[q]
  if p:
   v=V[abs(p)]
   if abs(p)==1:v+=(6-(q>>4))*10 if p>0 else((q>>4)-1)*10
   s+=v if p>0 else-v
 return s if S==1 else-s
def O(m):
 m.sort(key=lambda o:V[abs(B[(o>>7)&127])],reverse=True);return m
def J(d,a,b):
 i=A(K[(1-S)//2],-S)
 if d<=0:
  if not i:
   s=X()
   if s>=b:return b
   if s>a:a=s
   m=G(S,True)
  else:m=G(S)
  O(m);f=False
  for o in m:
   if not i:
    t=(o>>7)&127;v=B[t];g=V[abs(v)]if v else 100
    if s+g+200<a:continue
   u=Z(o)
   if not A(K[(S+1)//2],S):
    f=True;r=-J(0,-b,-a)
    if r>a:
     a=r
     if a>=b:Y(u);return b
   Y(u)
  if i and not f:return-M
  return a
 m=G(S);O(m);w=-M;q=0;f=False
 for o in m:
  u=Z(o)
  if not A(K[(S+1)//2],S):
   f=True;r=-J(d-1,-b,-a)
   if r>w:w=r;q=o
   if r>a:
    a=r
    if a>=b:
     Y(u);break
  Y(u)
 if not f:return-M if i else 0
 return w
def W(f,l):
 F(f)
 r=[e(I[s[:2]],I[s[2:4]],"nbrq".index(s[4])+2 if len(s)==5 else 0)for s in l]
 b=r[0];C3=-M
 for o in r:
  q=Z(o);r2=-J(3,-M,-C3);Y(q)
  if r2>C3:C3=r2;b=o
 return u(b)
U=os.environ["MAKEFUN_ENV_URL"]
def p(q,o):
 with r.urlopen(U+q,j.dumps(o).encode())as w:return j.load(w)
while True:
 g=p("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=p("/move",{"game":g["game"],"move":W(g["fen"],g["legal_moves"])})
