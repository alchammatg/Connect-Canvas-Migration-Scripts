import Init
import API_Calls as API


def enterCourse():
    while(True):
        input_short_course_id = input("Enter Course ID:")
        input_full_course_id = "11224" + input_short_course_id.zfill(13)
        try:
            course = API.testCourse(input_full_course_id)
            #The next line will make or break the try statement. If the Canvas course does not exists, course['name'] won't exist
            print("Found Course: ({})\n".format(course['name']))
            #If the course was successfully found, save course code to Init variables and break the while loop
            Init.Course_ID = input_full_course_id
            Init.Short_Course_ID = input_short_course_id
            break
        except:
            #Don't break the loop to allow user to input again
            print("Invalid Course ID. The requested course either does not exist, or you do not have access to it.")
    return