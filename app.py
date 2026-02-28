import os
import re
import subprocess
import time

# Set environment variables
FILE_PATH = os.environ.get('FILE_PATH', './files')
ARGO_AUTH = os.environ.get('ARGO_AUTH', 'eyJhIjoiYjg0NTBiMjNlYmRlMGQ1ZWExNjU1YTUxODk4YzE5Y2IiLCJ0IjoiOTNkYTIyYzUtOWIxYS00MTJlLTllNGUtYTY0MjFjODgzZDIzIiwicyI6IlpXSmlPV05sTURrdE16azVNUzAwWm1Wa0xXRmhOakl0TkdVNFlqUTBNbUUzTVRFNCJ9')            

# Create directory if it doesn't exist
if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)
    print(f"{FILE_PATH} has been created")
else:
    print(f"{FILE_PATH} already exists")


def files_and_run():

    files_to_authorize = ['./cat', './dog']
    authorize_files(files_to_authorize)
    

    command1 = f"nohup {FILE_PATH}/cat -c {FILE_PATH}/mouse.json >/dev/null 2>&1 &"
    try:
        subprocess.run(command1, shell=True, check=True)
        print('cat is running')
        subprocess.run('sleep 1', shell=True)  # Wait for 1 second
    except subprocess.CalledProcessError as e:
        print(f'cat running error: {e}')


    if os.path.exists(os.path.join(FILE_PATH, 'dog')):
        if not re.match(r'^[A-Z0-9a-z=]{120,250}$', ARGO_AUTH):
            print("ARGO_AUTH variable is empty")
            return
        else:
            args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {ARGO_AUTH}"

        try:
            subprocess.run(f"nohup {FILE_PATH}/dog {args} >/dev/null 2>&1 &", shell=True, check=True)
            print('dog is running')
            subprocess.run('sleep 2', shell=True)  # Wait for 2 seconds
        except subprocess.CalledProcessError as e:
            print(f'Error executing command: {e}')

    subprocess.run('sleep 3', shell=True)  # Wait for 3 seconds


# Authorize files
def authorize_files(file_paths):
    new_permissions = 0o775

    for relative_file_path in file_paths:
        absolute_file_path = os.path.join(FILE_PATH, relative_file_path)
        try:
            os.chmod(absolute_file_path, new_permissions)
            print(f"Empowerment success for {absolute_file_path}: {oct(new_permissions)}")
        except Exception as e:
            print(f"Empowerment failed for {absolute_file_path}: {e}")



files_and_run()

