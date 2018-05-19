import API_Calls as API
import Init
from bs4 import BeautifulSoup
import re

#This is a global flag used in all functions to signal change! For every new page, the flag is reset to 0 by the runCleaningSequence function
changes_flag = 0
#Dictionary that logs changes made to a page inside each function in preperation for printing and logging to overall clean_pages_log in printAndLog function
page_log = {}
#After a page is updated, it's page_log information is passed to this array in the printAndLog function
clean_pages_log = ['*********************', '*CLEAN PAGES RESULTS*', '*********************']

#Failed encodings replacemenet **UNLOGGED**
def encodingReplacements(body):
    newBody = body.replace('Ã©','é').replace('Ã','É').replace('â',"'").replace('Ã®','î').replace('Ã¨','è').replace('Ã ','à').replace('Ã§','ç').replace('Ãª','ê').replace('â','–')
    return newBody

#Remove empty lines from top and bottom of html files.. references an array of empty_line elements created and updated by me as I discover new empty line elements
def stripBborderSpace(input_string):
    # initialize globals. changes_flag flips if atleast one change is made, page_log is a dictionary that stores messages from each function.
    global changes_flag
    global page_log

    #Different types of empty lines I have encountered in Canvas html bodies
    border_blacklist = ['<br/>', '<p></p>', '<div></div>', '<h1></h1>', '<h2></h2>', '<h3></h3>', '<p><a></a></p>',
                        '<p><br/><br/></p>', '<p><br/></p>']

    #These two lists will be filled with the border elements stripped from the edges of the html body
    from_top = []
    from_bot = []

    soup = BeautifulSoup(input_string, 'html.parser')
    if soup:
        #recursively strip the first element from soup if it indicates empty space until first non-match is found
        while(True):
            try:
                #soup.find() returns the first element
                first_element = soup.find()
                #get rid of non-breaking backspace python representation. no need to decode/encode
                first_element_join = ''.join(str(first_element).split())
            except:
                break
            if (first_element_join in border_blacklist):
                from_top.append(str(first_element))
                first_element.extract()
                if changes_flag != 1:
                    changes_flag = 1
            else:
                break
        #recursively strip the last element from soup if it indicates empty space until first non-match is found
        while(True):
            try:
                #soup.find_all returns a list all elements. The index -1 returns the last element in the list.
                last_element = soup.find_all()[-1]
                # get rid of non-breaking backspace python representation. no need to decode/encode
                last_element_join = ''.join(str(last_element).split())
            except:
                break
            if (last_element_join in border_blacklist):
                from_bot.append(str(last_element))
                last_element.extract()
                if changes_flag != 1:
                    changes_flag = 1
            else:
                break

    #If any changes were made, add the results of this function call to the page_log and convert soup to a string to be returned
    if (from_top != []) or (from_bot != []):
        result_string = ["{} empty line(s) removed from top of html body.".format(len(from_top)), "{} empty line(s) removed from bottom of html body.".format(len(from_bot))]
        page_log['stripBborderSpace'] = result_string
        body = str(soup)
    else:
        #if no changes were made, return the original page body which is in the input_string parameter
        body = input_string

    return body


#Remove certain symbols and characters from html body
def removeHieroglyphs(input_string):
    #initialize globals. changes_flag flips if atleast one change is made, page_log is a dictionary that stores messages from each function.
    global changes_flag
    global page_log

    #If any of the elements in undesirable_elemens is found, it will be removed from the body and appended to found_undesirable_elements
    undesirable_elements = ['Â','/*&lt;![CDATA[*/','/*]]&gt;*/']
    found_undesirable_elements = []

    #Execute as per the description of the two arrays above
    output_string = input_string
    for undesirable_element in undesirable_elements:
        if undesirable_element in output_string:
            output_string = output_string.replace(undesirable_element,'')
            found_undesirable_elements.append(undesirable_element)
            if changes_flag != 1:
                changes_flag = 1

    #If any changes were made, add the results of this function call to the page_log
    if found_undesirable_elements != []:
        result_string = ["The following undesirable elements were stripped:", str(found_undesirable_elements)]
        page_log['removeHieroglyphs'] = result_string

    return output_string


#This function addressed the images created in the faculty of education to act as headers. It replaces the images by their alt text. This function is based on the conventions that were used by the faculty of education, and may not have any use outisde this faculty.
def textifyHeaders(input_string):
    # initialize globals. changes_flag flips if atleast one change is made, page_log is a dictionary that stores messages from each function.
    global changes_flag
    global page_log

    #This array will be populated with the alt text of all converted headers. It will remain empty if no conversions occur.
    textified_headers = []

    #Parse the input string (page html body) as a BeautifulSoup object
    soup = BeautifulSoup(input_string,'html.parser')
    #Find all <img> tags in the html body
    imageTags = soup.find_all('img',src=True, alt=True)
    if imageTags:
        for img in imageTags:
            #If either of the following key strings is detected in an img source, replace the image with its alt text
            if ("https://connect.ubc.ca/bbcswebdav/xid" in img['src']) or ("Course_Templates/icons" in img['src']):
                #Only continue if the image has any alt text
                if img['alt']:
                    img.replaceWith(BeautifulSoup('<h2>'+img['alt']+'</h2>', 'html.parser'))
                    textified_headers.append(img['alt'])
                    if changes_flag != 1:
                        changes_flag = 1

    #If the textified_headers array indicates that at least one header was converted, add the results to page_log dictionary and convert the soup to a string to be returned
    if textified_headers != []:
        result_string = ["Headers with the following alt text(s) were converted:", str(textified_headers)]
        page_log['textifyHeaders'] = result_string
        body = str(soup)
    else:
        #if no headers were converted by this call, setup the input string to be returned by the function instead of soup
        body = input_string

    return body


#Turn certain divs used often in Faculty of Education to corresponding headings for better styiling and spacing
def divs2Heads(input_string):
    # initialize globals. changes_flag flips if atleast one change is made, page_log is a dictionary that stores messages from each function.
    global changes_flag
    global page_log

    # This array will be populated with the replacemenet headings
    replacement_headings = []
    #Parse the page's html body into a BeautifulSoup object
    soup = BeautifulSoup(input_string,'html.parser')
    #Find all div elements in the soup that have an id and class in their description
    divs = soup.find_all('div',id=True, class_= True)
    #Check if divs is not NONE. find_all returns NONE if no instances are found
    if divs:
        for div in divs:
            if div['id'] == "imgheading":
                heading_text = str(div.text).strip()
                heading = BeautifulSoup("<h2>{}</h2>".format(heading_text), "html.parser")
                div.replaceWith(heading)
                replacement_headings.append(str(heading))
                if changes_flag != 1:
                    changes_flag = 1

    #If any changes were made, add the results of this function call to the page_log
    if replacement_headings != []:
        result_string = ["The following headings were used to replace header-divs in the page:", str(replacement_headings)]
        page_log['divs2Heads'] = result_string
        body = str(soup)
    else:
        #If no changes were made to soup, return the original string isntead of converting soup unnecessarily
        body = input_string

    return body


#The faculty of education has setup certain page elements with repeated ids, names, classes, or sources. I used this repetition to automate the deletion of these elements from html body.
def stripRepeatedElements(input_string):
    # initialize globals. changes_flag flips if atleast one change is made, page_log is a dictionary that stores messages from each function.
    global changes_flag
    global page_log

    extracted_elements = []

    #BeautifulSoup Portion********************************************************************
    #Parse the input string (page html body) as a BeautifulSoup object
    soup = BeautifulSoup(input_string,'html.parser')
    #These are parameters to pass to the BeautifulSoup find_all function to return the repeated elements we want to remove from all html bodies passed to this function
    soup_element_parameters_list = [('div', {"id":"footer"}), ('a', {"name":"top"}), ('div', {"class":"print"}), ('a', {"href": "#top"})]

    for element_parameters in soup_element_parameters_list:
        #*element_parameters represents the contents of each touple in the soup_element_parameters_list
        found_elements = soup.find_all(*element_parameters)
        if found_elements:
            #Signal this globally through the changes_flag
            if changes_flag != 1:
                changes_flag = 1
            for found_element in found_elements:
                found_element.extract()
                extracted_elements.append(str(found_element))

    #If any of the BeautifulSoup repeated elements were extracted, convert the soup back to a string. Else, use the input_string  forward
    if extracted_elements != []:
        body = str(soup)
    else:
        body = input_string

    #Regex Portion****************************************************************************
    page_number_regex = re.compile(r'\| Page .*? of .*?', re.I | re.M)
    page_number_matches = page_number_regex.findall(body)
    if page_number_matches != []:
        body = page_number_regex.sub('', body)
        extracted_elements.append(str(page_number_matches))
        if changes_flag != 1:
            changes_flag = 1

    #Enter any changes in the log and return***************************************************
    if extracted_elements != []:
        result_string = ["The following repeated elements were extracted from this page:", str(extracted_elements)]
        page_log['stripRepeatedElements'] = result_string

    return body


#This function deletes h1 elements whos text is the same as the general page title text.
#Module-specific parts of titles are removes such that ("Readings (Week 2)" is treated as "Readings")
def unrepeatTitles(input_string, page_title):
    # initialize globals. changes_flag flips if atleast one change is made, page_log is a dictionary that stores messages from each function.
    global changes_flag
    global page_log

    #This array will be populated for logging purposes with h1 elements that are removed by this functtion
    removed_h1s = []
    #Search and remove any in-parantheses text from all page titles before comparing them to h1 titles in html body
    specific_title_key = re.compile(r'\s\(.+\)')
    specific_title_component = specific_title_key.search(page_title)
    #If a module-specific element was found in the title, strip it... else, use the original title
    if specific_title_component:
        #.group(0) in regex is used to return the entire match from the .search(page_title) above
        general_title = page_title.replace(specific_title_component.group(0),'')
    else:
        general_title = page_title

    #Pare the page's html body into a BeautifulSoup object
    soup = BeautifulSoup(input_string, 'html.parser')
    #Find all h1 tags in the soup
    h1s = soup.find_all('h1')
    for h1 in h1s:
        #Compare all h1s to the page title and remove matches.. strip() removes all unnecessary space around the words
        if str(h1.string).strip() == general_title.strip():
            h1.extract()
            if changes_flag != 1:
                changes_flag = 1
            removed_h1s.append(str(h1))

    #If any changes were made, add the results of this function call to the page_log
    if removed_h1s != []:
        result_string = ["The following h1 element(s) matched the page title and was removed:", str(removed_h1s)]
        page_log['unrepeatTitles'] = result_string
        body = str(soup)
    else:
        body = input_string

    return body


#Print changes for each page and append them to overall clean_pages_log array
def printAndLog(page_title):
    #Initialize global logging variables. Data from page_log will be printed and appended to overall clean_pages_log
    global page_log
    global clean_pages_log

    # For each statement, print it to the console and append it to the clean_pages_log array of lines
    clean_pages_log.append("Adjusted ({}) with the following modifications:".format(page_title))
    print("Adjusted ({}) with the following modifications:".format(page_title))
    for function in page_log:
        clean_pages_log.append('**' + function)
        print('**' + function)
        for line in page_log[function]:
            clean_pages_log.append('****' + line)
            print('****' + line)
    # end with an empty line to leave space before next page's stats
    clean_pages_log.append("")
    print("")


#Pass the page html body through several cleaning functions and log all changes using printAndLog function
def runCleaningSequence(page):
    #Initial global changes_flag with initial value = 0. This flag will flip if changes are made to the page in any of the functions called below.
    global changes_flag
    changes_flag = 0
    #Initialize global page_log as an empty dictionary. Any function that makes changes will add its changes to this global log.
    global page_log
    page_log = {}

    #Setup the global clean_pages_log for this function to append lines to
    global clean_pages_log

    #Put current page body in clean_body variable in preparation for cleaning sequence
    clean_body = page['body']

    #Run sequence of cleaning functions
    clean_body = removeHieroglyphs(clean_body)
    clean_body = textifyHeaders(clean_body)
    clean_body = stripRepeatedElements(clean_body)
    clean_body = unrepeatTitles(clean_body, page['title'])
    clean_body = divs2Heads(clean_body)
    clean_body = stripBborderSpace(clean_body)
    clean_body = encodingReplacements(clean_body)

    if changes_flag == 1:
        API.updatePageBody(page['url'], clean_body)
        printAndLog(page['title'])
    return


#Gets all pages in a course. Sends all non-empty pages to the runCleaningSequence for individual processing.
def MasterClean():
    #API.getAllPages returns an array of all pages found in a course. The list does NOT include page bodies, those must be fetched using the API.getPage function with the desired page's url as a parameter.
    pages_list = API.getAllPages()
    #Only run the next bit if at-least one page is found in the pages_list array.
    if pages_list!=[]:
        #for each page found, get all page details (including the html body) using API.getPage(page_url)
        for page_from_list in pages_list:
            page = API.getPage(page_from_list['url'])
            #Only run the next bit if the page body is not empty.
            if len(page['body']) != 0:
                runCleaningSequence(page)

        for file_line in clean_pages_log:
            print(file_line)
    return
