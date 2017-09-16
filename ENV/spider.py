# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import sys


def print_greeting():
    print("Crawler running....")
    # Replace any spaces in the directory name with underscores
    dir_name = input("Please enter your project name: ").replace(" ", "_")
    num = input("Please enter the number of pages to be searched: ")
    queries = input("Please enter your search terms: ")
    return dir_name,num,queries


def query_google(dir_name,num,params):



    # Create project directory
    if not os.path.exists(dir_name):
        print("Creating directory : " + dir_name + "....")
        os.makedirs(dir_name)
        print("Directory created")
    else:
        print("Directory already exists, proceeding with web scraping...")

    # Create dir to store raw html
    search_dir = dir_name + "/googlehtml"
    if not os.path.exists(search_dir):
        os.makedirs(search_dir)
    else:
        print("Dir for Google search html already exists,proceeding with web scraping...")

    # Query Google
    user_agent = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}

    # Get number of pages to search -> If we want to search by num of results instead of pages
    # results_per_page = 10
    # num = int(num)
    # if(num % results_per_page is 0):
    #     pages = int(num / results_per_page)
    # else:
    #     pages = int(math.ceil(num/10) % results_per_page)
    # print("Number of google pages to search: " + str(pages))

    # NOTE: There are 10 results per page, but not all 10 are URLs.
    # E.g some may be link to gallery of images
    results_per_page = 10
    # Return a set from this function containing the file names of all the pages scraped
    file_names = set()

    for page in range(int(num)):

        cur_page = results_per_page * (page)
        search_term = {"q": params, "start": cur_page}
        # Spoofs a browser visit that times out after 5 sec(no reply within 5 sec)
        url = "https://www.google.com.sg/search"
        r = requests.get(url, headers=user_agent, params=search_term, timeout=5.0)
        print("Searching page " + str(page + 1) + " ....\n")
        # Add page to file_name set
        google_results = r.text.encode("utf-8")
        soup = BeautifulSoup(google_results, "html.parser")
        # To be returned from this function
        file_names.add(soup)
        # Used to store the html files to be saved
        file_name = search_dir + "/googleresultspage" + str(page + 1) + ".html"

        # Write to file
        with open(file_name, "wb") as file:
            file.write(soup.prettify().encode("utf-8"))

    print("Saving results.....\n Results saved.\n\n")
    return file_names


def get_search_links(search_results):

    links = set()
    for result in search_results:
        # For each <h3 class='r'> tag, find the <a> tag and get the href value
        link_set = result.body.find_all("h3", class_="r")

        # Add the href value to a set that will be saved to a file
        for link in link_set:
            print("Extracting link...\n")
            links.add(link.find("a").get("href"))

    with open(dir_name + "/googlelinks.txt","a") as f:
        print(str(len(links)) + " links extracted.")
        print("Saving links...")
        for each in links:
            f.write(each + "\n")
        print("Links saved.")
    return links


def crawl_links(set_of_links):

    # Create results dir
    results_dir = dir_name + "/results"
    if not os.path.exists(results_dir):
        print("Creating directory to store results")
        os.makedirs(results_dir)
        print("Directory created.")
    else:
        print("Directory already exists, continuing with web scraping")

    user_agent = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}

    results_set = set()

    for each in set_of_links:
        print("Crawling through link...")
        r = requests.get(each, headers=user_agent, timeout=10.0)
        html = r.text.encode("utf-8")
        soup = BeautifulSoup(html,"html.parser")
        body = soup.body.encode("utf-8")

        # Get file name(E.g google from https://ww.google.com
        print("Original: " + str(each))
        splitted = each.split(".")
        # E.g http://www.abc.com/example/year/month/day/page.html -> length of 4
        # splitted[-3] => abc
        if(len(splitted) > 3):
            file_name = splitted[-3]
        else:
            # E.g http://abc.com OR http://www.abc.com
            # splitted[-2] => abc
            file_name = splitted[-2]
        if "http" in file_name:
            file_name = file_name.split("//")[1]
        print("Domain Name: " + str(file_name))
        results_set.add((file_name,body))

    # Used to check duplicate file names arising from multiple links from the same domain name
    file_counter = 0

    # Save results to file
    for tup in results_set:

        # Check if name is too long(Indicative of error in getting file name above)
        if len(tup[0]) > 20:
            name = tup[0][:20]
        else:
            name = tup[0]

        # Replaces any / in the name with _ if they exists
        if "/" in name:
            name = name.replace("/", "_")

        # Check if file name already exists(Multiple pages from same site)
        if os.path.exists(results_dir + "/" + name + ".html"):
            file_counter += 1
            save_name = results_dir + "/" + name + str(file_counter) + ".html"

        else:
            file_counter = 0
            save_name = results_dir + "/" + name + ".html"

        print("Saving file: " + name)
        with open(save_name,"w") as f:
            f.write(str(tup[1]))



if __name__ == "__main__":
    dir_name,num,params = print_greeting()
    query_results = query_google(dir_name,num,params)
    search_links = get_search_links(query_results)
    crawl_links(search_links)