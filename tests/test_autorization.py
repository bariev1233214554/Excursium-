import os
import time
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

def test_authorization_flow():
    """Эта функция берет email и password из файла .env и производит авторизацию.
        Тест пройден если авторизация успешна или если сайт выдал ошибку "Неверная почта или пароль" """
    load_dotenv()
    TEST_EMAIL = os.getenv("TEST_EMAIL")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD")

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://excursium.com/Client/Login")
#ВВод email и password
        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        email_input.send_keys(TEST_EMAIL)
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_input.send_keys(TEST_PASSWORD)
# Кнопка Войти
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#login-btn")))
        login_button.click()
        time.sleep(5)
# Сообщение об успешной или ошибочной авторизации
        locator = (By.CSS_SELECTOR,
                   "section#login-vue > div > div:nth-of-type(2) > div > div:nth-of-type(7)")
        try:
            code_input = wait.until(EC.element_to_be_clickable(locator))
            print (" ")
            print("Email или password неверны.")

        except:
            wait.until(lambda d: "login" not in d.current_url)
            current_url = driver.current_url
            print(f"Текущий адрес страницы: {current_url}")

            assert "login" not in current_url, f"Ошибка: мы всё еще на странице логина! URL: {current_url}"
            print("Тест пройден успешно: вход выполнен!")

    except Exception as e:
        print(f" Произошла ошибка: {e}")
        driver.save_screenshot("error_screenshot.png")
        raise e
    finally:

        print("Закрываем браузер...")
        driver.quit()