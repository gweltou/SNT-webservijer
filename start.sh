#! /bin/bash

cd /home/pi/SNT-webservijer

echo "executing: python3 my_html_parser.py"
python3 my_html_parser.py

echo "executing: sudo python3 -m http.server 80 &"
sudo python3 -m http.server 80 &
sleep 2


echo "executing: python3 droopy.py -d pajennou/gwenn1 8000 &"
python3 droopy.py -d pajennou/gwenn1 8000 &
sleep 1

echo "executing: python3 droopy.py -d pajennou/gwenn2 8001 &"
python3 droopy.py -d pajennou/gwenn2 8001 &
sleep 1

echo "executing: python3 droopy.py -d pajennou/ruz1 8002 &"
python3 droopy.py -d pajennou/ruz1 8002 &
sleep 1

echo "executing: python3 droopy.py -d pajennou/ruz2 8003 &"
python3 droopy.py -d pajennou/ruz2 8003 &
sleep 1

echo "executing: python3 droopy.py -d pajennou/du 8004 &"
python3 droopy.py -d pajennou/du 8004 &
sleep 1

echo "executing: python3 droopy.py -d pajennou/glas 8005 &"
python3 droopy.py -d pajennou/glas 8005 &
sleep 1

echo "executing: python3 droopy.py -d pajennou/kelennerien 8006 &"
python3 droopy.py -d pajennou/kelennerien 8006 &
sleep 1


cd /home/pi/kaoz
echo "executing: python3 servijer.py 8100 &"
python3 servijer.py 8100 &

