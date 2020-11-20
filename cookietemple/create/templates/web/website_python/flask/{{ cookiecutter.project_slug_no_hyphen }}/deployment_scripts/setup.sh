#!/bin/bash
# Reference:
# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
sudo apt-get install software-properties-common
sudo apt-add-repository universe
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-dev nginx -y
sudo pip3 install virtualenv

virtualenv dpenv
source dpenv/bin/activate

sudo apt-get update
pip3 install gunicorn
make install

cp /home/{{cookiecutter.vmusername}}/{{cookiecutter.project_slug}}/deployment_scripts/{{cookiecutter.project_slug_no_hyphen}}.service \
/etc/systemd/system/{{cookiecutter.project_slug_no_hyphen}}.service

sudo systemctl start {{cookiecutter.project_slug}}

sudo systemctl enable {{cookiecutter.project_slug}}

cp /home/{{cookiecutter.vmusername}}/{{cookiecutter.project_slug}}/deployment_scripts/{{cookiecutter.project_slug_no_hyphen}} \
/etc/nginx/sites-available/{{cookiecutter.project_slug_no_hyphen}}

ln -s /etc/nginx/sites-available/{{cookiecutter.project_slug_no_hyphen}} /etc/nginx/sites-enabled

sudo nginx -t

sudo systemctl restart nginx

sudo ufw delete allow 5000

sudo ufw allow 'Nginx Full'

sudo add-apt-repository ppa:certbot/certbot -y

sudo apt install python3-certbot-nginx -y

sudo certbot --nginx -d {{cookiecutter.url}} -d www.{{cookiecutter.url}} --non-interactive --agree-tos -m {{cookiecutter.email}}
