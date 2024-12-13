from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
os.system('taskkill /f /im chromedriver.exe')
os.system('taskkill /f /im chrome.exe')

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

def getItemDivs(url):
    # Создаем объект ChromeOptions
    options = Options()

    # Запускаем драйвер с указанными параметрами
    driver = webdriver.Chrome()

    driver.get(url)
    print(driver.title)
    driver.quit()
    

# Пример использования
getItemDivs('https://www.yahoo.com')
