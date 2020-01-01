#!/bin/bash
# Reference:
# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

apt-get update

apt-get install python3-pip python3-dev nginx -y

pip3 install virtualenv

cd ~

git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}

cd {{cookiecutter.project_slug}}

virtualenv dpenv

source dpenv/bin/activate

pip3 install gunicorn

python setup.py clean --all install

cp /home/{{cookiecutter.uservmname}}/{{cookiecutter.project_slug}}/deployment_scripts/{{cookiecutter.project_slug}}.service \
/etc/systemd/system/{{cookiecutter.project_slug}}.service

systemctl start {{cookiecutter.project_slug}}

systemctl enable {{cookiecutter.project_slug}}

cp /home/{{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/deployment_scripts/{{cookiecutter.project_slug}} \
/etc/nginx/sites-available/{{cookiecutter.project_slug}}

ln -s /etc/nginx/sites-available/{{cookiecutter.project_slug}} /etc/nginx/sites-enabled

nginx -t

systemctl restart nginx

ufw delete allow 5000

ufw allow 'Nginx Full'

add-apt-repository ppa:certbot/certbot -y

apt install python-certbot-nginx -y

certbot --nginx -d {{cookiecutter.url}} -d www.{{cookiecutter.url}} --non-interactive --agree-tos -m {{cookiecutter.email}}







