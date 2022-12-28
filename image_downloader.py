from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
from selenium.webdriver.common.by import By



class ImageDownloader:

    def __init__(self, url, chromedriver_location):
        self.url = url
        self.chromedriver_location = chromedriver_location
        self.driver = webdriver.Chrome(self.chromedriver_location)

    def run(self):
        saved_page_count = 1
        self.__first_page_setup()
        pages = int(self.__get_max_pages())

        for i in range(1, pages + 1):
            if i != 1:
                self.__iterated_page_setup(i)
            # div_list = self.driver.find_elements_by_class_name("photo-list-photo-interaction")
            div_list = self.driver.find_elements(By.CLASS_NAME,"photo-list-photo-interaction")
            interim_url = []

            for div in div_list:
                # interim_url.append(div.find_element_by_css_selector("a").get_attribute("href"))
                interim_url.append(div.find_element(By.CSS_SELECTOR,"a").get_attribute("href"))

                

            for save_url in interim_url:
                pic_url = self.__get_image_loc(save_url)
                val = str(saved_page_count) + ".jpg"
                urllib.request.urlretrieve(pic_url, val)
                saved_page_count += 1

    def __scroll_to_bottom(self):
        # body_loc = self.driver.find_element_by_tag_name("body")
        body_loc = self.driver.find_element(By.TAG_NAME,"body")

        for j in range(35):
            body_loc.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

    def __get_image_loc(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            node = self.driver.find_element(By.CLASS_NAME,"download ")
            address = node.find_element(By.CSS_SELECTOR,"a").get_attribute("href")
            address = address[0:len(address) - 2] + "o/"
            self.driver.get(address)
            self.driver.implicitly_wait(5)
            pic_node = self.driver.find_element(By.ID,"allsizes-photo")
            pic_url = pic_node.find_element(By.CSS_SELECTOR,"img").get_attribute("src")
            return pic_url
        except:
            return None

    def __get_max_pages(self):
        page_loc = self.driver.find_element(By.CLASS_NAME,"pagination-view")
        pages = page_loc.find_elements(By.CSS_SELECTOR,"span")
        page_num = 1
        for page in pages:
            if page.text.isdigit():
                page_num = page.text
        return page_num

    def __first_page_setup(self):
        site = self.url + "/page1"
        self.driver.get(site)
        self.__scroll_to_bottom()

    def __iterated_page_setup(self, page_num):
        site = self.url + "/page" + str(page_num)
        self.driver.get(site)
        self.__scroll_to_bottom()
