from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service

import time
import sys


def login(driver, user, password):
  
    WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/grafana-app/div/div/react-container/div/div/div[2]/div/div/form/div[1]/div[2]/div/div/input')))
        
    login_user = driver.find_element("xpath","/html/body/grafana-app/div/div/react-container/div/div/div[2]/div/div/form/div[1]/div[2]/div/div/input")
    login_pass = driver.find_element("xpath","/html/body/grafana-app/div/div/react-container/div/div/div[2]/div/div/form/div[2]/div[2]/div/div/input")
    
    login_user.send_keys(user)
    login_pass.send_keys(password)
    
    driver.find_element("xpath",'/html/body/grafana-app/div/div/react-container/div/div/div[2]/div/div/form/button').click()
    
    # if running local grafana without auth use these
    #WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/grafana-app/div/div/react-container/div/div/div[2]/div/form/div[3]/div[2]/a/span/span')))
    #driver.find_element("xpath",'/html/body/grafana-app/div/div/react-container/div/div/div[2]/div/form/div[3]/div[2]/a/span/span').click()
    
    
def save_screenshot(driver, path, sleep_time):
    time.sleep(sleep_time)
    driver.save_screenshot(path)
    
    
def get_screenshot(url, file_path, browser_path, browser_driver_path, user, password, sleep_time):

    browser_options = webdriver.ChromeOptions()
    browser_options.add_argument("--headless")
    browser_options.add_argument("force-device-scale-factor=2.0")
    browser_options.binary_location = browser_path
    service = Service(executable_path=browser_driver_path)
    driver = webdriver.Chrome(service=service, options=browser_options)
    

    driver.set_window_size(1920, 1080)
    driver.get(url)
    
    try:
        login(driver, user, password)
    except Exception as e:
        print("Failed to login: {}".format(e))
        sys.exit(1)

    try:
        save_screenshot(driver, file_path, sleep_time)
    except Exception as e:
        print("Failed to save screenshot: {}".format(e))
        sys.exit(1)

def main():
    #TODO: add basic main for standalone script
    print('Hello')

if __name__ == "__main__":
    main()
