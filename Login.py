import API_Calls as API
import Init

def tokenLogin():
    while(True):
        token = input("Please enter your Canvas API Access Token:")
        test = API.testToken(token)
        #Look against the keyword errors in API request return
        if 'errors' not in test:
            Init.Access_Token = token
            break
        else:
            print("Invalid entry, try again.")
    return