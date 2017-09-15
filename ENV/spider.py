# -*- coding: utf-8 -*-
import re
import requests
import json
from bs4 import BeautifulSoup

def print_greeting():
    print("Crawler running....")
    return input("Please enter your search terms: ")


def query_google(params):
    search_term = {"q" : params}
    user_agent = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}
    google = "https://www.google.com.sg/search"
    # Spoofs a browser visit that times out after 5 sec(no reply within 5 sec)
    r = requests.get(google, headers=user_agent, params=search_term, timeout=5.0)
    print(r.request.url)
    google_results = r.text.encode("utf-8")
    soup = BeautifulSoup(google_results, "html.parser")
    # Write to file
    with open("googleresults.html", "wb") as file:
        file.write(soup.prettify().encode("utf-8"))
    return soup

def get_search_links(search_results):

    for result in search_results.body.find_all("a"):
        print(result.get("href"))




if __name__ == "__main__":
    user_input = print_greeting()
    query_results = query_google(user_input)
    get_search_links(query_results)