#Make all module items: external link open in new tab
def openLinksInNewTabs():
    modules = API.getAllModules()
    import requests
    for module in modules:
        moduleItems = API.getModuleItems(module['id'])
        for moduleItem in moduleItems:
            if moduleItem['type'] == 'ExternalUrl':
                requests.put('https://canvas.instructure.com/api/v1/courses/{}/modules/{}/items/{}'.format(Init.Course_ID,module['id'],moduleItem['id']), params = {'access_token': Init.Access_Token, 'module_item[new_tab]': True})
                print(moduleItem['title'])