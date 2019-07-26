import os
from sys import stdin

from image_downloader import ImageDownloader
import requests
from requests.exceptions import HTTPError


def main():
    url = get_url()
    pages = get_pages()
    chromedriver_location = get_chromedriver_location()
    downloader = ImageDownloader(url, pages, chromedriver_location)
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


def get_pages():
    while True:
        print()
        stdin.flush()
        try:
            pages = int(input("Enter the number of pages in the album: "))
            if pages < 1:
                print("Error. Must have at least 1 page!")
            else:
                break
        except ValueError as val_err:
            print("Error. Not a Number. Please try again. Error: " + str(val_err))
    return pages


def get_chromedriver_location():
    while True:
        print()
        stdin.flush()
        chromedriver_location = input("Enter the location of 'chromedriver.exe'(check the Readme for more info).\n"
                                      "Note: If using windows put two backslashes instead of one"
                                      "(i.e. 'C:\\\\chromedriver_win32\\\\chromedriver.exe'): ")
        if os.path.exists(chromedriver_location):
            break
        else:
            print("Error. Not a correct path to chromedriver. Please try again.")
    return chromedriver_location


main()
