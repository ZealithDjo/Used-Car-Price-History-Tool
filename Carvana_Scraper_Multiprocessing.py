import os
import sys
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import re
import json
import pandas as pd
from datetime import date
from lxml import etree
import multiprocessing as mp


# driver options
def get_driver_options():
    options = Options()
    prefs = {"profile.default_content_setting_values.notifications": 1}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_experimental_option("prefs", prefs)
    return options


# returns BS object using given url
def get_beautifulsoup_obj(url):
    try:
        rr = requests.get(url)
    except requests.exceptions.RequestException:
        return None
    return BeautifulSoup(rr.text, 'html.parser')


def print_list(l):
    for e in l:
        print(e)


def get_vehicle_details(url):
    while 1:
        try:
            # make bs obj from url
            bs = get_beautifulsoup_obj(url)

            vehicleList = []
            # find and get all details of each vehicle on page
            for item in bs.find('body').find_all('a', href=re.compile('/vehicle/[^:]*$')):
                ymm = item.find('div', attrs={'class': 'year-make'}).getText()
                mileage = item.find('div', attrs={'class': 'trim-mileage'}).getText()
                price = item.find('div', attrs={'class': 'upgrades-price'}).getText()
                obj = str(ymm + " " + mileage + " " + price)
                vehicleList.append(obj)
            # print_list(vehicleList)

            # remove unnecessary text
            vehicleList = list(map(lambda x: x.replace('miles $', '')
                                              .replace('• ', '')
                                              .replace(' w/', ''), vehicleList))
            return vehicleList
        except:
            print("Error in getting bs obj, retrying...")


# get the number of pages to iterate through
def get_num_pages(url):
    while 1:
        try:
            # make bs obj from url
            bs = get_beautifulsoup_obj(url)
            dom = etree.HTML(str(bs))
            pages = str(dom.xpath('// *[ @ id = "pagination"] / li[2] / span')[0].text)
            pages = pages[-4:]
            # print(pages + " to go through")
            return int(pages)
        except:
            print("Error in getting number of pages, retrying...")


def scrape(page, num_pages):
    from datetime import date

    vehicleList = []
    dict_list = []
    date = str(date.today())

    while page <= num_pages:
        url = "https://www.carvana.com/cars?page=" + str(page)
        print(url)

        vehiclespg = get_vehicle_details(url)
        vehicleList = vehicleList + vehiclespg

        # print_list(vehicleList)
        print_list(vehiclespg)
        print("----------" + str(page) + "/" + str(num_pages) + "---------\n")
        page += 1

    for e in vehicleList:
        year = e.split()[0]
        make = e.split()[1]
        mileage = e.split()[-2]
        price = e.split()[-1]
        model = re.search(make + " " + '(.*)' + " " + mileage, e)
        model = str(model.group(1))

        #add attributes to a dictionary
        dictionary = {"Year: ": year,
                      "Make: ": make,
                      "Model: ": model,
                      "Price: ": price,
                      "Mileage: ": mileage,
                      "Date: ": date}

        # list of dictionaries
        dict_list.append(dictionary)

    # save dictionary list to json file
    with open(date + ' carvana_data.json', 'w') as fp:
        json.dump(dict_list, fp, indent=4, separators=(',', ': '))

    # read json file and convert to csv file
    df = pd.read_json(date + ' carvana_data.json')
    df.to_csv(date + ' ' + str(page) + ' carvana_data.csv')

    # when finished the data is saved to a csv
    print("Done! Saving file as " + date + " carvana_data")
    print("Last page was: " + str(page))


if __name__ == '__main__':
    # get total num of pages from Carvana webpage
    totalpgs = get_num_pages("https://www.carvana.com/cars?page=1")
    start = 1
    # get number of available cores
    cores = int(mp.cpu_count())
    print(str(cores) + " cores detected")
    # divide up workload amongst available cores
    difference = totalpgs//cores
    finish = difference

    print("Total pages to scrape: " + str(totalpgs))
    print("Starting Processes...")

    proclist = []

    # initialize process for each core
    for num in range(0,cores):
        num = mp.Process(target=scrape, args=(start, finish))
        proclist.append(num)
        print("starting process " + str(num) + ": " + str(start) + "-" + str(finish))
        start = finish + 1
        finish = finish + difference

    # start processes
    print(proclist)
    for i in proclist:
        i.start()

    # wait for processes to complete
    for i in proclist:
        i.join()


    # Processes finished
    print("All Processes Completed!")

