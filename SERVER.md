Docker

NGINX

    Work with default config

Digital certificates (let's encrypt)
   65  sudo snap install --classic certbot
   66  sudo ln -s /snap/bin/certbot /usr/bin/certbot
   67  ls
   68  mkdir certs
   69  cd certs/
   70  sudo certbot certonly --nginx


26  sudo apt-get install nginx
   45  more /etc/nginx/nginx.conf
   50  cp /etc/nginx/nginx.conf conf/
   60  more nginxconf
   62  nano nginxconf
   70  sudo certbot certonly --nginx
   79  more nginx.conf
   85  more nginxconf
   94  more nginxconf
  102  ls /etc/nginx/sites-available/default
  103  ls -l /etc/nginx/sites-available/default
  104  more -l /etc/nginx/sites-available/default
  166  systemctl status nginx.service
  171  sudo systemctl reload nginx.service
  172  sudo systemctl reload nginx




  Algorithm store (optional but recommended)
The algorithm store is intended to be used as a repository for trusted algorithms within a certain project. Algorithm stores can be coupled to specific collaborations or to all collaborations on a given server. Note that you can also couple the community algorithm store (https://store.cotopaxi.vantage6.ai) to your server. This store contains a number of community algorithms that you may find useful.