import requests
import platform

from requests.exceptions import HTTPError
from sys import stdin

from image_downloader import ImageDownloader
from chromedriver_finder import ChromedriverFinder


def main():
    url = get_url()
    os_type = get_os()
    finder = ChromedriverFinder(os_type)
    driver_loc = finder.find_chromedriver()
    downloader = ImageDownloader(url, driver_loc)
    downloader.run()


def get_url():
    while True:
        print()
        stdin.flush()
        url = input("Enter the Flickr URL for the library you want to download. Do NOT include the page number,\n"
                    "and be sure to include the 'https://' at the beginning: ")
        if url[len(url) - 1] == "/":
            url = url[0:len(url) - 1]
        try:
            request = requests.get(url)
            request.raise_for_status()
            if request.status_code != 200:
                print("Error. This URL is not correct. Error Code " + str(request.status_code))
            else:
                break
        except HTTPError as http_err:
            print("Error. This is not a valid URL. Exception Code: " + str(http_err))
        except Exception as err:
            print("Error: " + str(err))
    return url


def get_os():
    return platform.system()


main()
