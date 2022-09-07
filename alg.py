import requests
import bs4
import re

word = input("調べたいこと:")
url = 'https://ja.wikipedia.org/wiki/'+word

res = requests.get(url)
soup = bs4.BeautifulSoup(res.text, "html.parser")

# toc_all = soup.select('.toc a')
toc_all = soup.select('.sidebar-toc-list-item a')

toc_display = []
for i in toc_all:
  toc_display.append(i.get_text())

for i,j in enumerate(toc_display):
  print(j + "……" + str(i))

toc_all_list = []
for a in toc_all:
  toc_all_list.append(a['href'])

toclevel1 = soup.select('.sidebar-toc-level-1 a')
toclevel2 = soup.select('.sidebar-toc-level-2 a')
toclevel3 = soup.select('.sidebar-toc-level-3 a')
toclevel4 = soup.select('.sidebar-toc-level-4 a')

toc1_list = []
for a in toclevel1:
  toc1_list.append(a['href'])

toc2_list = []
for a in toclevel2:
     toc2_list.append(a['href'])

toc3_list = []
for a in toclevel3:
     toc3_list.append(a['href'])

toc4_list = []
for a in toclevel4:
     toc4_list.append(a['href'])

for i in toc4_list:
  if i in toc3_list:
    toc3_list.remove(i)
    toc2_list.remove(i)
    toc1_list.remove(i)

for i in toc3_list:
  if i in toc2_list:
    toc2_list.remove(i)
    toc1_list.remove(i)

for i in toc2_list:
  if i in toc1_list:
    toc1_list.remove(i)

#-----ここまで目次ゲット機能-------

selected_chapter = int(input("どの項目を聞くか？"))

text_list = []
for t in soup.find_all(['h2','h3','p']):
  text_list.append(str(t))

text = " ".join(text_list)

start = toc_all_list[selected_chapter].replace("#","")

if toc_all_list[selected_chapter] in toc1_list:
  end = toc1_list[toc1_list.index(toc_all_list[selected_chapter])+1].replace("#","")

if toc_all_list[selected_chapter] in toc2_list:
  end = toc2_list[toc2_list.index(toc_all_list[selected_chapter])+1].replace("#","")

if toc_all_list[selected_chapter] in toc3_list:
  end = toc3_list[toc3_list.index(toc_all_list[selected_chapter])+1].replace("#","")

if toc_all_list[selected_chapter] in toc4_list:
  end = toc4_list[toc4_list.index(toc_all_list[selected_chapter])+1].replace("#","")

text = text.replace('<span class="mw-headline" id="'+start+'">','--><span class="mw-headline" id=' + start + '">')
text = text.replace('<span class="mw-headline" id="'+ end +'">','<!--<span class="mw-headline" id=' + end + '">')

s = "<!--" + text + "-->"
draft =bs4.BeautifulSoup(s,"html.parser")

manuscript = draft.text
perfect = re.sub('\[.*?\]','',manuscript)
print(perfect)