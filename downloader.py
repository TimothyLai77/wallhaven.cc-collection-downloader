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
    downloadWallpapers(collection, collectionID)

    print('Finished!')
    # print(apiKey)
    # print(collectionID)

# Get the large object that conatins the URLs to the images within a collection
def getCollection(username, apiKey, collectionID):
    url = 'https://wallhaven.cc/api/v1/collections/%s/%s' % (username, collectionID)
    response = requests.get(url, {'apikey': apiKey})
    return response.json()

# Main function that loops through the collection and downloads each one
# Wallhaven has a 45/min API rate limit, so this will wait 2 seconds (safer side) between downloads
def downloadWallpapers(collection, collectionID):
    # create directory 
    downloadDirectory = os.path.join('downloads/', collectionID, '')
    print(downloadDirectory)
    os.makedirs(os.path.dirname(downloadDirectory), exist_ok=True)

    # for tracking status of collection downloaded
    totalWallpapers = collection['meta']['total']
    current = 1

    # main loop
    for wallpaper in collection['data']:
        time.sleep(2)
        print("downloading: %i/%i..." % (current, totalWallpapers))
        download(wallpaper['path'], downloadDirectory)
        current += 1

        


def download(url, downloadDirectory):
    # extract the filename from the URL
    filename = os.path.basename(url)
    # create the filepath to write to 
    filepath = os.path.join(downloadDirectory, filename)


    response = requests.get(url)

    with open(filepath, "wb") as f:
        f.write(response.content)        

if __name__ == "__main__":
    main()


