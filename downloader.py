import sys
import requests
import os
import time
# for tracking progress
totalWallpapers = None
current = 1
currentPage = 1


# pass in API Key, and the collection you want to download
def main():
    global totalWallpapers
    global currentPage
    username = sys.argv[1]
    apiKey = sys.argv[2]
    collectionID = sys.argv[3]
    # get metadata about collection from API
    collection = getCollection(username, apiKey, collectionID);    

    # set number of wallpapers
    totalWallpapers = collection['meta']['total']

    # Wallhaven paginates collections. I think it's 24 wallpapers / page
    # so 49 wallpapers has 3 pages (also conviently there's a meta.last_page value).
    # So need to refetch the collection 3 times. 
    for currentPage in range(1, collection['meta']['last_page']+1):
        # refetch the collection on the current page
        collection = getCollection(username, apiKey, collectionID, currentPage);    
        # download all the wallpapers in that page
        downloadWallpapers(collection, collectionID)


    print('Finished!')

# Get the list of wallpapers (up to 24, wallhaven paginates 24 at a time)
def getCollection(username, apiKey, collectionID, page=1):
    url = 'https://wallhaven.cc/api/v1/collections/%s/%s' % (username, collectionID)
    response = requests.get(url, {'apikey': apiKey, 'page': page})
    return response.json()

# Main function that loops through the (sub)-collection and downloads each one
# Wallhaven has a 45/min API rate limit, so this will wait 2 seconds (safer side) between downloads
def downloadWallpapers(collection, collectionID):
    global current
    # set the directory and filepath on where to download
    downloadDirectory = os.path.join('downloads/', collectionID, '')
    os.makedirs(os.path.dirname(downloadDirectory), exist_ok=True)

    # main loop, wallhaven paginates a set amount at a time. so exit when current page is done.
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

    # get the response and write to disk
    response = requests.get(url)
    with open(filepath, "wb") as f:
        f.write(response.content)        

if __name__ == "__main__":
    main()


