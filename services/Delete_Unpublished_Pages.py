import API_Calls as API

def deleteUnpublishedPages():
    unpublished_pages = API.getAllUnpublishedPages()
    for unpublished_page in unpublished_pages:
        print(unpublished_page['title'])
        API.deletePage(unpublished_page['url'])