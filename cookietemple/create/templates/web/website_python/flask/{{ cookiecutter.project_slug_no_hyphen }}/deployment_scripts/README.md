1. SSH into server as root (if no user with superuser privileges exists)

2. Create an account with superuser privileges if not yet existing:
```bash
adduser {{cookiecutter.vmusername}}

usermod -aG sudo {{cookiecutter.vmusername}}

su {{cookiecutter.vmusername}}
```

3. Enable firewall
```bash
ufw allow OpenSSH
ufw enable
```

4. Clone the code and start the deployment script! Ensure beforehand that the user account and the URL are still matching!
```bash
cd ~

git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}
```
```bash
sudo bash {{cookiecutter.project_slug_no_hyphen}}/deployment_scripts/setup.sh
```
