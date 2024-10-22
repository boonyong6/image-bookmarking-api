#!/bin/bash
website_root=$WEBSITE_ROOT
website_host=$WEBSITE_HOST

echo '=> Start deploying...'
echo

echo '=> Pulling updates from the remote repository...'
git pull
echo '=> End pull.'
echo

echo '=> Syncing project files...'
rsync -a ./mysite/ "$website_root"
echo '=> End sync.'
echo

echo '=> Installing package dependencies...'
source "$website_root/venv/bin/activate"
python -m pip install -r requirements.txt
echo '=> End pip install.'
echo

echo '=> Running model migrations...'
python3 $website_root/manage.py migrate
echo '=> End Migration.'
echo

echo '=> Collecting static files into STATIC_ROOT...'
python3 $website_root/manage.py collectstatic
echo '=> End collectstatic'

echo '=> Restarting the website...'
devil www restart "$website_host"
echo '=> End restart.'
echo

echo '=> End deploy.'
echo
