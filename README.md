A simple python tool to manage Cloudflare DNS!!!

USAGE:
_ Provide email + API key + API CA key to ~/.cloudflare/cloudflare.cfg
_ If using API token, no need to provide email and API CA key
Example:
$ cat ~/.cloudflare/cloudflare.cfg
[CloudFlare]
email = user@example.com # Do not set if using an API token
token = 00000000000000000000 # API key or API token
certtoken = v1.0-...

_ Because the tool mostly uses cloudflare-wrapper, which requires python version 3, you need to install python 3 and the module
Python 3: https://realpython.com/installing-python/#how-to-install-python-on-linux
Cloudflare-wrapper: https://github.com/cloudflare/python-cloudflare#installation

_ Run script:
$ python3 cloudflare-tool.py
