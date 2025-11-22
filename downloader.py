import sys
import requests
import os
import time

# download path
baseDownloadPath='downloads/'
fullDownloadDirectory=''

# for tracking progress
totalWallpapers = None
current = 1
currentPage = 1

# duplicate checking with sets
existingWallpapers = set()

# pass in API Key, and the collection you want to download
def main():
    global baseDownloadPath
    global fullDownloadDirectory
    global totalWallpapers
    global currentPage
    global existingWallpapers

    username = sys.argv[1]
    apiKey = sys.argv[2]
    collectionID = sys.argv[3]
    
    # create the download path
    fullDownloadDirectory = os.path.join(baseDownloadPath, collectionID, '')
    existingWallpapers = populateSet(existingWallpapers, fullDownloadDirectory)

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


# go into a directory and put all the files into a set for duplicate checking
def populateSet(set, directory):
    set.update(os.listdir(directory))
    return set


# Get the list of wallpapers (up to 24, wallhaven paginates 24 at a time)
def getCollection(username, apiKey, collectionID, page=1):
    # *TECHNICALLY* you can exceed the rate limit if you had > 45 pages of wallpapers and it just skipped 45 pages of them in under a minute. 
    # probably don't need it, but this program is already slow as beans anyways.
    time.sleep(1.35) 
    url = 'https://wallhaven.cc/api/v1/collections/%s/%s' % (username, collectionID)
    response = requests.get(url, {'apikey': apiKey, 'page': page})
    return response.json()

# Main function that loops through the (sub)-collection and downloads each one
# Wallhaven has a 45/min API rate limit, so this will wait 2 seconds (safer side) between downloads
def downloadWallpapers(collection, collectionID):
    global current
    # set the directory and filepath on where to download
    #downloadDirectory = os.path.join('downloads/', collectionID, '')
    os.makedirs(os.path.dirname(fullDownloadDirectory), exist_ok=True)

    # main loop, wallhaven paginates a set amount at a time. so exit when current page is done.
    
    for wallpaper in collection['data']:
        currentFile = os.path.basename(wallpaper['path'])
        if(currentFile not in existingWallpapers):
            time.sleep(1.5)
            print("[%i/%i]: downloading..." % (current, totalWallpapers))
            download(wallpaper['path'], fullDownloadDirectory)
        else:
            print('[%i/%i]: wallpaper %s already exists, skipping...'%(current, totalWallpapers, currentFile))
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


