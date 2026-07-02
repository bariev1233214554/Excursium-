import os
import time
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By


def test_registration_flow():
    """Эта функция берет данные из файла .env и
     производит регистрацию. Если регистрация успешна - тест пройдет. При Негативном сценарии тест не пройден
    """

    load_dotenv()
    TEST_EMAIL = os.getenv("TEST_EMAIL")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD")
    ТEST_FAMALU = os.getenv("ТEST_FAMALU")
    TEST_NAME = os.getenv("TEST_NAME")
    TEST_FIRST = os.getenv("TEST_FIRST")
    TEST_SCHOOL = os.getenv("TEST_SCHOOL")
    TEST_PLAN = os.getenv("TEST_PLAN")
    TEST_PHONE = os.getenv("TEST_PHONE")

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
        time.sleep(10)


        code_input_locat = (By.CSS_SELECTOR, "section#login-vue > div > div:nth-of-type(2) > div:nth-of-type(5) > div:nth-of-type(2) > input")
        code_input = wait.until(EC.element_to_be_clickable(code_input_locat))
        assert code_input.is_displayed(), "Поле для ввода кода не появилось!"
        print("Страница ввода логина и пароля пройдена.")
        time.sleep(30)
#ВВодим код из письма почтового ящика

#Заполняем поля регистрации из фаила evn
        Famulu_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1"]/div[2]/input')))
        Famulu_input.clear()
        Famulu_input.send_keys(ТEST_FAMALU)

        Name_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1"]/div[3]/input')))
        Name_input.clear()
        Name_input.send_keys(TEST_NAME)

        first_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1"]/div[4]/input')))
        first_input.clear()
        first_input.send_keys(TEST_FIRST)
        time.sleep(5)

        key_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1"]/div[6]/button[1]')))
        key_input.click()
        print("Страница знакомства пройдена.")
        time.sleep(5)
#выбираем роль - в файле evn
        rol_input = wait.until(EC.visibility_of_element_located((By.XPATH, TEST_PLAN)))
        rol_input.click()
#Поле школа из файла evn
        school_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-2"]/div[4]/input')))
        school_input.send_keys(TEST_SCHOOL)
        time.sleep(5)

        keyy_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="next-client-type"]')))
        keyy_input.click()
        print("Страница школы пройдена.")
        time.sleep(5)
# Поле телефон из файла evn
        Phone_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="phone"]')))
        Phone_input.send_keys(TEST_PHONE)
        time.sleep(5)
# Выбор способов связи
        Tel_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3"]/div[3]/div[2]/div[1]/div[3]')))
        Tel_input.click()

        Wat_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3"]/div[3]/div[2]/div[2]/div[3]')))
        Wat_input.click()

        Max_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3"]/div[3]/div[2]/div[3]/div[3]')))
        Max_input.click()

        Em_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3"]/div[3]/div[2]/div[4]/div[3]')))
        Em_input.click()
        time.sleep(5)

        Em_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="step-3"]/div[4]/button[2]')))
        Em_input.click()
        print("Страница связи пройдена. Тест успешно завершон.")
        time.sleep(5)


    except Exception as e:
        print(f" Произошла ошибка: {e}")
        driver.save_screenshot("error_screenshot.png")
        raise e
    finally:
        driver.quit()
