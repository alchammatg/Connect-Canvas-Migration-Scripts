import API_Calls as API
import Init

def restorePage(page_title, page_url):
    #version #1 is always the first version of a page, hence the constant argument 1
    API.revertToPageRevision(page_url,1)
    print('[restorePage] Restored - {}'.format(page_title))
    return


def MasterRAP():
    Init.q.put(["task_description","Restoring Pages"])

    pages = API.getAllPages()
    Init.q.put(["total",len(pages)])

    processed_item_count = 0
    for page in pages:
        processed_item_count += 1
        Init.q.put(["current",processed_item_count])
        restorePage(page['title'], page['url'])
    Init.q.put(["finished",True])
    return