from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver
import os

def configure_chrome(download_folder):
    # Настраиваем папку загрузки
    chrome_options = Options()
    prefs = {
        "download.default_directory": download_folder,  # Указываем путь для загрузки
        "download.prompt_for_download": False,          # Не запрашивать подтверждение
        "download.directory_upgrade": True,             # Разрешить обновление папки загрузки
        "safebrowsing.enabled": True                    # Включить безопасный режим загрузки
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("detach", True)
    return chrome_options


# Функция для парсинга и выполнения действий
def get_weather_archive(download_folder):

    # Настройка опций Chrome
    chrome_options = configure_chrome(download_folder)

    # Запускаем драйвер
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    nums = []
    try:
        # Переходим на главную страницу
        driver.get("https://rp5.ru/Погода_в_Тюменской_области")

        # Находим элементы с классом href12 и переходим по ссылкам
        href12_links = driver.find_elements(By.CLASS_NAME, "href12")
        for i in range(len(href12_links)):
            # Заново ищем ссылки (в случае изменения DOM)
            href12_links = driver.find_elements(By.CLASS_NAME, "href12")
            
            # Клик на текущую ссылку
            href12_links[i].click()
            time.sleep(2)  # Подождать загрузку новой страницы
            
            # Ожидание элементов city_link
            city_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "city_link"))
            )
            bookmark = driver.current_url
            for j in range(len(city_links)):
                time.sleep(2)
                driver.get(bookmark)
                city_links = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "city_link"))
                )
                city_links[j].click()
                time.sleep(2)
                
                # Переход к ArchiveStrLink
                archive_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "ArchiveStrLink"))
                )
                archive_link.click()
                time.sleep(2)

                num = driver.find_element(By.ID, "wmo_id").get_attribute('value')
                if num in nums:
                    continue
                nums.append(num)
                time.sleep(2)

                element = driver.find_element(By.XPATH, "//div[text()='Скачать архив погоды']")
                # Проверка видимости элемента
                if element.is_displayed() and element.is_enabled():
                    element.click()
                else:
                    print("Элемент скрыт или неактивен.")
                time.sleep(2)

                # Находим и указываем даты в полях
                start_date = driver.find_element(By.ID, "calender_dload")
                start_date.clear()
                start_date.send_keys("01.01.2020")

                end_date = driver.find_element(By.ID, "calender_dload2")
                end_date.clear()
                end_date.send_keys("31.12.2022")

                # Нажимаем кнопку "Выбрать в файл GZ"
                gz_button = driver.find_element(By.XPATH, "//div[contains(@onclick, 'fFileSynopGet')]")
                gz_button.click()
                time.sleep(2)

                # Нажимаем кнопку "Скачать"
                download_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'download/files.synop')]"))
                )
                time.sleep(1)
                download_button.click()
                print("Файл загружен!")
            driver.get("https://rp5.ru/Погода_в_Тюменской_области")
            time.sleep(1)
            

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        # Закрываем драйвер
        time.sleep(20)
        driver.quit()

