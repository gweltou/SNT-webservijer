#!/usr/bin/env python3

import re
from os import walk
import os.path
import html


ROOT_FOLDER = "pajennou"
NOTES_FILE = "evezhiadennou.txt"
UPLOAD_SERVERS = {  "gwenn1": "8000",
                    "gwenn2": "8001",
                    "ruz1"  : "8002",
                    "ruz2"  : "8003",
                    "du"    : "8004",
                    "glas"  : "8005",
                    "kelennerien": "8006",
                  }

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
  
  <link rel="stylesheet" type="text/css" href="index_style.css">
  <link href="https://fonts.googleapis.com/css?family=Abril+Fatface|Open+Sans|Special+Elite|Ubuntu&display=swap" rel="stylesheet"> 
</head>
<body lang="br">
  <h1>Pajenno&ugrave; krouet ganeomp</h1>
  <div class='summary'>
"""



def list_files_in(directory, depth=2):
    list_files = []
    
    for dirpath, dirnames, filenames in walk(directory):
        if len(dirpath.split(os.path.sep)) > depth:
            continue
        for filename in filenames:
            list_files.append(os.path.join(dirpath, filename))
    
    return list_files


def list_files_by_subdirs(files_list):
    subdir = []
    dirname = ""
    content = []
    for f in files_list:
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
    d["filename"] = filename
    d["group"] = filename.split(os.path.sep)[1]
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read().strip()
    except UnicodeDecodeError:
        with open(filename, "r", encoding="latin-1") as f:
            text = f.read().strip()
    
    # Check for DOCTYPE tag
    d["doctype"] = True if re.search(r"^<!DOCTYPE html>", text) else False
    
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
      # d["author"] = m[0].strip()
      d["author"] = tuple(sorted([n.strip().capitalize() for n in m[0].split('&')]))
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
    

def parse_pages(files):
    pages = []
    
    for f in files:
        pages.append(parse_html_file(f))
    
    return pages


def parse_evezhiadennou():
    evezhiadennou = dict()
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            lines = f.readlines()
        
        for l in lines:
            l = l.strip()
            if not l or l.startswith('#'):
                continue
            strollad, evezhiadenn = l.split(';')
            strollad = tuple(sorted([n.strip().capitalize() for n in strollad.split('&')]))
            evezhiadennou[strollad] = evezhiadenn.strip()
    
    return evezhiadennou


def is_html(filename):
    return filename.lower().endswith('.html') or filename.lower().endswith('.htm')
    

def update_index_page():
    all_files = list_files_in(ROOT_FOLDER)
    html_files = [f for f in all_files if is_html(f)]
    group_of_files = [[f for f in sub] for sub in list_files_by_subdirs(html_files)]
    
    pages = parse_pages(html_files)
    file_to_page = dict()
    for p in pages:
        file_to_page[p["filename"]] = p
    
    evezhiadennou = parse_evezhiadennou()
    
    text = HTML_HEADER
    
    # Pajennoù liseidi
    group_names = []
    for files in group_of_files:
        text += "    <div class='column'>\n"
        group_name = files[0].split(os.path.sep)[1]
        group_names.append(group_name)
        text += "      <h2 class='group-title {}'>".format(group_name) + group_name + "</h2>\n"
        text += "      <ul>\n"
        for f in sorted(files):
            text +=  "        <li>"
            text += f'<a class="page-title" href="{f}" target="_blank">{file_to_page[f]["title"]}</a><br>'
            text +=  "</li>\n"
        
        text += "      </ul>\n"
        text += "    </div>\n"
    
    text += "  </div>\n\n"
    
    # Upload links
    text += """  <div id="upload-container">
    <strong id="upload-text">Pellgas ur bajenn</strong>
    <strong id="upload-arrow">&#x00BB;</strong>
    <div id="upload-links-container">
      <ul>
"""
    
    for group_name in sorted(group_names):
        text += "       <li><a href='#' id='upload-link-{}' class='upload-link {}' target='_blank'>{}</a></li>\n".format(group_name, group_name, group_name)
    
    text += """      </ul>
    </div>
  </div>
"""
    
    ### Kenteliou
    text += """
    <h1>Kentelioù</h1>
    <ul class="liammou">
      <li><a href="HTML.html" target="_blank">Ar gentel HTML e brezhoneg</a></li>
      <li><a href="CSS.html" target="_blank">Ar gentel CSS e brezhoneg</a></li>
      <li>Evit mon pelloc'h gant HTML ha CSS (e saozneg) : <a href="https://www.w3schools.com/" target="_blank">www.w3school.com</a></li>
    </ul>"""
    
    ### Ostilhoù
    text += """
    <h1>Ostilhoù</h1>
    <ul class="liammou">
      <li class="tooltip"><a href="https://html5-editor.net/" target="_blank">html5-editor.net</a><span class="tooltiptext">Evit skriva&ntilde; HTML nemetken</span></li>
      <li class="tooltip"><a href="https://liveweave.com/" target="_blank">liveweave.com</a><span class="tooltiptext">Evit skriva&ntilde; HTML ha CSS, labourat war 2 urzhiataer posupl</span></li>
      <li class="tooltip"><a href="https://fonts.google.com/" target="_blank">Google Fonts</a><span class="tooltiptext">Stilo&ugrave; skritur Google da zibab (CSS)</span></li>
      <li class="tooltip"><a href="https://www.w3schools.com/cssref/css_colors.asp" target="_blank">Livio&ugrave; CSS</a><span class="tooltiptext">Evit dibab livio&ugrave;</span></li>
      <li class="tooltip"><a id="kaoz-link" target="_blank" href="#">Kaoz</a><span class="tooltiptext">Chat lec'hel enlinenn home-made</span></li>
    </ul>
    """
    
    ### Priziañ
    if os.path.exists("prizian_dre_lisead.html"):
        text += """
    <h1>Prizia&ntilde;</h1>
    <ul class="liammou">
      <li><a href="prizian_dre_lisead.html" target="_blank">Piv a prizio peseurt strollad ?</a></li>
    </ul>
    """
    
    ### DIAGNOSTIC TABLE
    text += """
    <h1>Statistiko&ugrave;</h1>
    <table>
      <tr>
        <th class="tooltip">URL<span class="tooltiptext">Anv ar fichennaoueg a rank echui&ntilde; gant .html</span></th>
        <th class="tooltip">Oberourien<span class="tooltiptext">Merken &lt;meta name="author" content="..."&gt;</span></th>
        <th class="tooltip">Titl<span class="tooltiptext">Kavet e vez an elfenno&ugrave; &lt;title&gt;...&lt;/title&gt;</span></th>
        <th class="tooltip">Doctype<span class="tooltiptext">&lt;!DOCTYPE html&gt; e penn-kenta&ntilde; an teuliad HTML</span></th>
        <th class="tooltip">Framm HTML<span class="tooltiptext">Kavet e vez ar framm<pre style="text-align:left;">  &lt;html&gt;\n    &lt;head&gt;\n    &lt;/head&gt;\n    &lt;body&gt;\n    &lt;/body&gt;\n  &lt;/html&gt;</pre></span></th>
        <th class="tooltip">Pennad<span class="tooltiptext">Pennado&ugrave; skrid<br>&lt;p&gt;...&lt;/p&gt;</span></th>
        <th class="tooltip">Gerioù<span class="tooltiptext">Niver a gerio&ugrave; en holl pennado&ugrave; skrid</span></th>
        <th class="tooltip">Skeudenn<span class="tooltiptext">Skeudenno&ugrave;<br>&lt;img src="..."&gt;</span></th>
        <th class="tooltip">Hiperliamm<span class="tooltiptext">Liammo&ugrave; hiperskrid<br>&lt;a href="..."&gt;&nbsp;...&nbsp;&lt;/a&gt;</span></th>
        <th>Evezhiadenno&ugrave;</th>
      </tr>
    """
    
    for f in sorted(all_files):
        text += "<tr>\n"
        
        if is_html(f):
            text += "<td>"
            text += f"<a href=\"{f}\" target=\"_blank\">"
            text += html.escape(f)
            text += "</a></td>\n"
        else:
            text += "<td style=\"background-color:#FBA\">"
            text += f"<a href=\"{f}\">"
            text += html.escape(f)
            text += "</a></td>\n"
        
        if f in file_to_page:
            p = file_to_page[f]
            
            if p["author"]:
                names = p["author"][0] if len(p["author"]) == 1 else " & ".join(p["author"])
                text += f'<td style="background-color:#99FF99">{names}</td>'
            else:
                text += "<td style=\"background-color:#FBA\">Goulo</td>"
            
            if p["title"] != None:
                text += f"<td>{html.escape(p['title'])}</td>"
            else:
                text += "<td style=\"background-color:#FBA\">Titl ebet</td>"
            
            if p["doctype"]:
                text += "<td style=\"background-color:#99FF99\">Mat</td>"
            else:
                text += "<td style=\"background-color:#FBA\">Kudenn</td>"
            
            if p["html_tags"] and p["head_tags"] and p["body_tags"]:
                text += "<td style=\"background-color:#99FF99\">Mat</td>"
            else:
                text += "<td style=\"background-color:#FBA\">Kudenn</td>"
            
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
"""
    
    for folder_name in group_names:
        text += f"""      document.getElementById('upload-link-{folder_name}').href = 'http://' + document.domain + ':{UPLOAD_SERVERS[folder_name]}/';\n"""
    
    text += """
      document.getElementById('kaoz-link').href = "http://" + document.domain + ":8100/";
      
      function openInNewTab(url) {
        var win = window.open(url, '_blank');
        win.focus();
      }
    </script>
  </body>
</html>
"""
    
    with open("index.html", "w") as f_out:
        f_out.write(text)
        print("Index.html file updated")


if __name__ == "__main__":
    update_index_page()
    
