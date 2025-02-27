import logging
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class TestView():
    def setup_method(self):
        chrome_option = Options()
        chrome_option.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/114.0.5735.99 Mobile/15E148 Safari/604.1')
        self.driver = webdriver.Chrome(chrome_option)
        self.driver.implicitly_wait(1)
        self.driver.get("https://www.twitch.tv/")
        self.x = 390
        self.y = 844
        self.driver.set_window_size(self.x, self.y)
        self.wait = WebDriverWait(self.driver, timeout=2, poll_frequency=1.0)

    def teardown_method(self):
        self.driver.quit()

    def enter_search_page(self) -> None:
        """Find and click search button
        """
        search_element = self.driver.find_element(By.CSS_SELECTOR, ".ScInteractableBase-sc-ofisyf-0:nth-child(2) .CoreText-sc-1txzju1-0")
        search_element.click()

    def search_and_enter_category(self, category_name: str) -> None:
        """Find and input input bar

        Args:
            category_name (str): Name of the category, case sensitive.
        """
        self.driver.find_element(By.CSS_SELECTOR, ".ScInputBase-sc-vu7u7d-0").send_keys(category_name)
        # wait for catagory content to be displayed
        time.sleep(0.5)
        cat_elements = self.driver.find_element(By.XPATH, '//*[@id="page-main-content-wrapper"]/div/ul/li[1]/a/div/p')
        assert cat_elements.text == category_name, "Failed to find correct category link"
        cat_elements.click()

    def scroll_page(self, pixel_x: int = 0, pixel_y: int = 0) -> None:
        """Scroll Page with script, as top-left cornor as (0,0)

        Args:
            pixel_x (int): horizontal length by pixel. possitive for going right, negative for left.
            pixel_y (int): vertical length by pixel. positive for going down, negative for up.
        """
        time.sleep(0.5)
        self.driver.execute_script(f"window.scrollBy({pixel_x}, {pixel_y})")

    @pytest.mark.parametrize("y_scroll", [200])
    @pytest.mark.nondestructive
    def test_testopen(self, y_scroll: int):
        target_category = "StarCraft II"

        self.enter_search_page()
        self.search_and_enter_category(target_category)
        self.scroll_page(pixel_y=y_scroll)
        self.scroll_page(pixel_y=y_scroll)

        ## find Streamer and click

        ## check if consent button shows up

        ## Locate the video element and check if loaded
