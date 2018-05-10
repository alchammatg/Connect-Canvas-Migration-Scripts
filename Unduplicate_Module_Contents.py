import API_Calls as API

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
