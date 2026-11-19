# Собирает parts/n_glossary.html из старого словаря (gloss_old.json в src/data) и правок glossary_edit.py
import json, os, sys, html
D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D)
import glossary_edit as ge
old=json.load(open(os.path.join(D,'gloss_old.json'),encoding='utf-8'))
secs=[]; moved=[]
for sec,mod,items in old:
    out=[]
    for t,d in items:
        if t in ge.MOVE and ge.MOVE[t]!=mod:
            moved.append((ge.MOVE[t],t,d)); continue
        if t in ge.OVERRIDE: d,n=ge.OVERRIDE[t]
        else: n=''
        out.append([t,d.rstrip('.'),n])
    secs.append([sec,mod,out])
for mod,t,d in moved:
    for s in secs:
        if s[1]==mod: s[2].append([t,'объекты культуры, созданные прошлыми поколениями и имеющие национальную и мировую ценность (Список всемирного наследия ЮНЕСКО)',''])
for s in secs:
    s[2]+= [[t,d,n] for t,d,n in ge.ADD.get(s[1],[])]
    s[2].sort(key=lambda x:x[0].lower())
data=[[sec,mod,ge.PARA[mod],ge.LINES[mod],items] for sec,mod,items in secs]
n=sum(len(s[4]) for s in data); nn=sum(1 for s in data for i in s[4] if i[2])
page='''<section class="page" id="glossary" data-t="Словарь">
<h1>Словарь понятий</h1>
<p class="lead">Все понятия курса в одном месте: родовое слово и существенные признаки, параграф учебника и номера заданий ОГЭ, где понятие нужно. Определения сверены со словарем и текстом учебника под ред. Д.А. Медведева и пересказаны своими словами. В задании 1 засчитывают любое близкое по смыслу раскрытие понятия.</p>
<div class="c trap"><b class="tag">Как раскрывать смысл понятия в задании 1</b><p>Можно не строгим определением, а одним-двумя предложениями через существенные признаки или функции. Нельзя: тавтология («познание - это познавательная деятельность»), только отрицание, только происхождение слова, метафора или афоризм. Если раскрываешь смысл двух понятий и одно неверно, полного балла не будет.</p><p class="cap">Источник: методические рекомендации ФИПИ для обучающихся, ОГЭ 2026.</p></div>
<div class="gtools">
<label for="gq" class="gl">Поиск по словарю</label>
<input id="gq" type="search" placeholder="Например: дееспособность" autocomplete="off" aria-describedby="gcount">
<label class="ck gself"><input type="checkbox" id="gself"> <span>Проверить себя: скрыть определения (нажми на понятие, чтобы открыть)</span></label>
<label class="ck gself"><input type="checkbox" id="gtrap"> <span>Только понятия с частыми ошибками</span></label>
<p class="cap" id="gcount" aria-live="polite"></p>
</div>
<div id="glist"></div>
<div class="empty" id="gempty" hidden><b>Ничего не найдено</b>Попробуй часть слова (например, «дееспос») или сними фильтр частых ошибок.</div>
<script>
{
const G=__DATA__;
const list=document.getElementById('glist'),q=document.getElementById('gq'),self=document.getElementById('gself'),trap=document.getElementById('gtrap'),cnt=document.getElementById('gcount'),empty=document.getElementById('gempty');
const esc=t=>t.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
list.innerHTML=G.map(([g,m,par,ln,items])=>'<section class="gsec"><h2>'+esc(g)+' <a class="gmod" href="#'+m+'">модуль '+m.slice(1)+'</a></h2><p class="tb">Учебник: '+esc(par)+' · Задания ОГЭ: '+esc(ln)+'</p><dl>'+items.map(([t,d,n])=>'<div class="gi'+(n?' hasn':'')+'" data-s="'+esc((t+' '+d+' '+n).toLowerCase())+'"><dt data-t="'+esc(t)+'">'+esc(t)+'</dt><dd data-d="'+esc(d)+'">'+esc(d)+'.</dd>'+(n?'<p class="gnote"><b>Частая ошибка.</b> '+esc(n)+'</p>':'')+'</div>').join('')+'</dl></section>').join('');
const all=[...list.querySelectorAll('.gi')];
function mark(txt,v){if(!v)return esc(txt);const low=txt.toLowerCase();let out='',i=0,k;while((k=low.indexOf(v,i))>=0){out+=esc(txt.slice(i,k))+'<mark>'+esc(txt.slice(k,k+v.length))+'</mark>';i=k+v.length}return out+esc(txt.slice(i))}
function filt(){
  const v=q.value.trim().toLowerCase();let n=0;
  all.forEach(i=>{const on=(!v||i.dataset.s.includes(v))&&(!trap.checked||i.classList.contains('hasn'));i.hidden=!on;if(on){n++;const dt=i.querySelector('dt'),dd=i.querySelector('dd');dt.innerHTML=mark(dt.dataset.t,v);dd.innerHTML=mark(dd.dataset.d,v)+'.'}});
  list.querySelectorAll('.gsec').forEach(s=>{s.hidden=![...s.querySelectorAll('.gi')].some(i=>!i.hidden)});
  empty.hidden=n>0;cnt.textContent=(v||trap.checked?'Найдено понятий: ':'Всего понятий: ')+n;
}
q.addEventListener('input',filt);trap.addEventListener('change',filt);
self.addEventListener('change',()=>{list.classList.toggle('quiz',self.checked);all.forEach(i=>i.classList.remove('show'))});
list.addEventListener('click',e=>{const dt=e.target.closest('dt');if(dt&&list.classList.contains('quiz'))dt.parentElement.classList.toggle('show')});
filt();
}
</script>
</section>
'''.replace('__DATA__',json.dumps(data,ensure_ascii=False))
open(os.path.join(D,'..','parts','n_glossary.html'),'w',encoding='utf-8').write(page)
print('terms',n,'with notes',nn)
