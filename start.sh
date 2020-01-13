#! /bin/bash

cd /home/pi/SNT-webservijer

echo "executing: python3 my_html_parser.py"
python3 my_html_parser.py

echo "executing: sudo python3 -m http.server 80 &"
sudo python3 -m http.server 80 &
sleep 2

cd /home/pi/kaoz
echo "executing: python3 servijer.py 8001 &"
python3 servijer.py 8001 &

