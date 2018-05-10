from Files_To_Pages import MasterFTP
from Fix_Internal_Links import fixInternalLinks
from Modulate import MasterModulateBysub
from Clean_Pages import MasterClean
from Uniquify_Titles import MasterUT
from API_Calls import setHome


def fullMigration():
    MasterModulateBysub()
    MasterFTP()
    fixInternalLinks()
    MasterUT()
    MasterClean()
    setHome()