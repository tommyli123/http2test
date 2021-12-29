# Overview

This is a test of http2 protocols and the performance implications.

Using an async client, issue mutltiple concurrent requests against a http2 source and measure the duration.

I have used nginx (with http2) in localhost as a reverse proxy to upstream.  I choose https://httpbin.org as the test upstream as it readily supports http2 with the necessary HTTP methods for my testing.

# install and configure nginx

1. nginx with http2 requires using TLS, we need to create self signed certs. 
```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
```

2. install nginx
```
sudo apt update
sudo apt install nginx
```

3. create `/etc/nginx/snippets/self-signed.conf` with the certs
```
ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
```

4. create `/etc/nginx/snippets/ssl-params.conf`
```
ssl_protocols TLSv1.2;
ssl_prefer_server_ciphers on;
# ssl_dhparam /etc/nginx/dhparam.pem;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
ssl_ecdh_curve secp384r1; # Requires nginx >= 1.1.0
ssl_session_timeout  10m;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off; # Requires nginx >= 1.5.9
ssl_stapling on; # Requires nginx >= 1.3.7
ssl_stapling_verify on; # Requires nginx => 1.3.7
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
# Disable strict transport security for now. You can uncomment the following
# line if you understand the implications.
# add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
```

5. In `/etc/nginx/sites-available` create site `myhttpbin`.  Enable http2 in the ssl port, and add the self cert files. Disable serving html files, and set the reverse proxy
```
server {
	listen 8080 default_server;
	listen [::]:8080 default_server;

	# SSL configuration
	#
	listen 8443 ssl http2 default_server;
	listen [::]:8443 ssl http2 default_server;
    include snippets/self-signed.conf;
    include snippets/ssl-params.conf;
	
	# root /var/www/html/myhttpbin;

	server_name _;

	location / {
		proxy_pass https://httpbin.org;
	}

```

6. create symbolic link in `/etc/nginx/sites-enabled`
```
ln -s /etc/nginx/sites-available/httpbin httpbin
```

7. disable SSL settings in `/etc/nginx/nginx.conf`

```
TODO
```

# python setup

1. Install python3.9+.  The httpx library used (for async client support) does not work well with 3.8.

2. setup venv and install dependencies
```
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. run test1.py
```
python test1.py
```



