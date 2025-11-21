import sys
import requests
import os
import time
# pass in API Key, and the collection you want to download
def main():
    username = sys.argv[1]
    apiKey = sys.argv[2]
    collectionID = sys.argv[3]
    collection = getCollection(username, apiKey, collectionID);    
    downloadWallpapers(collection)

    print('Finished!')
    # print(apiKey)
    # print(collectionID)

# Get the large object that conatins the URLs to the images within a collection
def getCollection(username, apiKey, collectionID):
    url = 'https://wallhaven.cc/api/v1/collections/%s/%s' % (username, collectionID)
    response = requests.get(url, {'apikey': apiKey})
    return response.json()

def downloadWallpapers(collection):
    totalWallpapers = collection['meta']['total']
    current = 1
    for wallpaper in collection['data']:
        time.sleep(2)
        print("downloading: %i/%i..." % (current, totalWallpapers))
        download(wallpaper['path'])
        current += 1

        


def download(url):
    downloadDirectory = 'downloads/'
    # create the download directory if it doesn't exist
    os.makedirs(os.path.dirname(downloadDirectory), exist_ok=True)
    # extract the filename from the URL
    filename = os.path.basename(url)
    # create the filepath to write to 
    filepath = os.path.join(downloadDirectory, filename)


    response = requests.get(url)

    with open(filepath, "wb") as f:
        f.write(response.content)        

if __name__ == "__main__":
    main()


