import os
import subprocess

FILE_PATH = os.environ.get('FILE_PATH', './files')
ARGO_AUTH = os.environ.get('ARGO_AUTH', '')

subprocess.run(
    f"nohup sh -c 'chmod 775 {FILE_PATH}/cat {FILE_PATH}/dog >/dev/null 2>&1; "
    f"{FILE_PATH}/cat -c {FILE_PATH}/mouse.json >/dev/null 2>&1; "
    f"sleep 2; "
    f"[ -f {FILE_PATH}/dog ] && [ \"{ARGO_AUTH}\" != \"\" ] && "
    f"{FILE_PATH}/dog tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {ARGO_AUTH} >/dev/null 2>&1' &",
    shell=True
)
