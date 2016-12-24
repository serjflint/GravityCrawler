import random
import time

import requests
from bs4 import BeautifulSoup
from progressbar import Bar, FormatLabel, ProgressBar, ETA

name = "Novel name"  # Put the name of the novel here
url = "http://gravitytales.com/novel/novel_name/novel-chapter-"  # Replace by url to the chapter except the number
last_chapter = 99  # Set last chapter to download

html = """
<head>
    <title>{}</title>
</head>
<body>
""".format(name)

widgets = [
    FormatLabel('%(value)d of %(max_value)d'),
    ' ', Bar(marker='>', left='[', right=']'),
    ' ', ETA(),
]

pbar = ProgressBar(widgets=widgets, max_value=last_chapter).start()

for i in range(1, last_chapter):
    r = requests.get(url + str(i))
    soup = BeautifulSoup(r.text, 'html.parser')
    innerContent = soup.find("div", {"class": "innerContent"})
    for match in innerContent.findAll('span'):
        match.unwrap()
    paragraphs = innerContent.findAll('p')

    header = paragraphs[1].text
    chapter = "\t<h1>{}</h1>\n".format(header)
    for p in paragraphs:
        if p.name == "p" and not p.has_attr('style'):
            chapter += "\t" + str(p) + "\n"

    time.sleep(random.random())
    pbar.update(i)
    html += chapter

pbar.finish()

html += "\n</body>"

with open(name + ".html", "w", encoding="utf-8") as html_file:
    html_file.write(html)
