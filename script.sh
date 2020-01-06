#!/bin/bash
pip3 install virtualenv
mkdir scrapping
cd scrapping
sudo apt install virtualenv
virtualenv venv --python=python3
git clone https://git.weboob.org/weboob/weboob.git -b stable
source venv/bin/activate

dir=$(pwd)
a="file://"
c="/weboob/modules/"
pip3 install -e weboob/
touch test.txt
echo "${a}$(pwd)${c}" > test.txt
mv test.txt ~/.config/weboob/sources.list
cd weboob
weboob-config update
boobank

sudo apt-get install curl

sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
