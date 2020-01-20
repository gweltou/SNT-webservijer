#!/usr/bin/env python3

import re
from os import walk
import os.path
import html


ROOT_FOLDER = "pajennou"

pattern_title =     r"<title>(.+)</title>"
pattern_author =    r"<meta\s+name\s*=\s*\"author\"\s+content\s*=\s*\"(.+)\"\s*>"
pattern_h =         r"<h[1-6]>(.+)</h[1-6]>"
pattern_p =         r"<p>(.+)</p>"
pattern_img =       r"<img\s(.+)>"
pattern_a =         r"<a\s+.*href=\"(.+)\".*>.+</a>"


HTML_HEADER = """
<!DOCTYPE html>

<html>
<head>
  <title>Lec'hienn Web an eilveidi</title>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="10">

  <link rel="stylesheet" type="text/css" href="index_style.css">
  <link href="https://fonts.googleapis.com/css?family=Abril+Fatface|Open+Sans|Special+Elite|Ubuntu&display=swap" rel="stylesheet"> 
</head>
<body lang="br">
  <div id="upload-container">
    <strong id="upload-text">Pellgas ur bajenn</strong>
    <strong id="upload-arrow">&#x00BB;</strong>
    <a href="#" id="upload-link" target="_blank"><img src="images/upload.png" height="64"></a></a>
  </div>
  <h1>Pajenno&ugrave; krouet ganeomp</h1>
  <div class='summary'>
"""


def list_files_in(directory):
    list_files = []
    
    for dirpath, dirnames, filenames in walk(directory):
        for filename in filenames:
            list_files.append(os.path.join(dirpath, filename))
    
    return list_files


def list_files_by_subdirs(directory):
    files = list_files_in(directory)
    subdir = []
    
    dirname = ""
    content = []
    for f in files:
        d = f.split(os.path.sep)[1]
        if d != dirname:
            if content: subdir.append(content)
            content = [f]
            dirname = d
        else:
            content.append(f)
    
    subdir.append(content)
    
    return subdir


def filter_out_script_tag(filename):
    text = ""
    with open(filename, "rb") as f:
        text = f.read()
    
    m = re.search(rb"<script.*main\.js.*</script>", text)
    if m:
        text = text[:m.start()] + text[m.end():]
        print("script tag removed from", filename)
    
    with open(filename, "wb") as f:
        f.write(text)


def parse_html_file(filename):
    d = dict()
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read().strip()
    except UnicodeDecodeError:
        with open(filename, "r", encoding="latin-1") as f:
            text = f.read().strip()
    
    # Check for DOCTYPE tag
    d["doctype"] = True if text.startswith(r"<!DOCTYPE html>") else False
    
    # Check for HTML, HEAD and BODY tags
    d["html_tags"] = True if re.search(r"<html>.*</html>", text, flags=re.DOTALL) else False
    d["head_tags"] = True if re.search(r"<head>.*</head>", text, flags=re.DOTALL) else False
    d["body_tags"] = True if re.search(r"<body.*>.*</body>", text, flags=re.DOTALL) else False
    
    m = re.findall(pattern_title, text, re.UNICODE)
    if len(m) > 0:
      d["title"] = m[0].strip()
    else:
      d["title"] = None
    
    m = re.findall(pattern_author, text)
    if len(m) > 0:
      d["author"] = m[0].strip()
    else:
      d["author"] = None
    
    m = re.findall(pattern_p, text)
    d["number_p"] = len(m)
    d["number_words"] = 0
    for p in m:
        d["number_words"] += len(p.split())
    
    m = re.findall(pattern_img, text)
    d["number_img"] = len(m)
    
    m = re.findall(pattern_a, text)
    d["number_a"] = len(m)
    
    return d
    

def update_page():
    evezhiadennou = dict()
    if os.path.exists("evezhiadennou.txt"):
        with open("evezhiadennou.txt", "r") as f:
            lines = f.readlines()
        
        for l in lines:
            l = l.strip()
            if not l or l.startswith('#'):
                continue
            strollad, evezhiadenn = l.split(';')
            evezhiadennou[strollad.strip()] = evezhiadenn.strip()
    
    pages = dict()
    group_of_files = list_files_by_subdirs(ROOT_FOLDER)
    for files in group_of_files:
        for f in files:
            pages[f] = parse_html_file(f)
    
    text = HTML_HEADER
    
    # Pajennoù liseidi
    for files in group_of_files:
        text += "<div class='column'>\n"
        group_name = files[0].split(os.path.sep)[1]
        text += "<h2 class='group-title {}'>".format(group_name) + group_name + "</h3>\n"
        text += "<ul>\n"
        for f in sorted(files):
            if not f.lower().endswith(".html"):
                continue
            
            text += "<li>"
            text += f"<a class='page-title' href=\"{f}\" target=\"_blank\">{pages[f]['title']}</a><br>"
            text += "</li>\n"
        
        text += "</ul>\n"
        text += "</div>\n\n"
    
    text += "</div>\n"
    
    # Ostilhoù
    text += """
    <h1>Kentelioù</h1>
    <ul id="kenteliou">
      <li><a href="HTML.html" target="_blank">Ar gentel HTML e brezhoneg</a></li>
      <li><a href="CSS.html" target="_blank">Ar gentel CSS e brezhoneg</a></li>
      <li>Evit mon pelloc'h gant HTML ha CSS (e saozneg) : <a href="https://www.w3schools.com/" target="_blank">www.w3school.com</a></li>
    </ul>
    <h1>Ostilhoù</h1>
    <ul id="ostilhou">
      <li class="tooltip"><a href="https://html5-editor.net/" target="_blank">html5-editor.net</a><span class="tooltiptext">Evit skriva&ntilde; HTML nemetken</span></li>
      <li class="tooltip"><a href="https://liveweave.com/" target="_blank">liveweave.com</a><span class="tooltiptext">Evit skriva&ntilde; HTML ha CSS, labourat war 2 urzhiataer posupl</span></li>
      <li class="tooltip"><a href="https://fonts.google.com/" target="_blank">Google Fonts</a><span class="tooltiptext">Stilo&ugrave; skritur Google da zibab (CSS)</span></li>
      <li class="tooltip"><a id="kaoz-link" target="_blank" href="#">Kaoz</a><span class="tooltiptext">Chat lec'hel enlinenn home-made</span></li>
      <li class="tooltip"><input type="color" id="html5colorpicker" onchange="clickColor(0, -1, -1, 5)" value="#FF9D00" style="width:100px;"><span class="tooltiptext">Evit dibab livio&ugrave;</span></li>
    </ul>
    """
    
    text += """
    <h1>Statistiko&ugrave;</h1>
    <table>
      <tr>
        <th class="tooltip">URL<span class="tooltiptext">Anv ar fichennaoueg a rank echui&ntilde; gant .html</span></th>
        <th class="tooltip">Oberourien<span class="tooltiptext">Merken &lt;meta name="author" content="..."&gt;</span></th>
        <th class="tooltip">Doctype<span class="tooltiptext">&lt;DOCTYPE!&gt; e penn-kenta&ntilde; an teuliad HTML</span></th>
        <th class="tooltip">Framm HTML<span class="tooltiptext">Kavet e vez ar framm<pre style="text-align:left;">  &lt;html&gt;\n    &lt;head&gt;\n    &lt;/head&gt;\n    &lt;body&gt;\n    &lt;/body&gt;\n  &lt;/html&gt;</pre></span></th>
        <th class="tooltip">Titl<span class="tooltiptext">Kavet e vez an elfenno&ugrave; &lt;title&gt;...&lt;/title&gt;</span></th>
        <th class="tooltip">Pennad<span class="tooltiptext">Pennado&ugrave; skrid<br>&lt;p&gt;...&lt;/p&gt;</span></th>
        <th class="tooltip">Gerioù<span class="tooltiptext">Niver a gerio&ugrave; en holl pennado&ugrave; skrid</span></th>
        <th class="tooltip">Skeudenn<span class="tooltiptext">Skeudenno&ugrave;<br>&lt;img src="..."&gt;</span></th>
        <th class="tooltip">Hiperliamm<span class="tooltiptext">Liammo&ugrave; hiperskrid<br>&lt;a href="..."&gt;&nbsp;...&nbsp;&lt;/a&gt;</span></th>
        <th>Evezhiadenno&ugrave;</th>
      </tr>
    """
    
    for f in sorted(pages):
        p = pages[f]
        text += "<tr>\n"
        if f.lower().endswith(".html") or f.lower().endswith(".htm"):
            text += "<td>"
            text += f"<a href=\"{f}\" target=\"_blank\">"
            text += html.escape(f)
            text += "</a></td>\n"
        else:
            text += "<td style=\"background-color:#FBA\">"
            text += f"<a href=\"{f}\">"
            text += html.escape(f)
            text += "</a></td>\n"
        
        if p["author"]:
            text += f'<td style="background-color:#99FF99">{p["author"]}</td>'
        else:
            text += "<td style=\"background-color:#FBA\">Goulo</td>"
        
        if p["doctype"]:
            text += "<td style=\"background-color:#99FF99\">Mat</td>"
        else:
            text += "<td style=\"background-color:#FBA\">Kudenn</td>"
        
        if p["html_tags"] and p["head_tags"] and p["body_tags"]:
            text += "<td style=\"background-color:#99FF99\">Mat</td>"
        else:
            text += "<td style=\"background-color:#FBA\">Kudenn</td>"
        
        if p["title"] != None:
            text += f"<td>{html.escape(p['title'])}</td>"
        else:
            text += "<td style=\"background-color:#FBA\">Titl ebet</td>"
        
        text += f"<td>{p['number_p']}</td>"
        
        text += f"<td>{p['number_words']}</td>"
        
        text += f"<td>{p['number_img']}</td>"
        
        text += f"<td>{p['number_a']}</td>"
        
        if p['author'] in evezhiadennou:
            text += f"<td>{html.escape(evezhiadennou.get(p['author']))}</td>"
        
        text += "</tr>\n"
    
    text += """
    </table>
    
    <script type="application/javascript">
      document.getElementById('upload-link').href = "http://" + document.domain + ":8000/";
      document.getElementById('kaoz-link').href = "http://" + document.domain + ":8001/";
    </script>
  </body>
</html>
"""
    
    with open("index.html", "w") as f_out:
        f_out.write(text)
        print("Index.html file updated")


if __name__ == "__main__":
    update_page()
    
    
    
