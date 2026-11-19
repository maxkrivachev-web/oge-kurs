def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)
T=dict(bg='#f6f7fa',surface='#fdfdfe',ink='#1e2430',mute='#545d6e',blue='#2453c9',blue2='#1d3d8f',red='#b3261e',
 defbg='#edf2fd',vbbg='#fff5cf',trapbg='#fcefed',exbg='#eff1f4',egebg='#f3f0fb',okbg='#e8f5ed',warnbg='#fcf0e2',soft='#eceff4',
 vbtag='#6b5000',egetag='#553aa8',ok='#1b7543',warn='#8f4700')
bgs=['bg','surface','defbg','vbbg','trapbg','exbg','egebg','okbg','warnbg','soft']
for fg in ['ink','mute','blue','blue2','red','vbtag','egetag','ok','warn']:
    print(fg.ljust(7), ' '.join(f"{b}:{cr(T[fg],T[b]):.1f}" for b in bgs))
print('white on blue', round(cr('#ffffff',T['blue']),2), 'white on blue2', round(cr('#ffffff',T['blue2']),2))
