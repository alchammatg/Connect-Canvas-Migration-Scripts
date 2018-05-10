import API_Calls as API
import Init


def modulate(items, start_position, module_position):
    title_index = int(start_position)
    module_name = items[title_index]['title']
    module = API.createModule(module_name, module_position)
    API.publishModule(module['id'])
    print('Created New Module - ({})'.format(module_name))
    new_position = 1
    for item in items[title_index+1:]:
        if (item['type'] == 'SubHeader') & (item['indent'] == 0):
            break
        else:
            indent = item['indent']
            if indent!=0:
                indent = indent-1
            API.moveModuleItem(item['module_id'],item['id'],module['id'],indent, new_position)
            new_position+=1
            print('Moved Module Item - ({})'.format(item['title']))


def MasterModulateBysub(parent_module):
    print('{} is now being modulated by subHeader positions'.format(parent_module['name']))

    module_position_variable = int(parent_module['position']) + 1

    parent_module_items = API.getModuleItems(parent_module['id'])
    if parent_module_items == []:
        print("No items were found in the specified module - Process terminated")
        return
    else:
        for item in parent_module_items:
            if (item['type'] == 'SubHeader') & (item['indent'] == 0):
                modulate(parent_module_items, parent_module_items.index(item), module_position_variable)
                module_position_variable += 1
        API.deleteModule(parent_module['id'])
    return


def MasterModulateIndiscriminate(parent_module):
    print('{} is now being modulated indiscriminately'.format(parent_module['name']))

    module_items = API.getModuleItems(parent_module['id'])
    #In this for loop, create a new module for each module item and move the item to its new module. Publish each module after populating it
    for module_item in module_items:
        new_module = API.createModule(module_item['title'], module_item['position'])
        API.moveModuleItem(parent_module['id'], module_item['id'], new_module['id'], 0, 1)
        API.publishModule(new_module['id'])
        print("({}) now sits in is own module".format(module_item['title']))

    API.deleteModule(parent_module['id'])
    print("Deleted Parent Module: ({})".format(parent_module['name']))

    return


def MasterModulate():
    found_parent_module = False
    modules = API.getAllModules()
    if modules == []:
        print("This course does not contain any modules. The function will now exit.")
        return

    while (True):
        parent_module_name = input("If you would like to break up a module, enter its name here. To skip this function, enter 'NONE':")
        if parent_module_name.upper() == "NONE":
            print('You chose not to break up any modules by entering NONE.')
            return
        else:
            found = False
            for module in modules:
                if module['name'] == parent_module_name:
                    parent_module = module
                    found = True
                    break
            if not found:
                print("A module with the specified name could not be found. Please try again. If the issue persists, enter 'NONE' to skip the function.")

    #If the code reaches here, it means the target module has successfuly be found, and it is time to choose the method of modulation
    #This loop will only exit if a valid input is entered. 1, 2, or 3
    while(True):
        modulate_type = input("How would you like to break up the module? (Select 1, 2, or 3):\n1. Create a new Module for each item (indiscriminate)\n2. Create a module for each 0-indent subHeader found\n3. Nevermind, I don't want to break up the module\n")
        if modulate_type in ['1','2','3']:
            break
        else:
            print("ERROR - {} is an invalid input. Try again.".format(modulate_type))

    if modulate_type == '1':
        MasterModulateIndiscriminate(parent_module)
    elif modulate_type == '2':
        MasterModulateBysub(parent_module)
    #if modulate_type == 3, just use the default return statement to exit the function.
    return