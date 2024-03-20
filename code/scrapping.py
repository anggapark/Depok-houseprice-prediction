#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 21:32:06 2024

@author: anggapark
"""

import datetime
import time
from tqdm import tqdm

import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

links = []
page_url = []
parent_url = []

# list of house characteristic
price = []
categories = []
subcategories = []
bedrooms = []
bathrooms = []
building_size = []
land_size = []
num_floors = []
furnished = []
geo_point = []

icons = ["page_url", "location", "ac_unit", "balcony", "yard", "security", "pool"]
facility_dict = {key: [] for key in icons}


def get_subdristric_link(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # get sublinks for each sub-district in Depok
    click_expand = driver.find_element(
        By.XPATH, '//*[@id="js-crosslinkTopFilter"][@data-has-sublink=""]/a'
    ).click()
    sublinks_by_loc = driver.find_elements(
        By.XPATH, '//*[@id="js-crosslinkTopFilter"]/div/div/a'
    )

    for tag in tqdm(sublinks_by_loc):
        links.append(tag.get_attribute("href"))
        # time.sleep(1 + np.random.normal(loc=0.0,scale=0.627))

    driver.quit()


def get_house_characteristic():
    # get house characteristic
    # https://github.com/yusufprasetyo25/lamudi-house-price-yusuf/blob/main/scrape_lamudi.ipynb
    for link in tqdm(links):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(link)

        page_end = 1  # total pages
        page_iter = 1  # current page

        while page_iter <= page_end:
            info = driver.find_elements(
                By.CSS_SELECTOR, ".ListingCell-AllInfo.ListingUnit"
            )
            info_a = driver.find_elements(By.CSS_SELECTOR, ".js-listing-link")

            try:
                page_end = int(
                    driver.find_element(
                        By.CSS_SELECTOR, "*[data-pagination-end]:last-child"
                    ).get_attribute("data-pagination-end")
                )
            except:
                pass

            for i in range(len(info)):
                price.append(info[i].get_attribute("data-price"))
                categories.append(info[i].get_attribute("data-category"))
                subcategories.append(info[i].get_attribute("data-subcategories"))
                bedrooms.append(info[i].get_attribute("data-bedrooms"))
                bathrooms.append(info[i].get_attribute("data-bathrooms"))
                land_size.append(info[i].get_attribute("data-land_size"))
                furnished.append(info[i].get_attribute("data-furnished"))
                building_size.append(info[i].get_attribute("data-building_size"))
                geo_point.append(info[i].get_attribute("data-geo-point"))

                try:
                    num_floors.append(info[i].get_attribute("data-floors_total"))
                except AttributeError:
                    num_floors.append("")

                parent_url.append(link)
                page_url.append(info_a[i * 2].get_attribute("href"))

            page_iter += 1

            if page_end >= page_iter:
                # click_expand = driver.find_element(By.XPATH, '//*[@class="next "]/a').click()
                click_expand = driver.find_element(
                    By.CSS_SELECTOR, 'link[rel="next"]'
                ).get_attribute("href")
                driver.get(click_expand)
                # click_next_page = driver.find_element(By.CSS_SELECTOR, "body > div.row.fullWidth.ClpBody > div.small-9.columns.js-listingContainer > div.clp-wrapper > div:nth-child(2) > div.BaseSection.Pagination > div > div:nth-child(3) > div > a").click()
                time.sleep(3 + np.random.normal(loc=0.0, scale=0.627))

        driver.quit()


def get_inside_page(icons, facility_dict):

    # Iterate through URLs with progress bar
    # for url in tqdm(df['page_url'][4000:5000]):
    for url in tqdm(df["page_url"][5000:]):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        try:
            driver.get(url)
            facility_dict["page_url"].append(url)

            # Wait for the "Fasilitas" section to be visible
            wait = WebDriverWait(driver, 10)
            fasilitas_section = wait.until(
                EC.presence_of_element_located((By.ID, "listing-amenities"))
            )

            # Get all amenities within the section
            amenities = fasilitas_section.find_elements(
                By.CSS_SELECTOR, ".listing-amenities-list-item"
            )

            # Initialize presence of icons for the current URL
            current_presence = {key: False for key in icons if key != "page_url"}

            # Loop through each amenity and update the presence of icons
            for amenity in amenities:
                facility_name = amenity.find_element(
                    By.CSS_SELECTOR, ".material-icons.material-icons-outlined"
                ).text

                if facility_name in icons:
                    current_presence[facility_name] = True

            # Update facility_dict based on the presence of icons for the current URL
            for icon, presence in current_presence.items():
                facility_dict[icon].append("yes" if presence else "")

        except TimeoutException:
            # print(f"Error encountered for URL: {url}")
            for key in icons:
                if key != "page_url":
                    facility_dict[key].append("")

        # try:
        #     wait = WebDriverWait(driver, 10)
        #     # get_loc = driver.find_element(By.CSS_SELECTOR, '.Title-pdp-address').text
        #     get_loc = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".Title-pdp-address"))).text
        #     facility_dict['location'].append(get_loc)
        # except NoSuchElementException:
        #     facility_dict['location'].append('')

        time.sleep(3.05 + np.random.normal(loc=0.0, scale=0.627))
        driver.quit()

    return facility_dict


if __name__ == "__main__":
    get_subdristric_link(url="https://www.lamudi.co.id/depok/house/buy/")
    get_house_characteristic()
    facility_dict = get_inside_page(icons, facility_dict)

    df = pd.DataFrame(
        data={
            "price": price,
            "categories": categories,
            "subcategories": subcategories,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "building_size": building_size,
            "land_size": land_size,
            "num_floors": num_floors,
            "furnished": furnished,
            "geo_point": geo_point,
            "page_url": page_url,
            "parent_url": parent_url,
        }
    )

    df_facility = pd.DataFrame(facility_dict)

    all_df = pd.merge(left=df, right=df_facility, how="inner", on="page_url")

    df.to_parquet(
        f"depok_houseprice_merge{datetime.date.today().isoformat()}.parquet",
        index=False,
    )
