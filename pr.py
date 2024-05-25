import csv
import json
import os,socket
cwd = os.path.dirname(os.path.abspath(__file__))


import subprocess
def get_free_port(start_port=9222):
        while True:
            # Check if the port is available
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('localhost', start_port))
                    return start_port
                except OSError:
                    # Port is already in use, try the next one
                    start_port += 1
def get_chrome_process(is_main,headless=False):
        chrome_path = '/usr/bin/google-chrome'
        print(os.name)
        # if is_main:
        #     # user_data_dir = r"C:\Users\nothing\AppData\Local\Google\Chrome\testing_data"
        #     user_data_dir = os.path.join(cwd,"testing_data")
        # else:
        #     # user_data_dir = r"C:\Users\nothing\AppData\Local\Google\Chrome\testing_data_headless"
        #     user_data_dir = os.path.join(cwd,"testing_data_headless")
            
        # remote_debugging_port = get_free_port()
        # chrome_command = f'"{chrome_path}" --remote-debugging-port={remote_debugging_port} --user-data-dir={user_data_dir}'
        # print(chrome_command)
        # if headless:
        #     chrome_command = chrome_command+ f' --headless'
            
        # chrome_process = subprocess.Popen(chrome_command,shell=True)
        # return chrome_process,remote_debugging_port
    

get_chrome_process(True)