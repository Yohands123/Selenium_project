from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from booking.booking_filtration import BookingFiltration
from . import constants as const
from booking.booking_report import BookingReport
from prettytable import PrettyTable
import os
import time

class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:/webdrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['Path'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
        time.sleep(2)

    def dismiss_sign_in_info(self):
        try:
            dismiss_button = self.find_element(By.XPATH, '//button[@aria-label="Dismiss sign-in info."]')
            dismiss_button.click()
            print("Dismiss button clicked successfully.")
        except Exception as e:
            print(f"Error clicking dismiss button: {e}")

    def change_currency(self, currency=None):
        try:
            currency_picker_button = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]'))
            )
            currency_picker_button.click()

            currency_option = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH, f'//div[contains(@class, "CurrencyPicker_currency") and text()="{currency}"]'
                ))
            )
            currency_option.click()
            print(f"Currency changed to: {currency}")
        except TimeoutException:
            print("Timeout: Could not find or click the currency option.")
        except Exception as e:
            print(f"Currency change error: {e}")

    def select_place_to_go(self, place_to_go):
        try:
            search_field = WebDriverWait(self, 10).until(
                EC.visibility_of_element_located((By.NAME, "ss"))
            )
            search_field.clear()
            search_field.send_keys(place_to_go)

            dropdown_option = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//div[contains(@class, "ce5ee7d913") and .//div[text()="{place_to_go}"]]'))
            )
            dropdown_option.click()
            print(f"Successfully selected the place: {place_to_go}")

        except Exception as e:
            print(f"Error selecting place: {e}")

    def select_dates(self, check_in_date, check_out_date):
        try:
            calendar_button = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.ID, "calendar-searchboxdatepicker-tab-trigger"))
            )
            calendar_button.click()

            check_in_element = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]'))
            )
            check_in_element.click()

            check_out_element = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]'))
            )
            check_out_element.click()

            print(f"Selected check-in date: {check_in_date} and check-out date: {check_out_date}")

        except Exception as e:
            print(f"Error selecting dates: {e}")

    def select_adults(self, count=1):
        try:
            occupancy_element = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-testid="occupancy-config-icon"]'))
            )
            occupancy_element.click()

            adults_value_element = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.d723d73d5f'))
            )
            plus_button_element = self.find_element(By.XPATH, '//button[contains(@aria-label, "Increase number of Adults")]')
            minus_button_element = self.find_element(By.XPATH, '//button[contains(@aria-label, "Decrease number of Adults")]')

            while True:
                current_adults = int(adults_value_element.text.strip())
                if current_adults < count:
                    plus_button_element.click()
                elif current_adults > count:
                    minus_button_element.click()
                else:
                    break

            done_button = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[span[text()="Done"]]'))
            )
            done_button.click()

            print(f"Successfully selected {count} adults.")
        except Exception as e:
            print(f"Error selecting adults: {e}")

    def click_search(self):
        try:
            search_button = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"] span.e4adce92df'))
            )
            search_button.click()
            print("Search button clicked successfully.")
        except Exception as e:
            print(f"Error clicking search button: {e}")

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4, 5)
        filtration.sort_price_highest_first()
    def report_results(self):
        hotel_boxes = self.find_element(By.ID, 'hotellist_inner')

        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)