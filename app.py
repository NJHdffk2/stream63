import os
import json
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# ------------------------
# 环境变量
# ------------------------
FILE_PATH = os.environ.get('FILE_PATH', './files')

UUID = os.environ.get(
    'UUID',
    '01010101-0101-0101-0101-010101010101'
)

ARGO_AUTH = os.environ.get('ARGO_AUTH', 'eyJhIjoiYjg0NTBiMjNlYmRlMGQ1ZWExNjU1YTUxODk4YzE5Y2IiLCJ0IjoiOTNkYTIyYzUtOWIxYS00MTJlLTllNGUtYTY0MjFjODgzZDIzIiwicyI6IlpXSmlPV05sTURrdE16azVNUzAwWm1Wa0xXRmhOakl0TkdVNFlqUTBNbUUzTVRFNCJ9')

# Xray 主入口
ARGO_PORT = int(os.environ.get('ARGO_PORT', '8080'))

# 静态网站端口
WEB_PORT = int(os.environ.get('WEB_PORT', '8081'))

# 域名
DOMAIN = os.environ.get('DOMAIN', 'example.com')

# ------------------------
# 创建目录
# ------------------------
os.makedirs(FILE_PATH, exist_ok=True)

# ------------------------
# 删除旧配置
# ------------------------
config_path = os.path.join(FILE_PATH, 'config.json')

if os.path.exists(config_path):
    os.remove(config_path)

# ------------------------
# Xray 配置
# ------------------------
config = {
    "log": {
        "access": "/dev/null",
        "error": "/dev/null",
        "loglevel": "none"
    },

    "inbounds": [

        # 主入口
        {
            "port": ARGO_PORT,
            "protocol": "vless",

            "settings": {
                "clients": [
                    {
                        "id": UUID
                    }
                ],

                "decryption": "none",

                "fallbacks": [
                    {
                        "path": "/vless-argo",
                        "dest": 3001
                    },

                    {
                        "path": "/vmess-argo",
                        "dest": 3002
                    },

                    {
                        "path": "/trojan-argo",
                        "dest": 3003
                    },

                    {
                        "path": "/reality-argo",
                        "dest": 3004
                    }
                ]
            },

            "streamSettings": {
                "network": "tcp"
            }
        },

        # VLESS WS
        {
            "port": 3001,
            "listen": "127.0.0.1",
            "protocol": "vless",

            "settings": {
                "clients": [
                    {
                        "id": UUID
                    }
                ],

                "decryption": "none"
            },

            "streamSettings": {
                "network": "ws",

                "security": "none",

                "wsSettings": {
                    "path": "/vless-argo"
                }
            }
        },

        # VMESS WS
        {
            "port": 3002,
            "listen": "127.0.0.1",
            "protocol": "vmess",

            "settings": {
                "clients": [
                    {
                        "id": UUID,
                        "alterId": 0
                    }
                ]
            },

            "streamSettings": {
                "network": "ws",

                "wsSettings": {
                    "path": "/vmess-argo"
                }
            }
        },

        # Trojan WS
        {
            "port": 3003,
            "listen": "127.0.0.1",
            "protocol": "trojan",

            "settings": {
                "clients": [
                    {
                        "password": UUID
                    }
                ]
            },

            "streamSettings": {
                "network": "ws",

                "wsSettings": {
                    "path": "/trojan-argo"
                }
            }
        },

        # REALITY
        {
            "port": 3004,
            "listen": "127.0.0.1",
            "protocol": "vless",

            "settings": {
                "clients": [
                    {
                        "id": UUID
                    }
                ],

                "decryption": "none"
            },

            "streamSettings": {
                "network": "tcp",

                "security": "reality",

                "realitySettings": {
                    "show": False,

                    "dest": "www.cloudflare.com:443",

                    "xver": 0,

                    "serverNames": [
                        "www.cloudflare.com"
                    ],

                    "privateKey": "YOUR_PRIVATE_KEY",

                    "shortIds": [
                        "6ba85179e30d4fc2"
                    ]
                }
            }
        }
    ],

    "outbounds": [
        {
            "protocol": "freedom",
            "tag": "direct"
        },

        {
            "protocol": "blackhole",
            "tag": "block"
        }
    ]
}

# ------------------------
# 写入配置
# ------------------------
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2)

print('config.json generated')

# ------------------------
# 启动 cat ()
# ------------------------
cat_path = os.path.join(FILE_PATH, 'cat')

if os.path.exists(cat_path):

    os.chmod(cat_path, 0o775)

    subprocess.Popen(
        [cat_path, '-c', config_path]
    )

    print('cat started')

else:
    print('cat not found')

# ------------------------
# 静态网站
# ------------------------
web_dir = os.path.join(FILE_PATH, 'www')

os.makedirs(web_dir, exist_ok=True)

index_html = os.path.join(web_dir, 'index.html')

# 自动生成网页
if not os.path.exists(index_html):

    with open(index_html, 'w', encoding='utf-8') as f:

        f.write("""
<html>
<head>
<title>Welcome</title>
</head>

<body>
<h1>Hello World</h1>
<p>Cloudflare Tunnel Website</p>
</body>
</html>
""")

# 切换目录
os.chdir(web_dir)

# HTTP 服务
def start_web():

    httpd = HTTPServer(
        ('0.0.0.0', WEB_PORT),
        SimpleHTTPRequestHandler
    )

    httpd.serve_forever()

threading.Thread(
    target=start_web,
    daemon=True
).start()

print(f'web started : {WEB_PORT}')

# ------------------------
# 启动 dog (cloudflared)
# ------------------------
dog_path = os.path.join(FILE_PATH, 'dog')

if os.path.exists(dog_path) and ARGO_AUTH:

    os.chmod(dog_path, 0o775)

    cmd = [
        dog_path,

        'tunnel',

        '--edge-ip-version',
        'auto',

        '--no-autoupdate',

        '--protocol',
        'http2',

        'run',

        '--token',
        ARGO_AUTH,

        '--url',
        f'http://localhost:{WEB_PORT}'
    ]

    subprocess.Popen(cmd)

    print('dog started')

else:
    print('dog not found or token empty')

