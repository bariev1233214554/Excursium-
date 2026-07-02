import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager


def apply_and_reset_filter(driver, wait, css_selector, filter_name):
    """Эта функция дополнительная Она применяет фильтра и сравнивает URL для уменьшения кода"""
    url_before = driver.current_url
 # Применяем фильтр
    filter_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    filter_element.click()
# Ждём изменения URL
    wait.until(lambda d: d.current_url != url_before)
    url_after = driver.current_url
    print(" ")
    print(f"Тест пройден: для фильтра '{filter_name}'")
# Сбрасываем фильтр: ищем элемент заново
    filter_element_reset = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    filter_element_reset.click()
# Ждём возврата к исходному URL
    wait.until(lambda d: d.current_url == url_before)


def test_filtration():
    """Эта функция проверяет все фильтры:после нажатия на фильтр сверяет Url.
    Если Url отличается от начального - фильтр сработал."""

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        URL="https://excursium.com/ekskursii-dlya-shkolnikov/list"
        driver.get(URL)

# Принятие куков
        cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Принять')]")))
        cookie_btn.click()
# Убрали time.sleep — ждём исчезновения кнопки
        wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[contains(text(), 'Принять')]")))
# Проверяем фильтра
        apply_and_reset_filter(driver, wait, "input#popolarType_5", "С обедами")
        apply_and_reset_filter(driver, wait, "input#popolarType_6", "С мастер-классами")
        apply_and_reset_filter(driver, wait, "input#popolarType_7", "Для рейтинга школы")
        apply_and_reset_filter(driver, wait, "input#popolarType_36", "На выпускной")
        apply_and_reset_filter(driver, wait, "ul#collapse-grade > li > label", "1 класс")
        apply_and_reset_filter(driver, wait, "ul#collapse-grade > li:nth-of-type(2) > label", "2 класс")
        apply_and_reset_filter(driver, wait, "ul#collapse-grade > li:nth-of-type(3) > label", "3 класс")
        apply_and_reset_filter(driver, wait, "ul#collapse-grade > li:nth-of-type(4) > label", "4 класс")
        apply_and_reset_filter(driver, wait, "ul#collapse-grade > li:nth-of-type(5) > label", "5 класс")
        apply_and_reset_filter(driver, wait, "ul#collapse-grade > li:nth-of-type(6) > label", "6 класс")
        apply_and_reset_filter(driver, wait, "ul#collapse-grade > li:nth-of-type(7) > label", "7 класс")
        apply_and_reset_filter(driver, wait, "ul#collapse-grade > li:nth-of-type(8) > label", "8 класс")
        apply_and_reset_filter(driver, wait, "ul#collapse-grade > li:nth-of-type(9) > label", "9 класс")
        apply_and_reset_filter(driver, wait, "ul#collapse-grade > li:nth-of-type(10) > label", "10 класс")
        apply_and_reset_filter(driver, wait, "ul#collapse-grade > li:nth-of-type(11) > label", "11 класс")
        apply_and_reset_filter(driver, wait, "input#priceRange_1000", "1000-1500")
        apply_and_reset_filter(driver, wait, "input#priceRange_1500", "1500-2500")
        apply_and_reset_filter(driver, wait, "input#priceRange_2500", "25000-3500")
        apply_and_reset_filter(driver, wait, "input#priceRange_3500", "3500+")
        apply_and_reset_filter(driver, wait, "input#time_6", "Полдня")
        apply_and_reset_filter(driver, wait, "input#time_7", "Целый день")
        apply_and_reset_filter(driver, wait, "input#regions_77", "Москва")
        apply_and_reset_filter(driver, wait, "input#regions_50", "Московская обдасть")
        apply_and_reset_filter(driver, wait, "input#regions_40", "Калужская область")
        apply_and_reset_filter(driver, wait, "input#regions_33", "Владимирская область")
    # Открываем все фильтра
        full_field = driver.find_element(By.CSS_SELECTOR,
                                       "div#collapse-regions > a")
        full_field.click()
        apply_and_reset_filter(driver, wait, "input#regions_71", "Тульская область")
        apply_and_reset_filter(driver, wait, "input#regions_76", "Ярославская область")
        apply_and_reset_filter(driver, wait, "input#regions_62", "Рязанская область")
        apply_and_reset_filter(driver, wait, "input#activity3131", "Низкий уровень")
        apply_and_reset_filter(driver, wait, "input#activity3232", "Средний уровень")
        apply_and_reset_filter(driver, wait, "input#activity3333", "Высокий уровень")
    # Проверяем несколько фильтров сразу

        on_field = driver.find_element(By.CSS_SELECTOR,
                                                    "input#popolarType_5")
        on_field.click()
        to_field = driver.find_element(By.CSS_SELECTOR,
                                                    "ul#collapse-grade > li:nth-of-type(2) > label")
        to_field.click()
        fr_field = driver.find_element(By.CSS_SELECTOR,
                                                    "input#priceRange_1000")
        fr_field.click()
        fo_field = driver.find_element(By.CSS_SELECTOR,
                                                    "input#time_7")
        fo_field.click()
        fa_field = driver.find_element(By.CSS_SELECTOR,
                                                    "input#regions_40")
        fa_field.click()
        si_field = driver.find_element(By.CSS_SELECTOR,
                                                    "input#activity3131")
        si_field.click()

        si_field = driver.find_element(By.CSS_SELECTOR,
                                       "input#activity3131")
        si_field.click()
        time.sleep(3)

        new_Url = driver.current_url

        if new_Url != URL:
            print("Тест пройден: Несколько фильтров.")
        else:
            print("Ошибка")
            assert False
    # Проверяем кнопку сброса фильтров
        clean_field = driver.find_element(By.CSS_SELECTOR,
                                          "div#offcanvasSidebar > div:nth-of-type(3) > button")
        clean_field.click()
        time.sleep(3)
        newclean_Url = driver.current_url
        if newclean_Url == URL:
            print("Тест пройден: Очистка фильтра.")
        else:
            print("Ошибка")
            assert False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        driver.save_screenshot("error_screenshot.png")
        raise
    finally:
        driver.quit()


