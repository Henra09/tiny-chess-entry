import json,os,sys,urllib.request
E=os.environ["MAKEFUN_ENV_URL"]
def post(p,b):
    return json.load(urllib.request.urlopen(urllib.request.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})))
V={"P":100,"N":320,"B":330,"R":500,"Q":900,"K":20000}
T={
"P":(0,0,0,0,0,0,0,0,5,10,10,-20,-20,10,10,5,5,-5,-10,0,0,-10,-5,5,0,0,0,20,20,0,0,0),
"N":(-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,5,5,0,-20,-40,-30,5,10,15,15,10,5,-30,-30,0,15,20,20,15,0,-30),
"B":(-20,-10,-10,-10,-10,-10,-10,-20,-10,5,0,0,0,0,5,-10,-10,10,10,10,10,10,10,-10,-10,0,10,10,10,10,0,-10),
"R":(0,0,0,0,0,0,0,0,-5,0,0,0,0,0,0,-5,-10,0,0,0,0,0,0,-10,-10,0,0,0,0,0,0,-10),
"Q":(-20,-10,-10,-5,-5,-10,-10,-20,-10,0,5,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5),
"K":(20,30,10,0,0,10,30,20,20,20,0,0,0,0,20,20,-10,-20,-20,-20,-20,-20,-20,-10,-20,-30,-30,-40,-40,-30,-30,-20)}
def pst(c,i):
    t=T[c.upper()]
    return t[i if i<32 else 63-i]
NO=range(21,99)
NK=(-21,-19,-12,-8,8,12,19,21)
KB=(-11,-9,9,11,-10,-1,1,10)
def ix(i):return (i//10-2)*8+i%10-1
def moves(p):
    bd,s,ca,ep,sc=p;R=[]
    up=s=="w"
    for i in NO:
        c=bd[i]
        if c=="."or c=="?"or c.isupper()!=up:continue
        U=c.upper()
        if U=="P":
            d=-10 if up else 10
            pr=(i+d)//10 in(2,9)
            j=i+d
            if bd[j]==".":
                R.append((i,j,"q" if pr else ""))
                if i//10==(9 if up else 2)and bd[i+2*d]==".":R.append((i,i+2*d,""))
            for e in(-1,1):
                j=i+d+e
                t=bd[j]
                if t!="."and t!="?"and t.isupper()!=up:R.append((i,j,"q" if pr else ""))
                elif j==ep:R.append((i,j,""))
        elif U=="N"or U=="K":
            for d in NK:
                j=i+d
                if bd[j]not in".?"and bd[j].isupper()==up:continue
                R.append((i,j,""))
        else:
            for d in KB:
                j=i+d
                while bd[j]==".":
                    R.append((i,j,""));j+=d
                if bd[j]!="?"and bd[j].isupper()!=up:R.append((i,j,""))
        if U=="K"and i==(95 if up else 25):
            k="K" if up else "k";q="Q" if up else "q"
            if k in ca and bd[i+1]=="."and bd[i+2]==".":R.append((i,i+2,""))
            if q in ca and bd[i-1]==bd[i-2]==bd[i-3]==".":R.append((i,i-2,""))
    return R
def make(p,m):
    bd=list(p[0]);i,j,pr=m;up=p[1]=="w";sc=p[4]
    c=bd[i];t=bd[j];u=c.isupper();sgn=1 if u else -1
    sc-=sgn*(V[c]+pst(c,ix(i)))
    if t!=".":
        su=t.isupper()
        sc-=(1 if su else -1)*(V[t]+pst(t,ix(j)))
    n=(pr or c)
    n=n.upper() if up else n.lower()
    bd[j]=n;bd[i]="."
    sc+=sgn*(V[n]+pst(n,ix(j)))
    if c in"Pp"and i%10!=j%10and t==".":
        k=j+(10 if up else -10);x=bd[k];bd[k]="."
        sx=x.isupper()
        sc-=(1 if sx else -1)*(V[x]+pst(x,ix(k)))
    ep=(i+j)//2 if c in"Pp"and abs(j-i)==20 else None
    if c in"Kk"and abs(j-i)==2:
        a,b=(i+3,i+1) if j>i else (i-4,i-1)
        rk=bd[a];bd[b]=rk;bd[a]="."
        sc+=sgn*(pst(rk,ix(b))-pst(rk,ix(a)))
    ca=p[2]
    for q in((91,"Q"),(98,"K"),(21,"q"),(28,"k")):
        if i==q[0]or j==q[0]or c in"Kk":ca=ca.replace(q[1],"")
    return bd,("b" if up else "w"),ca,ep,sc
def pos(f):
    f=f.split();bd=["?"]*120
    for r,row in enumerate(f[0].split("/")):
        k=0
        for ch in row:
            if ch.isdigit():k+=int(ch)
            else:bd[21+10*r+k]=ch;k+=1
    sc=0
    for i in NO:
        c=bd[i]
        if c not in".?":
            su=c.isupper()
            sc+=(1 if su else -1)*(V[c.upper()]+pst(c,ix(i)))
    ep=None if f[3]=="-" else 21+(10-int(f[3][1]))*10+ord(f[3][0])-96
    return bd,f[1],("" if f[2]=="-" else f[2]),ep,sc
class Stop(Exception):pass
ND=0;BUD=60000
def qs(p,a,b):
    global ND
    ND+=1
    if ND>BUD:raise Stop
    up=p[1]=="w";s=p[4] if up else -p[4]
    if s>=b:return s
    if s>a:a=s
    for m in moves(p):
        if p[0][m[1]]=="."and p[0][m[0]]not in"Pp":continue
        v=-qs(make(p,m),-b,-a)
        if v>a:a=v
        if a>=b:break
    return a
def ab(p,d,a,b):
    global ND
    if d==0:return qs(p,a,b)
    ND+=1
    if ND>BUD:raise Stop
    ms=moves(p)
    if not ms:return 0
    ms=sorted(ms,key=lambda m:-V.get(p[0][m[1]],0)-(100 if m[2]else 0))
    for m in ms:
        v=-ab(make(p,m),d-1,-b,-a)
        if v>a:a=v
        if a>=b:break
    return a
def uc(m):
    i,j=m[0],m[1]
    return"%s%d%s%d"%(chr(96+i%10),10-i//10,chr(96+j%10),10-j//10)
def think(p,legal):
    global ND,BUD
    BUD=60000;ND=0
    ls=set(legal)
    ms=[m for m in moves(p) if uc(m) in ls]
    if not ms:return legal[0]
    best=ms[0]
    try:
        for d in range(1,10):
            sc={};a=-9e9
            for m in ms:
                v=-ab(make(p,m),d-1,-9e9,-a)
                sc[m]=v
                if v>a:a=v
            best=max(sc,key=sc.get)
            ms=sorted(ms,key=lambda m:-sc[m])
    except Stop:pass
    return uc(best)
g=post("/game",{})
while g.get("status")!="done":
    while g["status"]=="your_move":
        p=pos(g["fen"])
        mv=think(p,g["legal_moves"])
        g=post("/move",{"game":g["game"],"move":mv})
    print(g["game"],g.get("outcome"),g.get("reason"),file=sys.stderr)
    g=post("/game",{})
print("done",g.get("wins"),g.get("draws"),g.get("losses"),file=sys.stderr)
