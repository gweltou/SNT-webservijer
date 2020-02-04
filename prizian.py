#!/usr/bin/env python3

import random
import html

from update_index import *


HTML_HEADER = """
<!DOCTYPE html>
<html>
<head>
  <title>Prizia&ntilde;</title>
  <meta charset="UTF-8">
  <link rel="stylesheet" type="text/css" href="prizian.css">
</head>
<body lang="br">
"""


def dre_anv_html(anviou):
    html_text = HTML_HEADER
    last_group = None
    anviou = sorted(anviou, key=lambda f:f[0][2])
    for anv, da_prizian in anviou:
        if anv[2] != last_group:
            if last_group != None:
                html_text += "</ul>\n"
            last_group = anv[2]
            html_text += "  <h2>" + anv[2].capitalize() + "</h2>\n"
            html_text += "  <ul>\n"
        html_text += "    <li class=\"dropdown\">" + html.escape("{} ({})".format(anv[0], ' & '.join(anv[1]))) + "</li>\n"
        html_text += "    <ul class=\"dropdown-content\">\n"
        for pajenn in da_prizian:
            titl = pajenn[2] if pajenn[2] else "Titl ebet"
            html_text += "      <li><a href=\"" + pajenn[3] + "\">" + html.escape(titl) + "</a></li>\n"
        
        html_text += "    </ul>\n"
    
    html_text += "</ul>\n"
    html_text += "</body></html>"
    
    return html_text


def dre_strollad_html(groups_dict):
    html_text = HTML_HEADER
    strolladou = sorted(groups_dict.keys(), key=lambda f:f[1])
    last_group = None
    for s in strolladou:
        if s[1] != last_group:
            if last_group != None:
                html_text += "</ul>\n"
            last_group = s[1]
            html_text += "  <h2>" + s[1].capitalize() + "</h2>\n"
            html_text += "  <ul>\n"
        group = " & ".join(s[0])
        title = s[2] if s[2] else "Titl ebet"
        html_text += "    <li class=\"dropdown\"><a href=\"{}\">{}</a> ({})</li>\n".format(s[3], title, html.escape(group))
        html_text += "    <ul class=\"dropdown-content\">\n"
        for anv, strollad, klas in groups_dict[s]:
            html_text += "      <li>{} ({}) {}</li>\n".format(anv, ' & '.join(strollad), klas.capitalize())
        
        html_text += "    </ul>\n"
    
    html_text += "</ul>\n"
    html_text += "</body></html>"
    
    return html_text


if __name__ == "__main__":
    strolladou = []
    
    files_list = [f for f in list_files_in(ROOT_FOLDER) if is_html(f)]
    pages = parse_pages(files_list)
    print("Niver a bajennoù :", len(pages))
    strolladou = [(p["author"], p["group"], p["title"], p["filename"]) for p in pages if p["author"][0] not in ("Laure", "Gweltaz")]
    n_strolladou = len(set(strolladou))
    print("Niver a strolladoù :", n_strolladou)
    if n_strolladou != len(pages):
        # Check for duplicates
        strolladou_sorted = sorted(strolladou)
        for i in range(1, len(strolladou)):
            if strolladou_sorted[i][0] == strolladou_sorted[i-1][0]:
                print(strolladou_sorted[i-1])
                print(strolladou_sorted[i])
    
    liseidi = []
    for anviou, klas, _, _ in strolladou:
        for anv in anviou:
            liseidi.append((anv, anviou, klas))
    
    print("Niver a liseidi :", len(liseidi))
    
    random.shuffle(strolladou)
    
    prizi_anv = []
    prizi_strollad = {}
    idx = 0
    for anv, anviou, klas in liseidi:
        da_prizian = []
        for n in range(5):
            if strolladou[idx%len(strolladou)][0] == anviou:
                idx += 1
            strollad = strolladou[idx%len(strolladou)]
            da_prizian.append(strollad)
            
            if strollad in prizi_strollad:
                prizi_strollad[strollad].append((anv, anviou, klas))
            else:
                prizi_strollad[strollad] = [(anv, anviou, klas)]
            idx += 1
        
        prizi_anv.append([(anv, anviou, klas), da_prizian])
    
    """
    for strollad in prizi_strollad:
        print(strollad)
        for anv in prizi_strollad[strollad]:
            print("   ", anv)
    """
    
    with open("prizian_dre_lisead.html", "w") as f:
        f.write(dre_anv_html(prizi_anv))
    
    with open("prizian_dre_strollad.html", "w") as f:
        f.write(dre_strollad_html(prizi_strollad))

