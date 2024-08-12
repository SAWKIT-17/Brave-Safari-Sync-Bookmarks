import plistlib
import json
import os
import uuid

safari_bookmarks_path = os.path.expanduser('~/Library/Safari/Bookmarks.plist')
brave_bookmarks_path = os.path.expanduser('~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks')

def read_brave_bookmarks(path):
    with open(path, 'r') as f:
        bookmarks = json.load(f)
    return bookmarks

def read_safari_bookmarks(path):
    with open(path, 'rb') as f:
        plist = plistlib.load(f)
    return plist

def write_safari_bookmarks(path, bookmarks):
    with open(path, 'wb') as f:
        plistlib.dump(bookmarks, f)

def convert_brave_to_safari(brave_bookmarks):
    def process_bookmark(bookmark):
        if bookmark['type'] == 'url':
            return {
                'Title': bookmark['name'],
                'URLString': bookmark['url'],
                'WebBookmarkType': 'WebBookmarkTypeLeaf',
                'WebBookmarkUUID': str(uuid.uuid4()),
                'URIDictionary': {
                    'title': bookmark['name']
                }
            }
        elif bookmark['type'] == 'folder':
            safari_folder = {
                'Title': bookmark['name'],
                'WebBookmarkType': 'WebBookmarkTypeList',
                'WebBookmarkUUID': str(uuid.uuid4()),
                'Children': []
            }
            for child in bookmark['children']:
                safari_folder['Children'].append(process_bookmark(child))
            return safari_folder

    safari_bookmarks = []
    for bookmark in brave_bookmarks['roots']['bookmark_bar']['children']:
        safari_bookmarks.append(process_bookmark(bookmark))

    return safari_bookmarks

brave_bookmarks = read_brave_bookmarks(brave_bookmarks_path)
safari_bookmarks = read_safari_bookmarks(safari_bookmarks_path)

converted_bookmarks = convert_brave_to_safari(brave_bookmarks)

os.system('clear')

while True:
    print("Veux-tu effacer tes anciens favoris Safari ? ⌫")
    erase_bookmarks = str(input("Choisis par 'oui' ou par 'non' : ").strip().lower())

    if erase_bookmarks == "oui":
        safari_bookmarks['Children'][1]['Children'] = []
        break
    elif erase_bookmarks == "non":
        break
    else:
        os.system('clear')
        print("Mauvaise réponse, aller c'est pas compliqué.")

safari_bookmarks['Children'][1]['Children'].extend(converted_bookmarks)

write_safari_bookmarks(safari_bookmarks_path, safari_bookmarks)

print("Favoris synchronisés avec succès.")