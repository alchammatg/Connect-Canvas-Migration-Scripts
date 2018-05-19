import API_Calls as API
import urllib.request as req
from bs4 import BeautifulSoup
import Init

pageUrlHtmlList = []
processed_item_count = 0
total_item_count = 0

#to be used in log
processed_item_count = 0
total_item_count = 0
recreated_modules = []
created_pages = []


def deleteAllHTMLFiles():
    all_html_files = API.getAllFiles('text/html')

    deleted_file_count =0
    for file in all_html_files:
        API.deleteFile(file['id'])
        deleted_file_count += 1
    print("[deleteAllHTMLFiles] {} files were deleted".format(deleted_file_count))
    return


class pageUrlHtml(object):
    def __init__(self, url, html):
        self.url = url
        self.html = html
    def __repr__(self):
        return str(self.__dict__)


def getHtmlBody(file_url):
    # download file contents into html_content string
    response = req.urlopen(file_url)
    html_raw = response.read()
    response.close()

    soup = BeautifulSoup(html_raw, "html.parser")
    head = soup.find('head')
    if head:
        head.extract()
    body = str(soup)
    return body


def createReversionedModule(module_name, module_position, module_items):
    new_module = API.createModule(module_name, module_position)
    API.publishModule(new_module['id'])
    recreated_modules.append(new_module['name'])

    for item in module_items:
        #create next module item in list
        created_module_item = API.createModuleItem(new_module['id'], item)
        #publish item according to whether it was published in the original module or of it is a subheader
        if (item['published'] == True) or (item['type'] == 'SubHeader'):
            API.publishModuleItem(new_module['id'], created_module_item['id'])
    return


def reversionModule(module_ID):
    # For every html file found in a module, creates a wiki page version of the file. If a module contains one or more html files, creates a new version of that module with wiki pages in place of the old html files and deletes the original module. The recreation was necessary as the previous method of item replacement caused positioning errors, especially around subHeader items.

    old_module = API.getModule(module_ID)
    old_module_name = old_module['name']
    module_items = API.getModuleItems(old_module['id'])

    global processed_item_count
    #content id: The id of the content to link to the module item. Required, except for 'ExternalUrl', 'Page', and 'SubHeader' types.
    if module_items:
        global created_pages
        #the flag will flip if atleast one html file is found in the module
        new_module_flag = 0
        module_items_count = len(module_items)
        for n in range(module_items_count):
            processed_item_count += 1

            if module_items[n]['type'] == 'File':
                file = API.getFile(module_items[n]['content_id'])
                if (file['content-type'] == 'text/html'):
                    print('Converted HTML File - Title: {}'.format(module_items[n]['title']))
                    page_body = getHtmlBody(file['url'])
                    page = API.createPage(page_title = module_items[n]['title'], page_body = page_body)
                    created_pages.append([page['title'],old_module_name])
                    pageUrlHtmlList.append(pageUrlHtml(page['url'], file['display_name']))
                    page_changes = {'position': module_items[n]['position'],
                                    'indent': module_items[n]['indent'],
                                    'page_url': page['url'],
                                    'type': 'Page',
                                    'published': module_items[n]['published']}
                    page.update(page_changes)

                    module_items[n] = page
                    new_module_flag = 1

        if new_module_flag == 1:
            Init.pageUrlHtmlList = pageUrlHtmlList
            #create new module THEN delete old module
            createReversionedModule(old_module['name'], old_module['position'], module_items)
            API.deleteModule(module_ID)
            print("MODULE {} has been recreated".format(old_module['name']))
        else:
            print('MODULE {} contains no HTML files => No modifications necessary'.format(old_module['name']))
        return


def traverseCourseFTP():
    modules = API.getAllModules()

    for module in modules:
            reversionModule(module['id'])
    return


def MasterFTP():
    traverseCourseFTP()
    deleteAllHTMLFiles()
    return
