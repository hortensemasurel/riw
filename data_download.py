from zipfile import ZipFile
from os import rename, remove
from requests import get
from requests.exceptions import ConnectionError
from time import time, sleep
from tqdm import tqdm
import datetime

url_cs276 = "http://web.stanford.edu/class/cs276/pa/pa1-data.zip"

### Downloading the corpus
print("CS276 starts downloading...")

while "corpus_request" not in globals():
    #import the corpus of documents with the url
    corpus_request = get(url_cs276, stream=True)

    #we implement a loading bar
    bar_size = int(corpus_request.headers.get("content-length", 0))
    chunk_size = 1024
    bar = tqdm(total=bar_size, unit="iB", unit_scale=True)

    #reading data
    with open("cs276.zip", "wb") as f:
        for data in corpus_request.iter_content(chunk_size):
            bar.update(len(data))
            f.write(data)
    bar.close()
print("Corpus CS276 was successfully downloaded!")

### Extracting the files one by one
with ZipFile("cs276.zip", "r") as zip_file:
    print("Reading all the files...")
    for file in zip_file.namelist():
        zip_file.extract(member=file, path="data/")
    print("All files were correctly extracted !")

#Removing the zip file, we won't need it anymore
remove("cs276.zip")

#Renaming the data directory
rename(r"data/pa1-data", r"data/cs276")
