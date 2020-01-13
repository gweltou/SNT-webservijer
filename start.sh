#! /bin/bash

cd /home/pi/SNT-webservijer
python3 my_html_parser.py
sudo python3 -m http.server 80 &

cd /home/pi/kaoz
python3 servijer.py 8001 &

