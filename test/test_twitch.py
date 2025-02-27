import logging
import random
import time

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
        logging.debug("Finished setup_method")

    def teardown_method(self):
        self.driver.quit()
        logging.debug("Finished teardown_method")

    def enter_search_page(self) -> None:
        """Find and click search button
        """
        search_element = self.driver.find_element(By.CSS_SELECTOR, ".ScInteractableBase-sc-ofisyf-0:nth-child(2) .CoreText-sc-1txzju1-0")
        search_element.click()
        logging.debug("Entered search page")

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
        logging.debug(f"Found and enter category:{category_name}")

    def scroll_page(self, pixel_x: int = 0, pixel_y: int = 0) -> None:
        """Scroll Page with script, as top-left cornor as (0,0)

        Args:
            pixel_x (int): horizontal length by pixel. possitive for going right, negative for left.
            pixel_y (int): vertical length by pixel. positive for going down, negative for up.
        """
        time.sleep(0.5)
        self.driver.execute_script(f"window.scrollBy({pixel_x}, {pixel_y})")
        logging.debug(f"Scrolled page. x:{pixel_x}, y:{pixel_y}")

    def check_for_consent(self, view_content: bool = True) -> None:
        """Check if video is masked with consent warning, press consent button if desire.

        Args:
            view_content (bool, optional): control pressing consent button, True to press. Defaults to True.
        """
        try:
            verify_button = self.driver.find_element(By.XPATH, '//*[@id="channel-player-gate"]/div/div/div[4]/div/button')
            logging.info('Consent button found')
            if view_content:
                verify_button.click()
                logging.info('Clicked button.')
        except NoSuchElementException:
            logging.info('No consent button found')

    def wait_for_content(self) -> None:
        # Locate the video element and check if loaded
        element = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "video")))
        self.wait.until(lambda _ : self.driver.execute_script("return !arguments[0].paused;", element))

    @pytest.mark.parametrize("y_scroll", [0, 300, 600, 900, 1200])
    @pytest.mark.nondestructive
    def test_testopen(self, y_scroll: int):
        target_category = "StarCraft II"

        self.enter_search_page()
        self.search_and_enter_category(target_category)
        self.scroll_page(pixel_y=y_scroll)
        self.scroll_page(pixel_y=y_scroll)

        ## get current visible range
        main = self.driver.find_element(By.TAG_NAME, "main")
        front = self.driver.find_element(By.XPATH, '//*[@id="page-main-content-wrapper"]/div[1]')
        button = front.find_element(By.TAG_NAME, 'button')
        banner_trigger_height = button.size['height'] + button.location['y']
        lower_bound = (y_scroll * 2)
        if lower_bound > banner_trigger_height:
            logging.info('Scrolled over subscribe button, trigger banner')
        try:
            banner = self.driver.find_element(By.XPATH, '//*[@id="twilight-sticky-header-root"]/div/div')
            lower_bound += banner.size['height']
        except NoSuchElementException:
            logging.warning("No banner found")

        bar = self.driver.find_element(By.XPATH, '//*[@id="root"]/div[2]')
        upper_bound = lower_bound + main.size['height'] - bar.size['height']
        visible_range = range(lower_bound, upper_bound)
        ## filter visible streamer and click
        titles = self.driver.find_elements(By.TAG_NAME, "h2")
        logging.debug(f'Found titles elements:{len(titles)}')
        logging.debug(f'Visible range:{lower_bound}, {upper_bound}')
        for title in titles:
            logging.debug(f"Position:{title.location}, Title: {title.text}")
        visible_titles = [title for title in titles if title.is_displayed() and title.location['y'] in visible_range]
        logging.info(f'Visible titles elements: {[v.text for v in visible_titles]}')
        picked_title = random.choice(visible_titles)
        logging.info(f'choosed title name:{picked_title.text}')
        time.sleep(3)
        self.driver.execute_script(f"window.scrollTo(0,{picked_title.location['y']})")
        if picked_title.location['y'] > banner_trigger_height:
            logging.info("Title position cause banner pop out, try to find banner")
            try:
                banner = self.driver.find_element(By.XPATH, '//*[@id="twilight-sticky-header-root"]/div/div')
                self.driver.execute_script(f"window.scrollBy(0,{-banner.size['height'] * 2})")
            except NoSuchElementException:
                logging.warning("No banner found while trying to click the title")
        picked_title.click()

        self.check_for_consent()
        self.wait_for_content()
        assert self.driver.save_screenshot('./test_testopen.png'), "Failed to save screenshot"