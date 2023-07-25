import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import PySimpleGUI as sg
from concurrent.futures import ThreadPoolExecutor
import threading
import pyfiglet
import time
import pyfiglet.fonts

# Print "S1mpleDork" in Impact font and green color
text_impact = "S1mpleDork"
font_impact = "slant"
ascii_art_impact = pyfiglet.figlet_format(text_impact, font=font_impact)
print(ascii_art_impact)

# Print "by Browny59" in another font, smaller size, and without any color formatting
text_browny = "by Browny59"
font_browny = "small"
ascii_art_browny = pyfiglet.figlet_format(text_browny, font=font_browny, width=60)
print(ascii_art_browny)
# Function to read dorks from a file
def read_dorks(file_path):
    with open(file_path, 'r') as f:
        dorks = [line.strip() for line in f.readlines()]
    return dorks

# Function to read proxies from a file
def read_proxies(file_path):
    with open(file_path, 'r') as f:
        proxies = [line.strip() for line in f.readlines()]
    return proxies

# Function to search for URLs using dorks and proxies
def search_urls(dorks, use_proxy, proxies, search_pages, threads_per_search):
    search_engine_urls = [
        'https://www.google.com/search?q=',
        'https://www.bing.com/search?q=',
        'https://search.yahoo.com/search?p=',
        'https://duckduckgo.com/?q=',
        'https://www.ask.com/web?q=',
        'https://search.aol.com/aol/search?q=',
        'http://www.dogpile.com/search/web?q=',
        'https://yandex.com/search/?text=',
        'https://www.qwant.com/?q=',
    ]

    found_urls = []

    def search_dork(dork, url, thread_num):
        full_url = url + dork
        try:
            if use_proxy:
                for proxy in proxies:
                    response = requests.get(full_url, proxies={'http': proxy, 'https': proxy})
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        results = soup.find_all('a')
                        for result in results:
                            href = result.get('href')
                            if href and href.startswith('http'):
                                found_urls.append(href)
            else:
                response = requests.get(full_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    results = soup.find_all('a')
                    for result in results:
                        href = result.get('href')
                        if href and href.startswith('http'):
                            found_urls.append(href)
        except Exception as e:
            print(f"Error while searching {full_url}: {e}")

    with ThreadPoolExecutor(max_workers=threads_per_search) as executor:
        for dork in dorks:
            for url in search_engine_urls:
                for page in range(1, search_pages + 1):
                    full_url = f"{url}{dork}&start={10 * (page - 1)}"
                    executor.submit(search_dork, dork, full_url, threading.current_thread().name)

    return found_urls

# Function to export URLs to a file
def export_urls(urls):
    with open('urls.txt', 'w') as f:
        for url in urls:
            f.write(url + '\n')

if __name__ == '__main__':
    # Prompt user for dork file path
    dork_file_path = sg.popup_get_file('Select Dork File', file_types=(("Text Files", "*.txt"),))
    if not dork_file_path:
        sg.popup_error("Please select a valid dork file!")
        exit()

    # Prompt user for proxy file path
    proxy_file_path = sg.popup_get_file('Select Proxy File', file_types=(("Text Files", "*.txt"),))
    if not proxy_file_path:
        sg.popup_error("Please select a valid proxy file!")
        exit()

    # Prompt user for number of search result pages per dork
    search_pages = int(sg.popup_get_text("Enter the number of search result pages per dork:", default_text="1"))

    # Prompt user for number of threads per search
    threads_per_search = int(sg.popup_get_text("Enter the number of threads per search:", default_text="1"))

    dorks = read_dorks(dork_file_path)
    proxies = read_proxies(proxy_file_path)

    urls = search_urls(dorks, use_proxy=True, proxies=proxies, search_pages=search_pages, threads_per_search=threads_per_search)

    # Add ASCII progress bar
    total_dorks = len(dorks)
    for dork_index, dork in enumerate(dorks, start=1):
        print(f"Searching for vulnerable URLs for dork {dork_index}/{total_dorks}:")
        progress_bar = tqdm(total=search_pages, desc="Progress", ascii=True, bar_format="{desc}: {percentage:.0f}%|{bar}| {n_fmt}/{total_fmt} pages")
        for _ in range(search_pages):
            # Simulate searching process
            time.sleep(0.1)
            progress_bar.update(1)
        progress_bar.close()

    export_urls(urls)

    print("URLs saved in urls.txt")
