from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request


class ImageDownloader:

    def __init__(self, url, pages, chromedriver_location):
        self.url = url
        self.pages = pages
        self.chromedriver_location = chromedriver_location
        self.driver = webdriver.Chrome(self.chromedriver_location)

    def run(self):
        count = 1

        for i in range(1, self.pages + 1):
            site = self.url + "/page" + str(i)
            self.driver.get(site)
            self.scroll_to_bottom()

            div_list = self.driver.find_elements_by_class_name("photo-list-photo-interaction")
            interim_url = []

            for div in div_list:
                interim_url.append(div.find_element_by_css_selector("a").get_attribute("href"))

            for save_url in interim_url:
                pic_url = self.get_image_loc(save_url)
                val = str(count) + ".jpg"
                urllib.request.urlretrieve(pic_url, val)
                count += 1

    def scroll_to_bottom(self):
        body_loc = self.driver.find_element_by_tag_name("body")

        for j in range(35):
            body_loc.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

    def get_image_loc(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)
        node = self.driver.find_element_by_class_name("download ")
        address = node.find_element_by_css_selector("a").get_attribute("href")
        address = address[0:len(address) - 2] + "o/"
        self.driver.get(address)
        self.driver.implicitly_wait(5)
        pic_node = self.driver.find_element_by_id("allsizes-photo")
        pic_url = pic_node.find_element_by_css_selector("img").get_attribute("src")
        return pic_url
