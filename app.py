import os
import subprocess
import time

FILE_PATH = os.environ.get('FILE_PATH', './files')
ARGO_AUTH = os.environ.get('ARGO_AUTH', '')

def authorize(file_list):
    for f in file_list:
        path = os.path.join(FILE_PATH, f)
        os.chmod(path, 0o775)

def run_commands():
    authorize(['cat', 'dog'])
    
    subprocess.run(f"nohup {FILE_PATH}/cat -c {FILE_PATH}/mouse.json >/dev/null 2>&1 &", shell=True)
    time.sleep(2)
    
    if os.path.exists(os.path.join(FILE_PATH, 'dog')) and ARGO_AUTH:
        args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {ARGO_AUTH}"
        subprocess.run(f"nohup {FILE_PATH}/dog {args} >/dev/null 2>&1 &", shell=True)

run_commands()
