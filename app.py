import os
import subprocess
import json
import time

# ------------------------
# 环境变量
# ------------------------
FILE_PATH = os.environ.get('FILE_PATH', './files')
UUID = os.environ.get('UUID', '01010101-0101-0101-0101-010101010101')
ARGO_AUTH = os.environ.get('ARGO_AUTH', '')
ARGO_PORT = int(os.environ.get('ARGO_PORT', '8080'))
DOMAIN = os.environ.get('DOMAIN', 'example.com')  # dogflared 隧道绑定的域名

# ------------------------
# 创建必要目录
# ------------------------
os.makedirs(FILE_PATH, exist_ok=True)
print(f"{FILE_PATH} ready")

# ------------------------
# 删除旧配置
# ------------------------
config_file_path = os.path.join(FILE_PATH, 'config.json')
if os.path.exists(config_file_path):
    os.remove(config_file_path)
    print("Old config.json removed")

# ------------------------
# cat 配置
# ------------------------
config = {
    "log": {"access": "/dev/null", "error": "/dev/null", "loglevel": "none"},
    "inbounds": [
        {
            "port": ARGO_PORT,
            "protocol": "vless",
            "settings": {
                "clients": [{"id": UUID}],
                "decryption": "none",
                "fallbacks": [
                    {"dest": 3001},
                    {"path": "/vless-argo", "dest": 3002},
                    {"path": "/vmess-argo", "dest": 3003},
                    {"path": "/trojan-argo", "dest": 3004},
                    {"path": "/reality-argo", "dest": 3005},
                    {"path": "/hysteria2-argo", "dest": 3006}
                ]
            },
            "streamSettings": {"network": "tcp"}
        },
        {"port": 3001, "listen": "127.0.0.1", "protocol": "vless",
         "settings":{"clients":[{"id":UUID}]},
         "streamSettings":{"network":"ws","security":"none"}},
        {"port": 3002, "listen": "127.0.0.1", "protocol": "vless",
         "settings":{"clients":[{"id":UUID}]},
         "streamSettings":{"network":"ws","security":"none","wsSettings":{"path":"/vless-argo"}}},
        {"port": 3003, "listen": "127.0.0.1", "protocol": "vmess",
         "settings":{"clients":[{"id":UUID,"alterId":0}]},
         "streamSettings":{"network":"ws","wsSettings":{"path":"/vmess-argo"}}},
        {"port": 3004, "listen": "127.0.0.1", "protocol": "trojan",
         "settings":{"clients":[{"password":UUID}]},
         "streamSettings":{"network":"ws","wsSettings":{"path":"/trojan-argo"}}},
        {"port": 3005, "listen": "127.0.0.1", "protocol": "reality",
         "settings":{"clients":[{"id":UUID,"shortIds":[UUID[:8]]}]},
         "streamSettings":{"network":"ws","wsSettings":{"path":"/reality-argo"}}},
        {"port": 3006, "listen": "127.0.0.1", "protocol": "hysteria2",
         "settings":{"up_mbps":100,"down_mbps":100,"auth":UUID},
         "streamSettings":{"network":"ws","wsSettings":{"path":"/hysteria2-argo"}}}
    ],
    "outbounds":[{"protocol":"freedom","tag":"direct"},{"protocol":"blackhole","tag":"block"}]
}

# 写入 config.json
with open(config_file_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
print("config.json generated")

# ------------------------
# 启动 cat
# ------------------------
cat_path = os.path.join(FILE_PATH, "cat")
os.chmod(cat_path, 0o775)
subprocess.Popen([cat_path, "-c", config_file_path])
print("cat started")

# ------------------------
# 静态伪装网页处理
# ------------------------
web_dir = os.path.join(FILE_PATH, "www")
os.makedirs(web_dir, exist_ok=True)
index_html = os.path.join(web_dir, "index.html")
if not os.path.exists(index_html):
    with open(index_html, 'w', encoding='utf-8') as f:
        f.write("""<html>
<head><title>我的网站</title></head>
<body>
<h1>欢迎访问!</h1>
<p>这是通过 dogflared 隧道访问的静态网页</p>
</body>
</html>""")
    print(f"Generated default index.html in {web_dir}")
else:
    print(f"Using existing index.html in {web_dir}")

# ------------------------
# 启动 dogflared 隧道
# ------------------------
dog_path = os.path.join(FILE_PATH, "dog")
if os.path.exists(dog_path) and ARGO_AUTH:
    os.chmod(dog_path, 0o775)
    cmd = [
        dog_path,
        "tunnel",
        "--edge-ip-version", "auto",
        "--no-autoupdate",
        "--protocol", "http2",
        "run",
        "--token", ARGO_AUTH,
        "--url", f"http://localhost:{ARGO_PORT}"
    ]
    subprocess.Popen(cmd)
    print("dogflared tunnel started")
else:
    print("dogflared not found or ARGO_AUTH empty, tunnel not started")