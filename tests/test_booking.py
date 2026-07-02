import os
import time
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By


def test_booking_flow():
    """Эта функция берет email, password, страницу с экскурсией, дату, телефон из файла .env
    и производит авторизацию, затем переходит на страницу с экскурсией, заданную в файле и производит бронирование
    по данным телефона и даты из файла. В качестве имени использовано фиксированное - Наташа,
    выбраны все каналы связи для бронирования.
        Тест пройден если авторизация успешна, бронирование произведено, сообщение "Спасибо! Заявка принята" появилось """
    load_dotenv()
    TEST_EMAIL = os.getenv("TEST_EMAIL")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD")
    TEST_URL = os.getenv("TEST_URL")
    TEST_DATA = os.getenv("TEST_DATA")
    TEST_PHONE= os.getenv("TEST_PHONE")

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://excursium.com/Client/Login")
# АВТОРИЗАЦИЯ
        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        email_input.send_keys(TEST_EMAIL)
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_input.send_keys(TEST_PASSWORD)
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#login-btn")))
        login_button.click()
        time.sleep(5)
# Открытие экскурсии
        driver.get(TEST_URL)
        time.sleep(5)
# Принятие куков
        cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Принять')]")))

        cookie_btn.click()
# Открытие формы бронирования
        book_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Заказать экскурсию']"))
        )
        book_button.click()
# Выбор размера группы
        time.sleep(5)
        people_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div#bookingModal > div > div > div:nth-of-type(2) > div > div > label"))
        )
        people_button.click()
        time.sleep(5)

        peopleS_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "div#bookingModal > div > div > div:nth-of-type(2) > div > div > label:nth-of-type(2)"))
        )
        peopleS_button.click()
        time.sleep(5)

        peoplel_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "div#bookingModal > div > div > div:nth-of-type(2) > div > div > label:nth-of-type(3)"))
        )
        peoplel_button.click()
        time.sleep(5)
# Выбор даты
        target_date_str = TEST_DATA
        date_field = driver.find_element(By.CSS_SELECTOR, "input#bookingDates")

        driver.execute_script("""
            var element = arguments[0];
            var dateValue = arguments[1];
            element.value = dateValue;
            element.dispatchEvent(new Event('input', { bubbles: true }));
            element.dispatchEvent(new Event('change', { bubbles: true }));
        """, date_field, target_date_str)
# Ввод Имени
        name_field = driver.find_element(By.CSS_SELECTOR, "input#bookingUserName")
        name_field.send_keys("Наташа")
# Ввод телефона
        pfone_field = driver.find_element(By.CSS_SELECTOR, "input#orderPhone")
        pfone_field.send_keys(TEST_PHONE)
# Ввод примечаний
        re_field = driver.find_element(By.CSS_SELECTOR, "div#bookingModal > div > div > div:nth-of-type(2) > div:nth-of-type(4) > small")
        re_field.click()

        ree_field = driver.find_element(By.CSS_SELECTOR,
                                       "div#bookingModal > div > div > div:nth-of-type(2) > div:nth-of-type(5) > textarea")
        ree_field.send_keys('ТЕСТ')
        time.sleep(5)
# Выбор средств связи


        svazW_field = driver.find_element(By.CSS_SELECTOR, "div#bookingModal > div > div > div:nth-of-type(2) > div:nth-of-type(6) > div > button:nth-of-type(3)")
        svazW_field.click()
        svazM_field = driver.find_element(By.CSS_SELECTOR,
                                          "div#bookingModal > div > div > div:nth-of-type(2) > div:nth-of-type(6) > div > button:nth-of-type(2)")
        svazM_field.click()
        svazPh_field = driver.find_element(By.CSS_SELECTOR,
                                          "div#bookingModal > div > div > div:nth-of-type(2) > div:nth-of-type(6) > div > button:nth-of-type(4)")
        svazPh_field.click()
        Ok_field = driver.find_element(By.CSS_SELECTOR,
                                          "input#agreeCheck")
# Галочка
        Ok_field.click()
        send_field = driver.find_element(By.CSS_SELECTOR,
                                       "div#bookingModal > div > div > div:nth-of-type(3) > button")
        send_field.click()
        time.sleep(5)
        locator = (By.CSS_SELECTOR,
                   "div#bookingSuccess > div > div > div")
        try:
            code_input = wait.until(EC.element_to_be_clickable(locator))
            print(" ")
            print("Бронирование успешно")

        except:
            print("Произошла ошибка")
            assert False

    except Exception as e:
        print(f" Произошла ошибка: {e}")
        driver.save_screenshot("error_screenshot.png")
        raise e
    finally:

        print("Закрываем браузер...")
        driver.quit()

