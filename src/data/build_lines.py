import os, sys
D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D)
from lines import L, TEXT
def li(xs): return ''.join('<li>'+x+'</li>' for x in xs)
out=['<section class="page" id="lines" data-t="Все 20 заданий" data-toc="1">',
'<h1>Все 20 заданий: как решать</h1>',
'<p class="lead">Паспорт каждой линии: что проверяют, куда и как писать ответ, алгоритм, как оценивают по критериям ФИПИ, типичные ошибки по материалам разработчиков и два образца - на полный балл и на сниженный, с объяснением. Примеры - авторские задания по модели ФИПИ.</p>',
'<p class="cap">Источники: спецификация, демоверсия и критерии ФИПИ 2027; методические рекомендации ФИПИ для обучающихся (ОГЭ 2026); статья разработчиков КИМ О.А. Котовой и Т.Е. Лисковой («Педагогические измерения», 2026, № 2).</p>']
for x in L:
    n=x['n']
    out.append(f'<h2 id="l{n}"><span class="badge{" w" if x["w"] else ""}">{n}</span>{x["title"]}</h2>')
    mods=', '.join(f'<a href="#{a}">{b}</a>' for a,b in x['mod'])
    out.append(f'<dl class="lmeta"><dt>Проверяют</dt><dd>{x["checks"]}</dd><dt>Ответ</dt><dd>{x["fmt"]}</dd><dt>Баллы</dt><dd>{x["pts"]}</dd><dt>Учебник</dt><dd>{x["tb"]}</dd><dt>Теория</dt><dd>{mods}</dd></dl>')
    out.append('<h3>Как решать</h3><ol class="steps">'+li(x['algo'])+'</ol>')
    out.append('<h3>Как оценивают</h3><ul>'+li(x['crit'])+'</ul>')
    out.append('<div class="c trap"><b class="tag">Типичные ошибки</b><ul>'+li(x['err'])+'</ul><p class="cap">Источник: '+x['err_src']+'.</p></div>')
    if n==18: out.append('<div class="txt"><p class="cap" style="text-indent:0">Текст для линий 18-20 (авторский учебный текст)</p>'+TEXT+'</div>')
    out.append('<div class="task"><p class="tr-meta"><b>Пример</b> авторское задание по модели ФИПИ</p><p>'+x['task']+'</p></div>')
    g=x['good']; b=x['bad']
    out.append(f'<div class="good"><b>Ответ на {g[0]}</b><p>{g[1]}</p></div>')
    out.append(f'<div class="bad"><b>Ответ на {b[0]}</b><p>{b[1]}</p><p><b>Почему:</b> {b[2]}</p></div>')
    out.append(f'<p><a href="#trainer" data-line="{n}" class="trlink">Тренажер: задания линии {n}</a></p>')
out.append('</section>')
open(os.path.join(D,'..','parts','p_lines.html'),'w',encoding='utf-8').write('\n'.join(out)+'\n')
print('ok', len(L))
