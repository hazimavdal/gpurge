# GPurge

This is a utility that converts Google Documents, Sheets, etc. to physical files. `gpurge` can search in a local folder (typically a fully-synced Google Drive folder) recursively and convert all `.godc` and `gsheet` files to `.docx` and `xlsx`, respectively.

## Usage

Run `./gpurge.py -h`.

## Google Docs are great, why convert to MS Word?

Here are some scenarios that make sense to do this:

- You want to archive your files and guarantee that you have access to their _content_ 20 years from now. Google [killed](https://en.wikipedia.org/wiki/List_of_Google_products) a great many products in the past, and it is not unlikely that they will discontinue Google Docs at some point in the future.   

- Be able to perform bulk operations on these documents locally, such as searching.

- You need to port your files to another system. How many applications out there can process `.gdoc` files, other than Google Docs? 
