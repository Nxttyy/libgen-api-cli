import urllib.request

import requests
from bs4 import BeautifulSoup
from libgen_api import LibgenSearch

import os
import time
import threading

from tqdm import tqdm


def inp_to_int(inp):
    try:
        i = int(inp)
    except:
        i = 0
    return i


s = LibgenSearch()
results = []
my_dir = os.path.dirname(os.path.realpath(__file__))


def progress_bar(file_size, file_name):
    downloading = True
    downloaded_size = 0
    file_size_mb = int(file_size.split(" ")[0])
    
    with tqdm(total=file_size_mb, unit='MB', desc=file_name) as pbar:
        while downloading:
            time.sleep(0.5)
            try:
                downloaded_size = os.path.getsize(os.path.join(my_dir, 'Downloads', file_name)) / 1_000_000
            except FileNotFoundError:
                pass

            pbar.update(downloaded_size - pbar.n)
            
            if file_size_mb - downloaded_size <= 0.1:
                print("End", file_size_mb)
                downloading = False


        


search_choice = inp_to_int(
    input("Enter 1 for search by author,any number for search by title.\n")
)

try:
    if search_choice == 1:
        author = input("Who is the author?")
        results = s.search_author(author)
    else:
        title = input("What is the book titled?")
        results = s.search_title(title)
except Exception:
    print("[ERROR] query too short!")
    
    
def main():

    for result in results:
        author = result["Author"]
        title = result["Title"]
        size = result["Size"]
        extention = result["Extension"]
        # publisher = result["Publisher"]
        # mirrors = [result["Mirror_1"], result["Mirror_2"]]
        print(
            f"[*]{results.index(result)}.{title}\nBy:{author}\nSize:{size}\nFiletype:({extention}\n)"
        )

    if (results):
        try:
            book = results[inp_to_int(input("Select the book for download."))]
        except IndexError:
            print(f"[ERROR] your choice is valid!")
            return None

        response = requests.get(book["Mirror_1"])

        # BeautifulSoup gets the download link
        soup = BeautifulSoup(response.content, "html.parser")

        div = soup.find("div", id="download")
        download_link = div.h2.a.get("href")

        file_name = book["Title"] + "." + book["Extension"]

        print("[DOWNLOADING] Requisting book, please wait.....")

        def download_book():
            urllib.request.urlretrieve(download_link, "./Downloads/" + file_name)
                
        t1 = threading.Thread(target=download_book)
        t2 = threading.Thread(target=progress_bar, args=(book["Size"], file_name))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print(f"[DONE] {book['Title']} Saved!")
        
    else:
        print(f"[DONE] no books matched your query!")
        return None


if __name__ =="__main__":
    main()