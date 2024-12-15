from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        # Locate the star rating filtration box
        star_filtration_box = self.driver.find_element(By.CLASS_NAME, 'dff7374ff6')
        star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, 'div[class^="a53cbfa6de"]')

        for star_value in star_values:
            for attempt in range(3):  # Retry mechanism for stale elements
                try:
                    for star_element in star_child_elements:
                        label_element = star_element.find_element(By.CSS_SELECTOR, 'label div div div')
                        if str(label_element.text.strip()) == f'{star_value} stars':
                            checkbox = star_element.find_element(By.TAG_NAME, 'input')
                            if not checkbox.is_selected():
                                checkbox.click()
                                print(f"Star rating {star_value} applied successfully.")
                    break  # Exit retry loop if successful
                except StaleElementReferenceException:
                    print(f"Stale element detected for star rating {star_value}. Retrying...")
                    time.sleep(1)

    def sort_price_highest_first(self):
        try:
            # Click on the "Sort by" dropdown
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.cac967781c'))
            )
            dropdown.click()

            # Select the "Price (highest first)" option
            price_high_to_low = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-id="price_from_high_to_low"]'))
            )
            price_high_to_low.click()
            print("Sorted results by 'Price (highest first)'.")
        except Exception as e:
            print(f"Error while sorting: {e}")
