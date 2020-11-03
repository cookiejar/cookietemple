#!/bin/bash
# Reference:
# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

cp /home/{{cookiecutter.vmusername}}/{{cookiecutter.project_slug}}/deployment_scripts/{{cookiecutter.project_slug_no_hyphen}}.service \
/etc/systemd/system/{{cookiecutter.project_slug_no_hyphen}}.service

systemctl start {{cookiecutter.project_slug}}

systemctl enable {{cookiecutter.project_slug}}

cp /home/{{cookiecutter.vmusername}}/{{cookiecutter.project_slug}}/deployment_scripts/{{cookiecutter.project_slug_no_hyphen}} \
/etc/nginx/sites-available/{{cookiecutter.project_slug_no_hyphen}}

ln -s /etc/nginx/sites-available/{{cookiecutter.project_slug_no_hyphen}} /etc/nginx/sites-enabled

nginx -t

systemctl restart nginx

ufw delete allow 5000

ufw allow 'Nginx Full'

add-apt-repository ppa:certbot/certbot -y

apt install python3-certbot-nginx -y

certbot --nginx -d {{cookiecutter.url}} -d www.{{cookiecutter.url}} --non-interactive --agree-tos -m {{cookiecutter.email}}
