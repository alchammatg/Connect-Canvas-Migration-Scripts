#Settings
import Init

#Course entry and login
from Login import tokenLogin
from Enter_Course import enterCourse

#Migration functions
from Files_To_Pages import MasterFTP
from Clean_Pages import MasterClean
from API_Calls import setHome

#Log in and enter a course
tokenLogin()
enterCourse()

#coverts HTML files to pages and fixes links to internal files/images/content_pages
MasterFTP()

#Prompts user to break up a module, tries to uniquify repeated titles of pages (ex:readings, readings-2, ..), cleans html content of each page from specified items
MasterClean()

#Sets course home page to syllabus
setHome()