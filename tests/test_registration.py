import os
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By


def test_registration_flow():
    """Эта функция берет email и password из файла .env и
     производит регистрацию до момента ввода проверочного кода из email.
     Если загружается страница ввода кода - тест пройден.
     Так же проверяется уже зарегистрированный email.
     Если email зарегистрирован, то тест тоже пройден.
    В тесте использованы длинные селекторы потому что
    проблема в том, что Selenium физически не может найти этот элемент по id, class или тексту и заваливает тест"""

    load_dotenv()
    TEST_EMAIL = os.getenv("TEST_EMAIL")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD")

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://excursium.com/Client/Login")

# Кнопка регистрация
        reg_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Регистрация']")))
        driver.execute_script("arguments[0].click();", reg_btn)

        time.sleep(5)
# ВВод email и password
# Использован  SELECTOR потому Selenium физически не может найти этот элемент другими спосабами. пытался по id и XPath и по названию.
        email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "section#login-vue > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(3) > input")))
        email_input.send_keys(TEST_EMAIL)

        password_input = driver.find_element(By.CSS_SELECTOR, "section#login-vue > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(4) > div > input")
        password_input.send_keys(TEST_PASSWORD)

# Галочка согласия
        agreement_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "isAgreement")))
        if not agreement_checkbox.is_selected():
            agreement_checkbox.click()
        else:
            print("Галочка уже стояла.")

# Кнопка регистрации
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#registraion-btn")))
        login_button.click()
        time.sleep(5)
# Проверка: зврегистрирован ли email
        locator = (By.CSS_SELECTOR,
                   "section#login-vue > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(7)")

        try:
            code_input = wait.until(EC.element_to_be_clickable(locator))
            print("Email уже зарегестрирован.")
            assert True, "Тест пройден: поле для ввода кода отображено."

        except TimeoutException:
            code_input_locat = (By.CSS_SELECTOR, "section#login-vue > div > div:nth-of-type(2) > div:nth-of-type(5) > div:nth-of-type(2) > input")
            code_input = wait.until(EC.element_to_be_clickable(code_input_locat))


            assert code_input.is_displayed(), "Поле для ввода кода не появилось!"
            print("Тест пройден: поле для ввода кода успешно отображено.")

            wait.until(lambda d: "login" not in d.current_url)
            current_url = driver.current_url

            assert "login" not in current_url, f"Ошибка: мы всё еще на странице логина! URL: {current_url}"
            print("Тест пройден успешно: вход выполнен!")

    except Exception as e:
        print(f" Произошла ошибка: {e}")
        driver.save_screenshot("error_screenshot.png")
        raise e
    finally:
        driver.quit()
