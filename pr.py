import csv
import subprocess
import psutil
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import json
import socket
from tkinter import simpledialog, messagebox
import random
import pyautogui as py
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import tkinter as tk
import pyperclip
cwd = os.path.dirname(os.path.abspath(__file__))


def get_chrome_path():
        chrome_path=''
        if os.path.exists(os.path.join(cwd,"config.json")):
            with open (os.path.join(cwd,"config.json")) as f:
                data=json.load(f)
                chrome_path = data['chrome_path']
        
        return chrome_path
            

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

def close_driver(driver):
    driver.quit()

def is_chrome_window_closed():
    for window in psutil.process_iter(['pid', 'name']):
        try:
            if 'chrome' in window.info['name'].lower():
                return False
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return True

def get_chrome_process(is_main,headless=False):
    chrome_path = get_chrome_path()
    if is_main:
        # user_data_dir = r"C:\Users\nothing\AppData\Local\Google\Chrome\testing_data"
        user_data_dir = os.path.join(cwd,"testing_data")
    else:
        # user_data_dir = r"C:\Users\nothing\AppData\Local\Google\Chrome\testing_data_headless"
        user_data_dir = os.path.join(cwd,"testing_data_headless")
        
    remote_debugging_port = get_free_port()
    chrome_command = f'"{chrome_path}" --remote-debugging-port={remote_debugging_port}'
    if headless:
        chrome_command = chrome_command+ f' --headless'
    
    if os.name == "posix":
        chrome_process = subprocess.Popen(chrome_command,shell=True)
    elif os.name == 'nt':
        chrome_process = subprocess.Popen(chrome_command)
        
    return chrome_process,remote_debugging_port

    
def copy_to_clipboard_and_notify(url):
    pyperclip.copy(url)
    notify_window = tk.Toplevel()
    notify_window.title("Notification")
    label = tk.Label(notify_window, text="URL copied to clipboard", wraplength=300)
    label.pack(pady=10)
    ok_button = tk.Button(notify_window, text="OK", command=notify_window.destroy)
    ok_button.pack(pady=5)
    notify_window.mainloop()

def show_info_with_copy_button(master_url):
    def on_ok():
        root.destroy()

    def on_copy_url():
        copy_to_clipboard_and_notify(master_url)

    root = tk.Tk()
    root.title("Info")

    label = tk.Label(root, text=f"Please visit the URL: {master_url} and search for the location", wraplength=400)
    label.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    ok_button = tk.Button(button_frame, text="OK", command=on_ok)
    ok_button.grid(row=0, column=0, padx=5)

    copy_button = tk.Button(button_frame, text="Copy URL", command=on_copy_url)
    copy_button.grid(row=0, column=1, padx=5)

    root.mainloop()


master_url="https://www.realestate.com.au/"
chrome_process,port=get_chrome_process(is_main=True)

# Create Chrome options
# Initialize Chrome WebDriver with debugger address
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
driver = webdriver.Chrome(options=chrome_options)

time.sleep(1)
# messagebox.showinfo("Info",f"Please visit the url: {master_url} and search for the location")
# time.sleep(5)
# while True: 
#     time.sleep(1)
#     if len(driver.find_elements(By.XPATH,"//div[@id='heroImage']"))>0:
#         break

show_info_with_copy_button(master_url)



# # Initialize ActionChains
# action = ActionChains(driver)

# # Wait for the page to load
# time.sleep(5)

# # Open Google
# driver.get("https://google.com")
# time.sleep(3)

# # Click on the search bar and enter text
# search_bar = driver.find_element(By.XPATH, "//textarea[@title='Search']")
# search_bar.click()
# time.sleep(random.uniform(0, 2))
# action.send_keys(master_url).perform()
# time.sleep(1)

# # Press Enter to perform the search
# action.send_keys(Keys.ENTER).perform()
# time.sleep(5)

# # Click on the desired website link
# website_link = driver.find_elements(By.XPATH, "(//h3[contains(text(),'realestate.com.au')])[1]")
# website_link[0].click()
# time.sleep(10)

# # Open a new tab with master_url
# action.key_down(Keys.CONTROL).send_keys("T").key_up(Keys.CONTROL).perform()
# time.sleep(1)  # Add a small delay before sending the URL
# action.send_keys(master_url).send_keys(Keys.ENTER).perform()
# time.sleep(10)

# # Close the newly opened tab
# action.key_down(Keys.CONTROL).send_keys("W").key_up(Keys.CONTROL).perform()

# # Refresh the main tab
# driver.refresh()
# time.sleep(10)

# # Close the WebDriver
# driver.quit()

# # Exit the script
# exit(1)
