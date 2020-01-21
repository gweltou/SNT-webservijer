#! /bin/bash

cd /home/pi/SNT-webservijer

echo "executing: python3 my_html_parser.py"
python3 my_html_parser.py

echo "executing: sudo python3 -m http.server 80 &"
sudo python3 -m http.server 80 &
sleep 2


echo "executing: python3 droopy.py -d pajennou/gwenn1 8000 &"
sudo python3 droopy.py -d "pajennou/gwenn1" 8000 &
sleep 2

echo "executing: python3 droopy.py -d pajennou/gwenn2 8001 &"
sudo python3 droopy.py -d "pajennou/gwenn2" --chmod 0777 8001 &
sleep 2

echo "executing: python3 droopy.py -d pajennou/ruz1 8002 &"
sudo python3 droopy.py -d "pajennou/ruz1" --chmod 0777 8002 &
sleep 2

echo "executing: python3 droopy.py -d pajennou/ruz2 8003 &"
sudo python3 droopy.py -d "pajennou/ruz2" --chmod 0777 8003 &
sleep 2

echo "executing: python3 droopy.py -d pajennou/du 8004 &"
sudo python3 droopy.py -d "pajennou/du" --chmod 0777 8004 &
sleep 2

echo "executing: python3 droopy.py -d pajennou/glas 8005 &"
sudo python3 droopy.py -d "pajennou/glas" --chmod 0777 8005 &
sleep 2

echo "executing: python3 droopy.py -d pajennou/kelennerien 8006 &"
sudo python3 droopy.py -d "pajennou/kelennerien" --chmod 0777 8006 &
sleep 2


cd /home/pi/kaoz
echo "executing: python3 servijer.py 8100 &"
python3 servijer.py 8100 &

