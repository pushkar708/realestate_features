import csv
import subprocess
import psutil
import tkinter as tk
import pyperclip
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import json
import socket
import random
import pyautogui as py
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchWindowException
cwd = os.path.dirname(os.path.abspath(__file__))


class GetDetailsFromWeb():
    def __init__(self,needed_data_list):
        super().__init__()
        self.neended_data_list = needed_data_list
        self.csv_file_path = os.path.join(cwd,'home_details.csv')
        self.json_file_path = os.path.join(cwd,'home_details.json')
        print("needed data= ",self.neended_data_list)
        self.main()
        self.json_to_csv(self.json_file_path,self.csv_file_path)

    def get_chrome_path(self):
        chrome_path=''
        if os.path.exists(os.path.join(cwd,"config.json")):
            with open (os.path.join(cwd,"config.json")) as f:
                data=json.load(f)
                chrome_path = data['chrome_path']
        
        return chrome_path
            
    
    def get_free_port(self,start_port=9222):
        while True:
            # Check if the port is available
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('localhost', start_port))
                    return start_port
                except OSError:
                    # Port is already in use, try the next one
                    start_port += 1

    def close_driver(self,driver):
        driver.quit()

    def is_chrome_window_closed(self):
        for window in psutil.process_iter(['pid', 'name']):
            try:
                if 'chrome' in window.info['name'].lower():
                    return False
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return True

    def get_chrome_process(self,is_main,headless=False):
        chrome_path = self.get_chrome_path()
        if is_main:
            # user_data_dir = r"C:\Users\nothing\AppData\Local\Google\Chrome\testing_data"
            user_data_dir = os.path.join(cwd,"testing_data")
        else:
            # user_data_dir = r"C:\Users\nothing\AppData\Local\Google\Chrome\testing_data_headless"
            user_data_dir = os.path.join(cwd,"testing_data_headless")
            
        remote_debugging_port = self.get_free_port()
        chrome_command = f'"{chrome_path}" --remote-debugging-port={remote_debugging_port}'
        if headless:
            chrome_command = chrome_command+ f' --headless'
        
        if os.name == "posix":
            chrome_process = subprocess.Popen(chrome_command,shell=True)
        elif os.name == 'nt':
            chrome_process = subprocess.Popen(chrome_command)
            
        return chrome_process,remote_debugging_port

    def get_page_details(self,driver):
        time.sleep(1)
        features=[]
        data={}
        
        house_details=driver.find_elements(By.XPATH,"//div[@class='Inline__InlineContainer-sc-lf7x8d-0 gOaIBl View__InlineStyled-sc-4or7us-0 AYXFA property-info__property-attributes']")
        
        if 'house_name' in self.neended_data_list:
            house_name = driver.find_elements(By.XPATH, "//h1[@class='property-info-address']")
            if house_name:
                data["House Name"] = house_name[0].text
        
        if 'property_price' in self.neended_data_list:
            property_price=driver.find_elements(By.XPATH,"//span[@class='property-price property-info__price']")
            if property_price:
                data["Price"] = property_price[0].text
        
        if 'loan_repay_item' in self.neended_data_list:
            loan_repay_item=driver.find_elements(By.ID,"summary-repayments-container")
            if loan_repay_item:
                data["Loan Repay Amount"]=loan_repay_item[0].get_attribute("aria-label")
        
        if 'property_details' in self.neended_data_list:
            property_details=driver.find_elements(By.XPATH,"//span[@class='property-description__content']")
            if property_details:
                data["Description"]=str(property_details[0].text).replace("\\n", "\n")
        
        if 'property_features_item' in self.neended_data_list:
            property_features_item=driver.find_elements(By.XPATH,"//div[@class='property-features__feature']//p")
            if property_features_item:
                show_more_button=driver.find_elements(By.XPATH,"//button//p[contains(text(), 'Show more feature')]")
                if len(show_more_button) > 0:
                    show_more_button[0].click()
                for feature in property_features_item:
                    features.append(feature.text)
                features_value = ", ".join(features)
                if features_value:
                    data["Features"]=features_value
        
        if 'floorplan_area' in self.neended_data_list:
            floorplan_area=driver.find_elements(By.XPATH,"//span[@class='View__StyledIcon-sc-1am1guj-0 gPRTZR floorplans-tours__floorplan']")
            if floorplan_area:
                floorplan_area[0].click()
                time.sleep(1)
                floorplan_image=driver.find_elements(By.XPATH,"(//img[@class='pswp__img'])[1]")
                if floorplan_image:
                    data["Floor Plan"]=floorplan_image[0].get_attribute("src")
                    driver.find_element(By.XPATH,"//button[@title='Close (Esc)']").click()
        
        if 'agent_org' in self.neended_data_list:
            agent_org=driver.find_elements(By.XPATH,"(//a[@class='LinkBase-sc-12oy0hl-0 iskBYI sidebar-traffic-driver__name'])[last()]")
            if agent_org:
                data["Agent Organisation"]=agent_org[0].text
        
        if 'agent_org_address' in self.neended_data_list:
            agent_org_address=driver.find_elements(By.XPATH,"(//div[@class='sidebar-traffic-driver__detail-info'])[last()]")
            if agent_org_address:
                data["Agent Organisation Address"]=agent_org_address[0].text
        
        if 'property_size' in self.neended_data_list:
            property_size=house_details[0].find_elements(By.XPATH,"//div[@class='View__PropertySize-sc-1psmy31-0 cgTBlr property-size']")
            if property_size:
                data["Size"] = property_size[0].get_attribute("aria-label")
        
        if 'property_type' in self.neended_data_list:
            property_type=house_details[0].find_elements(By.XPATH,"//span[@class='property-info__property-type']")
            if property_type:
                data["Type"] = property_type[0].text
        
        if 'agent_phone' in self.neended_data_list:
            agent_phone=driver.find_elements(By.XPATH,"//ul[@class='agent-info agent-info--horizontal']/li//div[@class='phone']/a[1]")
            if agent_phone:
                if len(agent_phone) > 0:
                    names = []
                    for name_element in agent_phone:
                        names.append(str(name_element.get_attribute("href")).replace("tel:",''))
                    tel = "; ".join(set(names))
                data["Agent Phone"]=tel
        
        if 'agent_name' in self.neended_data_list:
            agent_name=driver.find_elements(By.XPATH,"//ul[@class='agent-info agent-info--horizontal']/li//a[contains(@class,'agent-info__name')]")
            if agent_name:
                if len(agent_name) > 1:
                    names = []
                    for name_element in agent_name:
                        names.append(name_element.text)
                    name = "; ".join(set(names))
                else:
                    name = agent_name[0].text
                data["Agent Name"] = name
        
        if 'house_properties_list' in self.neended_data_list:
            if house_details:
                house_properties_list=house_details[0].find_elements(By.XPATH,"//div[@class='View__PropertyDetail-sc-11ysrk6-0 haFtfe']")
                property_type=house_details[0].find_elements(By.XPATH,"//span[@class='property-info__property-type']")
                if house_properties_list:
                    for detail in house_properties_list:
                        try:
                            attribute = detail.get_attribute("aria-label")
                            if attribute:
                                if "bedroom" in attribute.lower():
                                    data["Bedrooms"] = attribute.title()
                                elif "bathroom" in attribute.lower():
                                    data["Bathroom"] = attribute.title()
                                elif "parking" in attribute.lower():
                                    data["Parking"] = attribute.title()
                        except Exception as e:
                            print(f"Error: {e}")
        
        data["Property URL"]=driver.current_url

        return data

    def json_to_csv(self,json_file_path, csv_file_path):
        # Read the JSON data from the file
        with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
            home_details = json.load(jsonfile)

        # Check if home_details is a list of dictionaries
        if not isinstance(home_details, list) or not all(isinstance(i, dict) for i in home_details):
            raise ValueError("JSON data must be a list of dictionaries")

        # Filter out empty dictionaries or dictionaries with all empty values
        filtered_home_details = [home for home in home_details if home and any(home.values())]

        if not filtered_home_details:
            raise ValueError("No valid data found to write to CSV")

        # Open the CSV file for writing
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            # Define the header names based on the keys of the first dictionary in filtered_home_details
            fieldnames = filtered_home_details[0].keys()

            # Create a DictWriter object with the specified fieldnames and the CSV file object
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Iterate over each dictionary in filtered_home_details and write it as a row in the CSV file
            for home in filtered_home_details:
                writer.writerow(home)


    def write_home_details(self,home_details, json_file_path):
        try:
            # Check if the JSON file exists and read the existing data if it does
            if os.path.isfile(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
                    try:
                        existing_data = json.load(jsonfile)
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []

            # Append new home details to the existing data
            existing_data.extend(home_details)

            # Write the updated data back to the JSON file
            with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(existing_data, jsonfile, ensure_ascii=False, indent=4)

        except PermissionError:
            # Handle permission error, usually occurs if the file is open elsewhere
            new_json_file_path = os.path.join(os.path.dirname(json_file_path), 'home_details_1.json')
            with open(new_json_file_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(home_details, jsonfile, ensure_ascii=False, indent=4)

    def get_random_useragent(self):
        ua = UserAgent()
        chrome_user_agent = ua.chrome
        return chrome_user_agent

    def get_data(self,driver):
        data_dict={}
        house_names = driver.find_elements(By.XPATH, "//a[@class='details-link residential-card__details-link']//span")
        house_url = driver.find_elements(By.XPATH, "//a[@class='details-link residential-card__details-link']")
        for names,urls in zip(house_names,house_url):
            data_dict[urls.get_attribute("href")]=names.get_attribute('innerHTML')
        return(data_dict)

    def show_info_with_copy_button(self,master_url):
        def on_ok():
            root.destroy()

        def on_copy_url():
            root.destroy()

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

        root.wait_window(root)
    
    
    def main(self):
        master_url="https://www.realestate.com.au/"
        chrome_process,port=self.get_chrome_process(is_main=True)

        # Create Chrome options
        chrome_user_agent = self.get_random_useragent()
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        chrome_options.add_argument(f"user-agent={chrome_user_agent}")

        # Connect to the existing Chrome instance
        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.maximize_window()
        except WebDriverException as e:
            print(f"Error maximizing window: {e}")

        # Now you can interact with the existing Chrome session
        self.show_info_with_copy_button(master_url)
        original_url=''
        driver_headless=None
        try:                                                                                       
            while not self.is_chrome_window_closed():
                while "/buy/" not in driver.current_url.lower():
                    if self.is_chrome_window_closed():
                        raise NoSuchWindowException
                    time.sleep(1)
                if driver.current_url != original_url:
                    original_url=driver.current_url
                    # If the URL contains '/buy/', fetch the data
                    data_dict = self.get_data(driver=driver)
                    chrome_headless, headless_port = self.get_chrome_process(is_main=False,headless=False)

                    try:
                        chrome_user_agent = self.get_random_useragent()
                        chrome_options_headless = Options()
                        chrome_options_headless.add_experimental_option("debuggerAddress", f"127.0.0.1:{headless_port}")
                        chrome_options_headless.add_argument(f"user-agent={chrome_user_agent}")
                        chrome_options_headless.add_argument("--disable-gpu")
                        chrome_options_headless.add_argument("--no-sandbox")
                        chrome_options_headless.add_argument("--disable-dev-shm-usage")
                        
                        
                        # Connect to the existing Chrome instance
                        driver_headless = webdriver.Chrome(options=chrome_options_headless)
                        try:
                            driver_headless.maximize_window()
                        except WebDriverException as e:
                            print(f"Error maximizing window: {e}")
                        
                        home_details = []
                        counter=0
                        for url,data_list in data_dict.items():
                            if counter==3:
                                break
                            counter+=1
                            driver_headless.get(url)
                            names = self.get_page_details(driver_headless)
                            time.sleep(random.uniform(9,15))
                            home_details.append(names)
                        self.write_home_details(home_details, self.json_file_path)
                    except Exception as e:
                        print(f"Error initializing headless WebDriver: {e}")
                    finally:
                        # Close the browser
                        if driver_headless:
                            self.close_driver(driver_headless)
                        
                        # Terminate the Chrome process opened by the script
                        if not self.is_chrome_window_closed():
                            chrome_headless.kill()
                            chrome_headless.wait()


        except NoSuchWindowException:
            # Close the browser
            if driver_headless:
                self.close_driver(driver_headless)
            
            # Terminate the Chrome process opened by the script
            if not self.is_chrome_window_closed():
                chrome_process.kill()
                chrome_process.wait()
            print("Selenium window closed")
            exit(1)
        except Exception as e:
            print(f"error here {e}")
        
        finally:
            # Close the browser
            if driver_headless:
                self.close_driver(driver_headless)
            
            # Terminate the Chrome process opened by the script
            if not self.is_chrome_window_closed():
                chrome_process.kill()
                chrome_process.wait()
            self.json_to_csv(self.json_file_path,self.csv_file_path)