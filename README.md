# wallhaven.cc-collection-downloader
script to download all wallpapers in original size from wallhaven.cc

# Usage:
run `python3 downloader.py <username> <apikey> <collectionID>`
apikey can be found in your user settings, and the collection ID is some string of numbers in the URL when viewing a collection.

# Todo:
* Probably some way to only download the difference in the wallhaven collection and disk. 
    * as long as I don't touch the filenames when downloaded to disk, i should be able to compare the IDs to what's on disk. 
        * compare the collection ID to the downloads folder, get all the filenames parse out the ID and put into a set. 
        * and before each download() call check the path that it's about the download and extract the ID from the basename and see if it exists in set.
        * probably need to figure out when to sleep so i don't anger the rate limit.