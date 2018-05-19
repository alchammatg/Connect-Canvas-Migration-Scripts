#Course entry and login
from Login import tokenLogin
from Enter_Course import enterCourse

#Migration functions
from Files_To_Pages import MasterFTP
from Clean_Pages import MasterClean
from Modulate import MasterModulate
from Uniquify_Titles import MasterUniquifyTitles
from Fix_Internal_Links import fixInternalLinks
from API_Calls import setHome
import Services

################################################

#Log in and enter a course
tokenLogin()
enterCourse()

#coverts HTML files to pages and fixes links to internal files/images/content_pages
MasterFTP()

MasterClean()

#Sets course home page
setHome('syllabus')
