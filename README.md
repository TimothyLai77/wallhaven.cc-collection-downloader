# wallhaven.cc-collection-downloader
script to download all wallpapers in original size from wallhaven.cc

# Usage:
run `python3 downloader.py <username> <apikey> <collectionID>`
apikey can be found in your user settings, and the collection ID is some string of numbers in the URL when viewing a collection.

# Todo:
* Make API key optional. Public collections should download without an API key.  
* Probably should check the status of the response in download(), if 200OK then keep going. and anything else try again (up to a limit)