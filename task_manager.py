# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

# importing libraries
import os
from datetime import datetime

DATETIME_STRING_FORMAT = "%Y-%m-%d" # the date format to be used, using format codes 
todays_date = datetime.now()

def save_to_file() :
# is called in other functions to write task_list to file tasks.txt

    # opens tasks.txt, rewriting its contents. loops through the dictionary nested within list task_list, 
    # joining the values of the dictionary using semicolon delimeter appending to a temporary list then saved to file
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    

def reg_user() :
# is called main menu to add a new user to username_password and user.txt

    # user is prompted to enter a new username. if its already in use, the user will be 
    # given a second chance to enter a new user name before function is exited
    count = 0
    while True :
        new_username = input("New Username: ") 
        if new_username not in username_password.keys() :
            break
        elif count < 2 :
            print("Error this user name already exists, please try again")
            count += 1       
        else :
            print("Number of attempts exceeded")
            return

    # user prompted to enter the new users password twice
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password are the same. if true, the 
    # dictionary username_password is updated with a new pair of key: username and value: password
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        
        # the keys of dictionary username_password is looped through, with pairs appended to the list user_data
        # with it being written to file user.txt
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    
    # Otherwise print error message
    else:
        print("Passwords do no match")


def add_task() : 
# is called from main menu to add a new task to task_list and then updating tasks.txt

    read_tasks_file()

    # user prompted to enter a user to assign task to. if value entered is not a key in the dictionary username_password, 
    # error message is printed and return function exits to main while loop
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    
    # user prompted to enter title, description and due date of task. if entered date format is incorrect the user is prompted to retry.
    # using method strptime to create a datetime object in format %Y-%m-%d from the user entered date 
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    
    # create dictionary of key - value pairs for this new task and append to list task_list 
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": todays_date,
        "completed": False
    }
    task_list.append(new_task)

    # message printed and function save_to_file called to write the list task_list to file tasks.txt
    print("Task successfully added.")
    save_to_file()


def view_all() : 
# is called from main menu to display all tasks
    
    read_tasks_file()

    # takes the list task_list read from file tasks.txt, looping through the list, using its nested dictionary 
    # key-values to print the tasks in a readable format 
    print (f"\n\n{'':_>120}\n")
    for this_task in task_list:
        disp_str = f"Task: \t\t {this_task['title']}\n"
        disp_str += f"Assigned to: \t {this_task['username']}\n"
        disp_str += f"Date Assigned: \t {this_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {this_task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Complete? \t {'Yes' if this_task['completed'] == True else 'No'}\n"
        disp_str += f"Task Description: \n{this_task['description']}\n"
        disp_str += f"{'':_>120}\n"
        print(disp_str)


def view_mine() : 
# is called from main menu to view all the tasks that have been assigned to the user and edit those tasks.
    
    read_tasks_file()

    task_list_index = 0 # used to refer to the tasks index in task_list
    task_count = 1 # used to count/identify users tasks

    # initialises a empty list and dictionary for the storage of the specific users tasks in same format as task_list
    this_task = {} 
    users_tasks = []
    
    # print row titles
    print(f"\n{'Current User: ':}{curr_user}\n")    
    disp_str = f"{'Id Number: ':15}{'Date Assigned: ':19}{'Date Due: ':15}{'completed: ':15}{'Task: ':21}{'Task Description: '}"
    print(disp_str)

    # loop through all tasks in list task_list
    for t in task_list:
        
        # compares each tasks username value with the current logged in user. if theyre the same, saves the task information to 
        # dictionary this_task which is appended to list users_tasks. 
        if t['username'] == curr_user:
            this_task["index"] = task_list_index # records the index in task_list of this current task
            this_task["username"] = t['username']
            this_task["date_assigned"] = t['assigned_date'].strftime(DATETIME_STRING_FORMAT)
            this_task["due_date"] = t['due_date'].strftime(DATETIME_STRING_FORMAT)
            this_task["completed"] = "Yes" if t['completed'] == True else "No"
            this_task["title"] = t['title']
            this_task["description"] = t['description']
            users_tasks.append(this_task.copy()) # append with shallow copy
            
            # prints the task values in a easily readable format
            disp_str = f"{task_count:<15}{this_task['date_assigned']:<19}{this_task['due_date']:<15}{this_task['completed']:<15}{this_task['title']:<21}{this_task['description']}"
            print(disp_str)
            
            task_count+=1
        task_list_index +=1 

    # prompts user to decide which task to edit or return to main menu
    try:
        user_input_1 = int(input('''\nenter a task number to edit / mark as complete
or enter -1 to return to the main menu
: '''))
    except ValueError :
        print("error invalid input")
        return
    
    # exits function to main menu if -1 entered   
    if user_input_1 == -1 :
        return

    # checks if entered task is a valid value and if already complete prints a error message and exits to main menu
    elif user_input_1-1 < len(users_tasks) and users_tasks[user_input_1-1]["completed"] == "Yes":
        print("\nunable to reassign task as it has already been completed") 
        return

    # checks that value enetered is a valid task
    elif user_input_1-1  < len(users_tasks) : 
        
        # prompts user to decide which operation to perform on the task
        user_input_2 = input('''\nenter a value you wish to change
MC - Mark as complete 
CU - Change user the task is assigned to
CD - Change due date
: ''').lower()
        
        # marks the task complete in list task_list
        if user_input_2 == "mc" :            
            task_list[users_tasks[user_input_1-1]['index']]['completed'] = True

        # changes which user the task is assigned to. 
        elif user_input_2 == "cu" :

            # prompts the user to enter a new user name then checks the value is valid. before assigning the new username to task_list or printing a error message
            new_username = input("""enter the username to assign this task to
            : """)
            if new_username in username_password.keys():# checks input is a key of dictionary username_password
                task_list[users_tasks[user_input_1-1]['index']]['username'] = new_username
            else :
                print(f"error the username {new_username} does not exist")

        # changes the due date for the task
        elif user_input_2 == "cd" :
            # prompts user to enter a new date, if the format is correct it is assigned to task_list or a error message is displayed
            try:
                task_due_date = input("""enter a new date in format (YYYY-MM-DD)
: """)
                task_list[users_tasks[user_input_1-1]['index']]['due_date'] = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)               
            except ValueError:
                print("Error invalid datetime format")

    # catches invalid user input and prints a error message
    else :
        print("\nerror invalid value entered")
        return
    
    # calls this function to save task_list to file when a valid operation has been completed  
    save_to_file()        


def generate_reports(output) :
# is called from main menu to calculate the task statistics and either print or save them to files user_overview.txt and task_overview.txt depending on which argument is passed to it

    # calls functions to read tasks and user files or create them
    read_users_file()
    read_tasks_file()

    total_no_of_tasks = len(task_list) # total numbber of tasks generated
    total_complete_tasks = 0 # total number of completed tasks
    incomplete_overdue_tasks = 0 # total number of uncomplete and overdue tasks:
    user_list = [] # initialise a empty list to be appended with unique usernames and their statistics
    
    # loops through the tasks of list task_list with the first two if statements counting the complete and overdue incomplete tasks
    for task in task_list :
        if task['completed'] == True :
            total_complete_tasks+=1
        elif todays_date > task['due_date'] : 
            incomplete_overdue_tasks +=1
            
        # this loops through the list user_list, comparing the username of the task from the outer loop above to the usernames of elements in user_list. 
        # its statements count the users tasks, those completed and overdue 
        for looped_user in user_list :# loop through listt of dict
            if task['username'] == looped_user['username'] :
                looped_user['number_of_tasks'] += 1
                looped_user['number_tasks_completed'] += 1 if task['completed'] is True else 0
                looped_user['number_tasks_overdue'] += 1 if (todays_date > task['due_date'] and task['completed'] is False) else 0 #????????????????????
                break
        # when the username of the task isnt in user_list, this else statement appends it
        # with the new username and begins counting the users statistics
        else : 
            this_dict = { 'username' : task['username'],
                        'number_of_tasks' : 1, 
                        'number_tasks_completed' : 1 if task['completed'] is True else 0, 
                        'number_tasks_overdue' : 1 if (todays_date > task['due_date'] and task['completed'] is False) else 0 }
            user_list.append(this_dict)
        
    # generation of first part of string for user_overview 
    user_overview_data = f"""\n\n{'':_>120}\n\n
Total number of users registered: {len(user_list)}
Total number of tasks generated: {total_no_of_tasks}
        \n\n{'':_>120}\n\n\n"""

    # loops through user_list calculating statistics and embedding them in the string
    for looped_user in user_list :
        percentage_total_tasks = round((looped_user['number_of_tasks']/total_no_of_tasks)*100, 1)
        percentage_completed_tasks = round((looped_user['number_tasks_completed']/looped_user['number_of_tasks'])*100, 1)
        percentage_incomplete_overdue = round((looped_user['number_tasks_overdue']/looped_user['number_of_tasks'])*100, 1)

        user_overview_data += f"""Assigned username: {looped_user['username']}
The users number of assigned tasks: {looped_user['number_of_tasks']}
The percentage of total tasks assigned to user : {percentage_total_tasks}%
The percentage of users completed tasks: {percentage_completed_tasks}%
The percentage of users incomplete tasks: {100-percentage_completed_tasks}% 
The percentage of tasks assigned to this user that are overdue and not complete: {percentage_incomplete_overdue}%
    \n\n{'':_>120}\n\n\n""" 

    # calculations for task_overview and then embedding them in a string
    incomplete_tasks = total_no_of_tasks - total_complete_tasks # total number of incomplete tasks
    percentage_overdue = (incomplete_overdue_tasks/total_no_of_tasks)*100
    percentage_incomplete = (incomplete_tasks/total_no_of_tasks)*100

    task_overview_data = f"""\n\n{'':_>120}\n\n
Total number of tasks generated: {total_no_of_tasks}\n
Total number of completed tasks: {total_complete_tasks}\n
Total number of incomplete tasks: {incomplete_tasks}\n
Total number of incomplete overdue tasks: {incomplete_overdue_tasks}\n
The percentage of incomplete tasks: {round(percentage_incomplete, 1)}%\n
The percentage of incomplete overdue tasks: {round(percentage_overdue, 1)}%
    \n\n{'':_>120}\n\n"""
    
    # using the argument passed to the function to either write to the files task_overview and user_overview or print to screen
    if output == "print to screen" :
        print(task_overview_data, user_overview_data)    
    elif output == "save to file" :
        with open("user_overview.txt", "w+") as file :
            file.write(user_overview_data)            
        with open("task_overview.txt", "w+") as file :    
            file.write(task_overview_data)
    
            

def read_users_file() :
# is called from main menu to read the user file and assign the values to a dictionary

    # initialise a empty global dictionary for user/password storage
    global username_password 
    username_password = {}

    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # reads each line of user file to list user_data 
    with open("user.txt", 'r', encoding='utf-8') as user_file:
        user_data = user_file.read().split("\n")
    
    # splits each element of user_data on semicolon delimeter then stored in dictionary username_password with username as key and passwrod for value
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password


def read_tasks_file() :
# is called to read tasks.txt to nested dictionary within list task_list 

    # initialises a empty global list task_list for use in other functions
    global task_list
    task_list = [] 

    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    # reads tasks file outputing each line to list task_data
    with open("tasks.txt", 'r', encoding='utf-8') as task_file:
        task_data = task_file.read().split("\n") # create  alist of each line
        task_data = [t for t in task_data if t != ""]
    
    # loop through the list. splitting each line on semicolon delimeeter and assigning those elements to list task_data. 
    # manually assigning each element of task_data to keys of dictionary curr_t, which is nested within list task_list
    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component to the dictionary curr_t and appending it to list task_list 
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        
        task_list.append(curr_t)

    
# this function is called to read users file
read_users_file()

# user prompted to input username and password until a valid pair is entered
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# main menu created where user is prompted to enter valid operations
while True:
    print()

    # the following if - else statement prints different menus dependant if logged in user is admin or not
    if curr_user == "admin" :
            menu = input('''Select one of the following Options below:
r - Registering a user
a - Add a task
va - View all tasks
vm - View my task
gr - Generate Reports
ds - Display statistics
e - Exit
: ''').lower()
    else :
            menu = input('''Select one of the following Options below:
a - Add a task
va - View all tasks
vm - View my task
e - Exit
: ''').lower()

    # condition ensures only admin is allowed to see the generated reports / register new users / view statistics
    if curr_user != "admin" and (menu == "r" or menu == "gr" or menu == "ds") :
        print("\nerror your account does not have required privileges")

    # reg_user function is called to add a user to the database and save to file
    elif menu == 'r':
        reg_user()

    # add_task function is called to allow a user to add a new task to database and save to file
    elif menu == 'a':
        add_task()

    # view_all function called to print all tasks within tasks.txt
    elif menu == 'va':
        view_all()
    # view_mine function called to display the users tasks and allow editing
    elif menu == 'vm':
        view_mine()   

    # generate_reports function called to calculate statistics of tasks/users then save to file
    elif menu == "gr" :
        generate_reports("save to file")

    # generate reports function with 'print to screen' argument to display statistics 
    elif menu == 'ds' :
        # from the assignemnt descriptions' last bullet point - 'display statistics so that the reports generated are read from tasks.txt and users.txt 
        # and then displayed on the screen' - i assume that means print the statisitics from the reports generated in previous step
        generate_reports("print to screen") 

    # allows user to exit program
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    
    # prints error message
    else:
        print("You have made a wrong choice, Please Try again")
