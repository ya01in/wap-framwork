import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

  @pytest.mark.nondestructive
  def test_testopen(self):
    target_category = "StarCraft II"

    ## enter_search_page

    ## search_and_enter_category

    ## scroll page

    ## find Streamer and click

    ## check if consent button shows up

    ## Locate the video element and check if loaded
