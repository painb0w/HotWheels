from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#comment
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
