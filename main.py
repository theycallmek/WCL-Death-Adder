import os
import sys
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pprint import pprint


# Helper for webdriver path (fixes pyinstaller path issue)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


# Make sure Chrome webdriver doesn't show a window
chrome_options = Options()
# Comment below line to show browser window
chrome_options.add_argument('--headless')
# Prevent useless error messages
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--ignore-ssl-errors')


# Set path to webdriver using helper
service = Service(resource_path('./driver/chromedriver.exe'))
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(5)
final_count = {}


def get_user_input():
    strings = [item for item in text_input.get('1.0', tk.END).split()]
    return strings


def construct_link(url):
    return f'{url}#boss=-2&difficulty=0&type=deaths'


def parse_link(url):
    # Open the webpage and find the table with the data we want
    driver.get(url)
    table = driver.find_element(By.ID, 'actor-deaths-0')

    # Find all the rows in the table (excluding the header row)
    rows = table.find_elements(By.XPATH, './/tbody/tr')

    # Loop through each row and extract the name and total deaths
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        name = cells[0].text.strip()
        total_deaths = cells[2].text.strip()
        if name != '':
            if total_deaths != '':
                if int(total_deaths) > 0:
                    try:
                        final_count[name] = final_count[name] + int(total_deaths)
                    except KeyError:
                        final_count[name] = int(total_deaths)


def scrape_links(links: list):
    print('Scraper Initialized...')
    for link in links:
        built_url = construct_link(link)
        print(f'Scraping: {built_url}')
        print('GUI freezing while scraping is expected behavior. Please wait...')
        parse_link(built_url)
        print('Finished scraping link. Moving on...')


def process_links():
    strings = [item for item in text_input.get('1.0', tk.END).split()]
    scrape_links(strings)
    return final_count


def go_clicked():
    result = process_links()
    sorted_words = sorted(result.items(), key=lambda item: int(item[1]))
    pprint(sorted_words)
    # Close the webdriver
    driver.close()


def about_clicked():
    messagebox.showinfo('About', 'Made By:\n   RoyalT <The Crew>\n   Whitemane-US')


if __name__ == '__main__':

    # Init tkinter
    window = tk.Tk()
    window.title('Name N Shame - Death Adder v0.1')
    window.resizable(width=False, height=False)

    # Create instructions label
    label = tk.Label(text='Enter 1 WarcraftLogs link per line (No spaces or commas). Then see console for results.')
    label.pack(side=tk.TOP, padx=5, pady=5)

    # Create text input field
    text_input = tk.Text(window, height=20, width=60)
    text_input.pack(side=tk.BOTTOM)

    # Create buttons
    button = tk.Button(text='Scrape Links', command=go_clicked)
    button.pack(side=tk.LEFT, padx=5, pady=5)

    button = tk.Button(text='About', command=about_clicked)
    button.pack(side=tk.RIGHT, padx=5, pady=5)

    # Start GUI
    window.mainloop()
