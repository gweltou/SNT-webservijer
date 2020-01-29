#!/usr/bin/env python3

import random
import html

from update_index import *


def dre_anv_html(anviou):
    html_text = ""
    
    html_text = "<ul>\n"
    for anv, da_prizian in anviou:
        html_text += "  <li>" + html.escape(str(anv)) + "</li>\n"
        html_text += "  <ul>\n"
        for strollad in da_prizian:
            html_text += "    <li>" + html.escape(str(strollad)) + "</li>\n"
        
        html_text += "  </ul>\n"
    
    html_text += "</ul>\n"
    
    return html_text



if __name__ == "__main__":
    strolladou = []
    
    """
    klas = None
    
    with open(NOTES_FILE, "r") as f:
        lines = f.readlines()
    
    for l in lines:
        if not l.strip():
            continue
        if l.startswith('#'):
            klas = l[1:].strip()
        else:
            anviou = l.split(';')[0]
            anviou = [s.strip() for s in anviou.split('&')]
            strolladou.append((tuple(anviou), klas))
    random.shuffle(strolladou)
    """
    
    files_list = [f for f in list_files_in(ROOT_FOLDER) if is_html(f)]
    pages = parse_pages(files_list)
    print("Niver a bajennoù :", len(pages))
    strolladou = [(p["author"], p["group"]) for p in pages]
    print("Niver a strolladoù :", len(set(strolladou)))
    
    liseidi = []
    for anviou, klas in strolladou:
        for anv in anviou:
            liseidi.append((anv, anviou, klas))
    
    print("Niver a liseidi :", len(liseidi))
    
    
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
    
    #print(dre_anv_html(prizi_anv))
    
    
