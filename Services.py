#Make all module items: external link open in new tab
def MasterOpenLinksInNewTabs():
    modules = API.getAllModules()
    import requests
    for module in modules:
        moduleItems = API.getModuleItems(module['id'])
        for moduleItem in moduleItems:
            if moduleItem['type'] == 'ExternalUrl':
                requests.put('https://canvas.instructure.com/api/v1/courses/{}/modules/{}/items/{}'.format(Init.Course_ID,module['id'],moduleItem['id']), params = {'access_token': Init.Access_Token, 'module_item[new_tab]': True})
                print(moduleItem['title'])
                
def MasterDeleteUnpublishedPages():
    unpublished_pages = API.getAllUnpublishedPages()
    for unpublished_page in unpublished_pages:
        print(unpublished_page['title'])
        API.deletePage(unpublished_page['url'])
        
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

def unduplicateModuleContents(moduleID):
    module_items = API.getModuleItems(moduleID)
    checked_items = []
    for module_item in module_items:
        data_pair = (module_item['title'], module_item['type'])
        if data_pair not in checked_items:
            checked_items.append(data_pair)
        else:
            print("----Repeated item detected: [{}]".format(data_pair))
            API.deleteModuleItem(moduleID, module_item['id'])


def MasterUMC():
    modules = API.getAllModules()
    for module in modules:
        print("Processing Module: ({})".format(module['name']))
        unduplicateModuleContents(module['id'])
