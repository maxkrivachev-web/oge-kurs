import os, sys, json, random, html
D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D)
from tr_short1 import T2,T3,CH4,CH5,J6
from tr_short2 import CH9,J10,CH11,CH13,M14,CH15,J16
from tr_ext import E1,E7,E8,E12,E17
from tr_text import TEXTS
AUTH="авторское задание по модели ФИПИ"
JOPTS=["верно только А","верно только Б","верны оба суждения","оба суждения неверны"]
tasks=[]
def rnd(i): return random.Random(i)
def add(t): tasks.append(t)
for i,(hd,rows,ans,e,s) in enumerate(T2,1):
    tb='<div class="scroll"><table><thead><tr><th>'+hd[0]+'</th><th>'+hd[1]+'</th></tr></thead><tbody>'+''.join('<tr><td>'+a+'</td><td>'+b+'</td></tr>' for a,b in rows)+'</tbody></table></div>'
    add(dict(id=f"t2-{i:02}",l=2,k="word",q="Заполните пропуск в таблице.",x=tb,a=ans,e=e,s=s,m=1))
for i,(what,sim,dif,s) in enumerate(T3,1):
    items=[(f,'s') for f in sim]+[(f,'d') for f in dif]; rnd(f"t3{i}").shuffle(items)
    q=f"Сравните {what}. Выберите и запишите сначала порядковые номера черт сходства, затем черт различия: "+'; '.join(f"{k+1}) {f}" for k,(f,_) in enumerate(items))+'.'
    S=[str(k+1) for k,(f,t) in enumerate(items) if t=='s']; Dd=[str(k+1) for k,(f,t) in enumerate(items) if t=='d']
    add(dict(id=f"t3-{i:02}",l=3,k="seq",q=q,a=dict(s=S,d=Dd),e="Сходство: "+', '.join(S)+"; различие: "+', '.join(Dd)+". Внутри группы порядок любой.",s=s,m=1))
def choice(line,data,pref):
    for i,(q,opts,e,s) in enumerate(data,1):
        o=list(opts); r=rnd(f"{pref}{i}"); idx=list(range(len(o))); r.shuffle(idx)
        add(dict(id=f"{pref}-{i:02}",l=line,k="choice",q=q,o=[o[j] for j in idx],a=idx.index(0)+1,e=e,s=s,m=1))
def judg(line,data,pref):
    for i,(th,A,B,ans,e,s) in enumerate(data,1):
        add(dict(id=f"{pref}-{i:02}",l=line,k="choice",q=f"Верны ли следующие суждения {th}?<br>А. {A}<br>Б. {B}",o=JOPTS,a=ans,e=e,s=s,m=1))
choice(4,CH4,"t4"); choice(5,CH5,"t5"); judg(6,J6,"t6"); choice(9,CH9,"t9"); judg(10,J10,"t10"); choice(11,CH11,"t11"); choice(13,CH13,"t13")
for i,(q,items,cats,e,s) in enumerate(M14,1):
    L="АБВГД"
    body=q+'<br>'+'<br>'.join(f"{L[k]}) {it}" for k,(it,c) in enumerate(items))+'<br><i>'+'; '.join(f"{n+1}) {c}" for n,c in enumerate(cats))+'</i>'
    add(dict(id=f"t14-{i:02}",l=14,k="match",q=body,a=''.join(c for it,c in items),e=e,s=s,m=2))
choice(15,CH15,"t15"); judg(16,J16,"t16")
for i,(th,cons,pair,mean,s) in enumerate(E1,1):
    add(dict(id=f"t1-{i:02}",l=1,k="ext",q=f"Какие два из перечисленных понятий используются в первую очередь при описании {th}? <i>{cons}.</i> Выпишите соответствующие понятия и раскройте смысл любого одного из них.",
        model=f"Понятия: {pair}. Смысл, например: {mean}",crit=["2 балла: выписаны два верных понятия и раскрыт смысл одного.","1 балл: два верных понятия без смысла; или лишнее понятие при раскрытом верном; или одно верное понятие со смыслом.","0 баллов: только одно понятие без смысла или раскрыт смысл только лишнего."],s=s,m=2))
for i,(photo,qq,vals,expl) in enumerate(E7,1):
    add(dict(id=f"t7-{i:02}",l=7,k="ext",q=f"<i>На фото:</i> {photo}<br>Какая традиционная духовно-нравственная ценность российского общества может быть проиллюстрирована с помощью данной фотографии? {qq}",
        model=f"1) Подходит: {vals}. 2) {expl}",crit=["2 балла: названа подходящая ценность из перечня и объяснено ее значение.","1 балл: верно названа только ценность.","0 баллов: ценность не из перечня или среди названных есть неверная."],s="§ 4; Указ № 809",m=2))
for i,(q,mod,s) in enumerate(E8,1):
    add(dict(id=f"t8-{i:02}",l=8,k="ext",q=q,model=mod,crit=["2 балла: верные ответы на оба вопроса.","1 балл: верный ответ на один вопрос.","0 баллов: общие рассуждения."],s=s,m=2))
for i,(qq,gr,rows,model,ans) in enumerate(E12,1):
    tb='<div class="scroll"><table><thead><tr><th>Вариант ответа</th><th class="num">'+gr[0]+', %</th><th class="num">'+gr[1]+', %</th></tr></thead><tbody>'+''.join(f'<tr><td>{a}</td><td class="num">{b}</td><td class="num">{c}</td></tr>' for a,b,c in rows)+'</tbody></table></div>'
    req=("Сформулируйте по одному выводу: а) о сходстве и б) о различии в позициях групп опрошенных. В чем, на ваш взгляд, состоит а) польза, б) вред этого явления? (Предположения - распространенные предложения с объяснением.)" if model==1 else
         "Сформулируйте по одному выводу: а) о сходстве и б) о различии в позициях групп опрошенных. Выскажите предположение, чем объясняются а) сходство и б) различие.")
    crit=(["По 1 баллу: вывод о сходстве, вывод о различии, предположение о пользе, предположение о вреде (максимум 4)."] if model==1 else
          ["4 балла: два вывода и к каждому уместное предположение.","3 балла: два вывода, предположение только к одному.","2 балла: один вывод с предположением или только два вывода.","1 балл: только один вывод."])+["0 баллов: описание данных вместо выводов, общие рассуждения."]
    add(dict(id=f"t12-{i:02}",l=12,k="ext",q=f"Модель {model}. В ходе социологического опроса задавали вопрос: «{qq}» Результаты (в % от числа опрошенных в каждой группе):",x=tb,q2=req,model=ans,crit=crit,s="работа с данными; рекомендации ФИПИ 2026",m=4))
for i,(cond,qq,a,b,s) in enumerate(E17,1):
    add(dict(id=f"t17-{i:02}",l=17,k="ext",q=f"{cond} {qq}",model=f"{a}<br>{b}",crit=["2 балла: приведены два объяснения (а и б).","1 балл: одно объяснение.","0 баллов: общие рассуждения, пересказ условия."],s=s,m=2))
for i,(title,paras,plan,qs,ans,t20,m20,s) in enumerate(TEXTS,1):
    txt='<details class="trtext"><summary>Текст «'+title+'»</summary><div class="txt">'+''.join('<p>'+p+'</p>' for p in paras)+'</div></details>'
    add(dict(id=f"t18-{i:02}",l=18,k="ext",q=f"Прочитайте текст «{title}». Составьте план текста: выделите основные смысловые фрагменты и озаглавьте каждый.",x=txt,model='Возможный план: '+'; '.join(f"{k+1}) {p}" for k,p in enumerate(plan))+'. Допускаются иные формулировки и дополнительные пункты.',crit=["2 балла: выделены основные фрагменты, названия отражают главную мысль каждого.","1 балл: верно выделено больше половины фрагментов или не все названия точные.","0 баллов: названия-цитаты или фрагменты не выделены."],s="авторский учебный текст",m=2))
    add(dict(id=f"t19-{i:02}",l=19,k="ext",q=f"По тексту «{title}»: 1) {qs[0]} 2) {qs[1]} 3) {qs[2]}",x=txt,model='<br>'.join(f"{k+1}) {a}" for k,a in enumerate(ans)),crit=["2 балла: верные ответы на три вопроса.","1 балл: на два.","0 баллов: на один или неверно."],s="авторский учебный текст",m=2))
    add(dict(id=f"t20-{i:02}",l=20,k="ext",q=f"По тексту «{title}». {t20}",x=txt,model='<br>'.join(f"{k+1}) {a}" for k,a in enumerate(m20)),crit=["3 балла: три примера, каждый пояснен.","2 балла: пояснены только два.","1 балл: пояснен один или примеры без пояснений.","0 баллов: один пример без пояснения, общие рассуждения."],s=s,m=3))
for t in tasks: t['src']=AUTH
tasks.sort(key=lambda t:(t['l'],t['id']))
from collections import Counter
cnt=Counter(t['l'] for t in tasks)
tpl=open(os.path.join(D,'trainer_page.html'),encoding='utf-8').read()
page=tpl.replace('__TASKS__',json.dumps(tasks,ensure_ascii=False)).replace('__TOTAL__',str(len(tasks)))
open(os.path.join(D,'..','parts','p_trainer.html'),'w',encoding='utf-8').write(page)
print(len(tasks), dict(sorted(cnt.items())))
