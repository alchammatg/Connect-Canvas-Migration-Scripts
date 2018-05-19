# connect-canvas-migration-scripts
Python/CanvasAPI

This repository contains a collection of Python scripts that leverage the Canvas API to automate multiple elements of the Connect to Canvas course migration process. The main way to operate the scripts is by editing and launching the file Main.py. All API calls are made through the API_Calls file which is imported to other files and used by the name API. For example, when you call tokenLogin() from Main.py, tokenLogin() calls API.testToken() which it has access to by importing the API_Calls module with the overwritten name API.


**Main.py:**

This file contains a collection of imports from the rest of the files in this repository. Here, you can queue up various functions to be performed on a course in sequence. You can even modify the code to queue up many courses for modification.

**Init.py:**

Before you can interact with the Canvas API, your access token needs to be stored in Init.Access_Token Variable. *You can store your token by calling the tokenLogin() function through Main.py*. To interact with a course, its short course ID needs to be store in Init.Short_Course_ID. *You can store a course ID by calling enterCourse() through Main.py*.

**API_Calls.py:**

Using the library *requests*, API calls are made to the Canvas API through a collection of small functions in this file.

******************************************************************************************************************************

All the remaining files except Services.py contain one Master function which I have imported directly into Main.py. Services.py contains four Master functions, which you can call in Main by entering Services.{FunctionName}
