import re, glob, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAV = [
    ("Начало", [("start", "", "Старт: карта и расписание"), ("m0", "0", "Как устроен экзамен")]),
    ("Темы", [("m1", "1", "Человек и общество"), ("m2", "2", "Группы, нормы, семья"), ("m3", "3", "Ценности и Россия"),
              ("m4", "4", "Культура"), ("m5", "5", "Экономика"), ("m6", "6", "Финансовая грамотность"),
              ("m7", "7", "Государство и политика"), ("m8", "8", "Власть в РФ и гражданин"), ("m9", "9", "Право")]),
    ("Практика", [("lines", "", "Все 20 заданий: как решать"), ("trainer", "", "Тренажер по линиям"), ("m10", "10", "Фото, статистика, 14, 17"), ("m11", "11", "Работа с текстом"), ("m12", "12", "Пробники и финал")]),
    ("Итог", [("glossary", "", "Словарь определений"), ("progress", "", "Прогресс и карта заданий")]),
]
parts = sorted(glob.glob("parts/*.html"))
html = "\n".join(open(p, encoding="utf-8").read() for p in parts)
ids = set(re.findall(r'<section class="page" id="([^"]+)"', html))
nav = []
for grp, items in NAV:
    nav.append(f"<h4>{grp}</h4>")
    for pid, n, label in items:
        if pid not in ids:
            continue
        nav.append(f'<a href="#{pid}"><span class="n">{n}</span><span>{label}</span><span class="d"></span></a>')
tpl = open("template.html", encoding="utf-8").read()
out = tpl.replace("<!--NAV-->", "\n".join(nav)).replace("<!--PAGES-->", html)
bad = [(m.start(), out[max(0, m.start()-40):m.start()+40]) for m in re.finditer("[—–]", out)]
if bad:
    print("DASHES FOUND:", len(bad))
    for b in bad[:20]:
        print(repr(b[1]))
# broken internal links
for h in set(re.findall(r'href="#([^"]+)"', out)):
    if h not in ids and not re.search(r'id="%s"' % re.escape(h), out):
        print("BROKEN LINK #" + h)
open(os.path.join("..", "index.html"), "w", encoding="utf-8").write(out)
print("pages:", sorted(ids), "size:", len(out))
