import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime
import os

def scrape_UCPD_data(start_date = "06-01-2015", end_date = None,
                     max_page = None, data_type = "Field Interview"):

    """
    Scraps University of Chicago Police Department's website.
    Takes arguments start_date, end_date, max_page, data_type.

    Arguments:
    start_date: Date in %MM%DD%YYYY format denoting start date for query.
    end_date: Date in %MM%DD%YYYY format denoting end date for query.
    max_page: Integer denoting number of entries desired.
    data_type: String. Options: "Field interview", "Traffic".
    """

    # Initializing date_range
    if end_date == None:
        end_date = datetime.datetime.now().strftime("%m-%d-%Y")

    start_date = start_date.replace("-", "%2F")
    end_date = end_date.replace("-", "%2F")
    date_range = f"startDate={start_date}&endDate={end_date}"

    # Forming search url
    if data_type == "Field Interview": # Find appropriate search type
        ucpd_site = "https://incidentreports.uchicago.edu/fieldInterviewsArchive.php?"
    elif data_type == "Traffic":
        ucpd_site = "https://incidentreports.uchicago.edu/trafficStopsArchive.php?"


    base_url = ucpd_site + date_range

    if max_page == None: # unless specified do maximum query
        page = requests.get(base_url)
        soup = bs(page.text)
        page_counter = soup.find_all('li', {"class": "page-count"})
        max_page = int(page_counter[0].text.split()[-1])

    # Scraping Data
    df_list = []
    for page_num in range(max_page):

        page = requests.get(base_url + f"&offset={page_num*5}")
        soup = bs(page.text)

        # Read in soup as dataframe and add to list
        df_list.append(pd.DataFrame(pd.read_html(str(soup))[0]))

    df = pd.concat(df_list)
    return df

if __name__ == "__main__":
    field_df = scrape_UCPD_data(data_type = "Field Interview")
    traffic_df = scrape_UCPD_data(data_type = "Traffic")

    field_df.to_csv("../data/field_interview_df.csv", index = False)
    traffic_df.to_csv("../data/traffic_df.csv", index = False)
