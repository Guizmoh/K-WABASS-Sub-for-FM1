#!/usr/bin/env python3
"""Adds a version to the "Latest updates" of index.html / fr/index.html: the newest four in full, the rest folded.
   python3 source/tools/add_news.py 0.9.36 "english point · another" "point français · un autre"   (from the repo root)"""
import re, sys
v, en, fr = sys.argv[1:4]
for p, txt in (("index.html", en), ("fr/index.html", fr)):
    s = open(p).read()
    a = s.index('<ol class="news">') + len('<ol class="news">\n')
    s = s[:a] + '<li><span class="v">%s</span><ul>%s</ul></li>\n' % (v, "".join("<li>%s</li>" % x.strip() for x in txt.split(" · "))) + s[a:]
    full = re.findall(r'<li><span class="v">[^<]*</span><ul>.*?</ul></li>\n', s[s.index('<ol class="news">'):s.index('</ol>', s.index('<ol class="news">'))], re.S)
    if len(full) > 4:                        # the fifth goes to the folded list, as one line
        last = full[-1]
        s = s.replace(last, "", 1)
        m = re.match(r'<li><span class="v">([^<]*)</span><ul>(.*?)</ul></li>', last, re.S)
        one = '<li><span class="v">%s</span><div>%s</div></li>\n' % (m.group(1), " · ".join(re.findall(r"<li>(.*?)</li>", m.group(2), re.S)))
        b = s.index('<ol class="news old">\n') + len('<ol class="news old">\n')
        s = s[:b] + one + s[b:]
        s = re.sub(r'(<summary>[^<(]*\()(\d+)(\)</summary>)', lambda k: k.group(1) + str(int(k.group(2)) + 1) + k.group(3), s, count=1)
    open(p, "w").write(s)
print("news", v)
