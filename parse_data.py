from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


# Функция для парсинга и выполнения действий
def get_weather_archive(download_folder):

    # Настройка опций Chrome
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # Настройка директории для скачивания
    chrome_options.add_argument(f"--download-default-directory={download_folder}")

    # Запускаем драйвер
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        # Переходим на главную страницу
        driver.get("https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%A2%D1%8E%D0%BC%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B9_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D0%B8")

        # Находим элементы с классом href12 и переходим по ссылкам
        href12_links = driver.find_elements(By.CLASS_NAME, "href12")
        for link in href12_links:
            link.click()
            time.sleep(2)

            # Находим элемент с классом city_link и переходим по ссылке
            city_link = driver.find_element(By.CLASS_NAME, "city_link")
            city_link.click()
            time.sleep(2)

            # Находим элемент ArchiveStrLink и переходим по ссылке
            archive_link = driver.find_element(By.CLASS_NAME, "ArchiveStrLink")
            archive_link.click()
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
            download_button.click()
            time.sleep(50)
            print("Файл загружен!")
            break  # Убираем break, если нужно обработать все ссылки

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        # Закрываем драйвер
        driver.quit()

