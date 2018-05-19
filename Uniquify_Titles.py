import Init
import API_Calls as API
import re


def getCoreNames(names, ugly_names):
    canvas_extension = re.compile(r'-[0-9]+')
    plain_ugly_names = []

    for uname in ugly_names:
        plain_ugly_names.append(canvas_extension.split(uname)[0])

    core_names = list(set(plain_ugly_names))
    print(core_names)

    for core_name in core_names:
        if core_name not in names:
            print('No page with the title ({}) was found. Based on this, there are no ugly names with the base: {}'.format(core_name,core_name))
            core_names.remove(core_name)

    return core_names


def MasterUniquifyTitles():
    names = []
    ugly_names = []
    pages = API.getAllPages()

    for page in pages:
        names.append(page['title'])

    potential_reused_title = re.compile(r'.+?-[0-9]+')
    for name in names:
        if potential_reused_title.match(name):
            ugly_names.append(name)

    core_names = getCoreNames(names, ugly_names)
    if core_names!=[]:
        canvas_extension = re.compile(r'-[0-9]+')
        module_identifier = re.compile(r'[^0-9]+[0-9]*')

        modules = API.getAllModules()
        for module in modules:
            module_items = API.getModuleItems(module['id'])
            for module_item in module_items:
                if module_item["type"] == "Page":
                    stripped_title = canvas_extension.split(module_item['title'])[0]
                    if stripped_title in core_names:

                        module_partial_name = module_identifier.findall(module["name"])[0]
                        new_page_title = '{} ({})'.format(stripped_title, module_partial_name)
                        print("({}) used to be ({})".format(new_page_title,module_item['title']))
                        page = API.updatePageTitle(module_item['page_url'], new_page_title)
                        #get page url  and change page title not item title
        print("Finished all modules")

    return
