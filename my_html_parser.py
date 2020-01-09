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



def list_files_in(directory):
    list_files = []
    
    for dirpath, dirnames, filenames in walk(directory):
        for filename in filenames:
            if filename.lower().endswith(".html"):
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


def parse_html_file(filename):
    d = dict()
    
    with open(filename, "r", encoding="latin-1") as f:
        text = f.read().strip()
    
    # Check for DOCTYPE tag
    d["doctype"] = True if text.startswith(r"<!DOCTYPE html>") else False
    
    # Check for HTML, HEAD and BODY tags
    d["html_tags"] = True if re.search(r"<html>.*</html>", text, flags=re.DOTALL) else False
    d["head_tags"] = True if re.search(r"<head>.*</head>", text, flags=re.DOTALL) else False
    d["body_tags"] = True if re.search(r"<body.*>.*</body>", text, flags=re.DOTALL) else False
    
    m = re.findall(pattern_title, text)
    if len(m) > 0:
      d["title"] = m[0].strip()
    else:
      d["title"] = None
    
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
    pages = dict()
    group_of_files = list_files_by_subdirs(ROOT_FOLDER)
    for files in group_of_files:
        for f in files:
            pages[f] = parse_html_file(f)
    
    text = "<!DOCTYPE html>\n"
    text += "<html>\n"
    text += "<head>\n"
    text += "<title>Pajenn degemer lec'hienn Web an eilveidi</title>\n"
    text += "<meta charset=\"UTF-8\">\n"
    
    text += "<style>\n"
    text += ".summary {height: 800px; display:flex; flex-direction:column; flex-wrap:wrap;}\n"
    text += ".column {width:300px;}\n"
    text += ".gwenn1 {color:#222; background-color:#EEE;}\n"
    text += ".gwenn2 {color:#222; background-color:#DDD;}\n"
    text += ".ruz1 {color:#FFF; background-color:#E42;}\n"
    text += ".ruz2 {color:#FFF; background-color:#E24;}\n"
    text += ".du {color:#EEE; background-color:#111;}\n"
    text += ".glas {color:#FFF; background-color:#29E;}\n"
    text += "</style>\n"
    
    text += "</head>\n"
    text += "<body lang=\"br\">\n"
    
    text += "<h1>Pajenn degemer</h1>\n"
    
    text += "<div class='summary'>\n"
    
    for files in group_of_files:
        text += "<div class='column'>\n"
        group_name = files[0].split(os.path.sep)[1]
        text += "<h2 class='group-title {}'>".format(group_name) + group_name + "</h3>\n"
        text += "<ul>\n"
        for f in sorted(files):
            text += "<li>"
            text += f"<a class='page-title' href=\"{f}\">{pages[f]['title']}</a><br>"
            text += "</li>\n"
        
        text += "</ul>\n"
        text += "</div>\n\n"
    
    text += "</div>\n"
    
    text += "<h1>Statistiko&ugrave;</h1>\n"
    text += "<table>\n"
    text += "<tr>\n"
    text += "<th>URL</th><th>Doctype</th><th>Framm HTML</th><th>Titl</th><th>Pennadoù</th><th>Gerioù</th><th>Skeudennoù</th><th>Hiperliammoù</th>\n"
    text += "</tr>\n"
    
    for f in sorted(pages):
        p = pages[f]
        text += "<tr>\n"
        if f.lower().endswith(".html"):
            text += "<td>"
            text += f"<a href=\"{f}\">"
            text += html.escape(f)
            text += "</a></td>\n"
        else:
            text += "<td style=\"background-color:#FBA\">"
            text += f"<a href=\"{f}\">"
            text += html.escape(f)
            text += "</a></td>\n"
        
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
        
        text += "</tr>\n"
    
    text += "</table>\n"
    text += "</body>\n"
    text += "</html>"
    
    with open("index.html", "w") as f_out:
        f_out.write(text)
        print("Index.html file updated")


if __name__ == "__main__":
    update_page()
    
    
    
