import API_Calls as API
from bs4 import BeautifulSoup
import Init
import unidecode

def getImageNameDuplicates(images):
    image_names = []
    unique_image_names = []
    duplicate_image_names = []

    for image in images:
        image_names.append(image['display_name'])

    for image_name in image_names:
        if image_name not in unique_image_names:
            unique_image_names.append(image_name)
        else:
            #Removing the existing name from  unique_array then add it to duplicate_array
            unique_image_names.remove(image_name)
            duplicate_image_names.append(image_name)
            break
    return duplicate_image_names


def fixInternalLinks():
    print("****FIXING INTERNAL LINKS****")
    pages = API.getAllPages()
    files = API.getAllFiles("")
    images = API.getAllFiles("image")
    #flag duplicate image names to decide how to fix image links
    duplicate_image_names = getImageNameDuplicates(images)

    if duplicate_image_names != []:
        #if a valid input is entered, make appropriate changes and exit the loop. Else, prompt reentry
        while (True):
            image_inclusion = input("The following duplicate image names were found in your course:\n{}\nThis function cannot distinguish between different images with the same name.\nSelect one:\n1. Remove listed images\n2. Include listed imagees - ONLY IF: They are identical and don't need to be distinguished\n3. Don't fix any image links\n".format(duplicate_image_names))
            if image_inclusion == '1':
                print("Removing images with repeated names from the fixing list.")
                for image in images:
                    if image['display_name'] in duplicate_image_names:
                        images.remove(image)
                break
            elif image_inclusion == '2':
                print("Continuing without removing duplicate images.")
                break
            elif image_inclusion == '3':
                #overwrite images with empty array
                images = []
                break
            else:
                print("Invalid Input. Please enter one of the specified digit choices.")

    #Files with these extension/type can be viewed in the Canvas previewer
    previewable_types = ['doc', 'odt', 'sxi', 'docx', 'pdf', 'sxw', 'odf', 'ppt', 'xlsx', 'odg', 'pptx', 'xls', 'odp',
                         'rtf', 'txt', 'ods', 'sxc']

    processed_item_count = 0
    for page in pages:
        processed_item_count+=1

        body = API.getPage(page['url'])['body']
        image_flag, file_flag, page_flag = False, False, False
        if body is not None:
            soup = BeautifulSoup(body,"html.parser")

            aTags = soup.findAll('a',href=True)
            if aTags:
                for aTag in aTags:
                    decoded_href = aTag['href'].replace('%20', ' ')

                    #Loop through all page URLs looking for matches between html-href and  decoded url
                    for pageUrlHtml in Init.pageUrlHtmlList:
                        aTagtextToUrl = unidecode.unidecode(aTag.get_text().replace(' ', '-').lower())
                        if (pageUrlHtml.html in decoded_href or aTagtextToUrl == pageUrlHtml.url):
                            page_flag = True

                    #Loop through all files looking for matches between html-href and file display name
                    for file in files:
                        if file['display_name'] in decoded_href:
                            print("Match(file) - {}".format(file['display_name']))
                            file_flag = True
                            for type in previewable_types:
                                if type in file['content-type']:
                                    aTag['class'] = "instructure_file_link instructure_scribd_file"
                            aTag['href'] = "https://canvas.ubc.ca/courses/{}/files/{}/download"\
                                .format(Init.Short_Course_ID,file['id'])
                            aTag['title'] = file['display_name']


            imageTags = soup.findAll('img',src=True)
            if imageTags:
                for img in imageTags:
                    decoded_image = img['src'].replace('%20', ' ')

                    #Loop through all images looking for matches between html-src and image display name
                    for image in images:
                        if image['display_name'] in decoded_image:
                            print("Match(Image) - {}".format(image['display_name']))
                            image_flag = True
                            img['src'] = "https://canvas.ubc.ca/courses/{}/files/{}/preview"\
                                .format(Init.Short_Course_ID,image['id'])

            body = str(soup)

            if file_flag == True or image_flag == True or page_flag == True:
                API.updatePageBody(page['url'], body)
    return