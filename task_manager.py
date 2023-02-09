# =====Importing Libraries===========
from datetime import datetime
import os


# =====Globals===========
datetime_string_format = "%d %b %Y"
admin_menu = {
    'r': 'Registering a user',
    'a': 'Adding a task',
    'va': 'View all tasks',
    'vm': 'View my task',
    'gr': 'Generate reports',
    'ds': 'Display statistics',
    'e': 'Exit'
}
user_menu = {
    'a': 'Adding a task',
    'va': 'View all tasks',
    'vm': 'View my task',
    'e': 'Exit'
}


# =========Functions==========
# calculate and return a string with the percentage
def percentage(parts, whole):
    return f'{round((parts / whole * 100), 2)}%'


def edit_due_date():
    while True:
        due_date = input("Enter date in the format '01 Jan 1999': ")
        try:
            # initializing and checking if format matches the date
            due_date = datetime.strptime(due_date, "%d %b %Y")
        except ValueError:
            print("Incorrect date format, please enter a proper date.")
        else:
            if due_date.date() >= datetime.now().date():
                return due_date.strftime("%d %b %Y")
            print("Date must not be in the past.")


def edit_username():
    username = input("Enter username of person the task should be assigned to: ")
    if username in ["v", ""]:
        return "v"
    elif username not in user_ppd:
        print("The username does not exist. Select one of the options below:\n\nv - Go back to Main Menu, or ")
        return edit_username()
    else:
        return username


def write_task_file(tasks):
    with open("tasks.txt", "w") as file:
        task_list_to_write = []
        for t in tasks:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'],
                t['assigned_date'],
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        file.write("\n".join(task_list_to_write))



# adding a new user to the user.txt file (admin ONLY)
def reg_user():
    # request new username input
    new_username = input("New Username: ")
    while new_username in user_ppd:
        print(f"username already exists. Choose another name\n")
        new_username = input("New Username: ")
    else:
        # request and confirm new password input
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

    # check if new password and confirmed password are the same
    if new_password == confirm_password:
        print("New user added")
        user_ppd[new_username] = new_password

        with open("user.txt", "w") as user_file:
            # write new username and password in the file
            user_file.write("\n".join([f"{k};{user_ppd[k]}" for k in user_ppd]))

    # otherwise print a relevant message
    else:
        print("Passwords do no match, user has not been registered")



# adding a new task to task.txt file
def add_task():
    # request the following input from the user:
    task_username = input("Enter username of the person the task is to be assigned to: ")

    task_title = input("Task title: ")

    task_description = input("Task description: ")

    due_date_time = edit_due_date()

    today = datetime.today()
    current_date = today.strftime("%d %b %Y")

    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": current_date,
        "completed": False
    }

    task_list.append(new_task)
    write_task_file(task_list)
    print("Task successfully added.")


# creating a task list
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    current_task = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    current_task['username'] = task_components[0]
    current_task['title'] = task_components[1]
    current_task['description'] = task_components[2]
    current_task['due_date'] = task_components[3]
    current_task['assigned_date'] = task_components[4]
    current_task['completed'] = "Yes" if task_components[5] == "Yes" else False

    task_list.append(current_task)



# allow user to view all tasks
def view_all():
    for idx, t in enumerate(task_list, 1):
        all_tasks = f'——————————————[Task {idx}]————————————————————\n'
        all_tasks += '\n'
        all_tasks += f"User assigned to:  {t['username']}\n"
        all_tasks += f"Task Title:       {t['title']}\n"
        all_tasks += f"Task Description: {t['description']}\n"
        all_tasks += f"Date Assigned:    {t['assigned_date']}\n"
        all_tasks += f"Due Date:         {t['due_date']}\n"
        all_tasks += f"Task complete?:    {'Yes' if t['completed'] else 'No'}\n"

        print(all_tasks)



# allow a user to view tasks assigned to only them
def view_mine():
    for idx, t in enumerate(task_list, 1):
        if t['username'] == current_user:
            my_tasks = f'———————————[Task {idx} - {current_user}]————————————————\n'
            my_tasks += '\n'
            my_tasks += f"Task Title:       {t['title']}\n"
            my_tasks += f"Task Description: {t['description']}\n"
            my_tasks += f"Date Assigned:    {t['assigned_date']}\n"
            my_tasks += f"Due Date:         {t['due_date']}\n"
            my_tasks += f"Task complete?:    {'Yes' if t['completed'] else 'No'}\n"

            print(my_tasks)

    while True:
        # ask user to select task
        try:
            task_select = int(input("""Type the number of the task to select it.
Or type '-1' to go back to the main menu : \n"""))
            task_select = task_select - 1

        except ValueError:
            task_select = -1
            print("Invalid option selected. Please use the format specified")

        if task_select == -1:
            return

        elif task_select > len(task_list) - 1:
            print("There is no task with this identifier.\n")

        else:
            # request user to choose an option, edit is displayed only if the selected task is not completed
            task_option = input(f"""\nSelect one of the following options below:
m - Mark the task as complete
{(not task_list[task_select]["completed"]) * "d - Edit the task"}\n\n""").lower()

            if task_option == "m":
                # changing task's completed value to True
                task_list[task_select]["completed"] = True
                print(f"Task number {task_select} has been marked as completed\n")
            elif task_option == "d":
                # user can change the username and/or due date
                task_username = edit_username()
                if task_username == "v":
                    break
                else:
                    task_list[task_select]["username"] = task_username
                task_list[task_select]["due_date"] = edit_due_date()
                print("Task successfully edited.")
                break
            else:
                print("You have made a wrong choice, Please Try again\n")

            # write changes to task.txt file
            write_task_file(task_list)
            return



def generate_report(tasks, users):
    # current date 
    today = datetime.today()
    current_date = today.strftime("%d %b %Y")

    # create a dictionary for the full report
    report = {"total_tasks": len(tasks),
              "total_users": len(users),
              "total_completed": 0,
              "overdue": 0,
              "users": {}
              }

    for task in tasks:
        # check if username is in the users dictionary
        if task["username"] not in report["users"]:
            # create a dictionary for that user
            report["users"][task["username"]] = {"n_of_tasks": 0, "completed": 0, "overdue": 0}

        # increasing the number of task of a specific user
        report["users"][task["username"]]["n_of_tasks"] += 1

        # check if task is completed and add it to the report dictionary
        if task["completed"]:
            report["total_completed"] += 1
            report["users"][task["username"]]["completed"] += 1

        # check if task is not completed and overdue and add it to the report dictionary
        if task["due_date"] < current_date and task["completed"] is not True:
            report["overdue"] += 1
            report["users"][task["username"]]["overdue"] += 1

    # adding users that don't have tasks assigned to them
    for user in user_data:
        user = user.split(";")[0]
        if user not in report["users"]:
            report["users"][user] = {"n_of_tasks": 0, "completed": 0, "overdue": 0}

    # write the output files task_overview.txt and user_overview.txt
    with open("task_overview.txt", "w") as task_overview_file, open("user_overview.txt", "w") as user_overview_file:
        task_overview_file.write(f"""----------------------------------------------------
Task Overview Report
Date : {today.strftime("%d %b %Y")}
----------------------------------------------------
Total number of tasks :                      {report["total_tasks"]}
Total number of completed tasks :            {report["total_completed"]}
Total number of uncompleted tasks :          {report["total_tasks"] - report["total_completed"]}
Total number of overdue uncompleted tasks:   {report["overdue"]}
The percentage of tasks that are incomplete: {round((report["total_tasks"] - report["total_completed"]) / report["total_tasks"] * 100, 2)}% 
The percentage of tasks that are overdue:    {round(report["overdue"] / report["total_tasks"] * 100, 2)}%""")

        user_overview_file.write(f"""------------------------------------
User Overview Report
Date : {today.strftime('%Y-%m-%d')}
--------------------------------------------------
Total number of user :                       {report["total_users"]}
Total number of tasks :                      {report["total_tasks"]}
--------------------------------------------------\n""")
        for user in report["users"]:
            try:
                user_overview_file.write(f"""\nUsername : {user}\n
Total number of tasks assigned to the user :                                                   {report["users"][user]["n_of_tasks"]}
Percentage of the total number of tasks that have been assigned to the user :                  {percentage(report["users"][user]["n_of_tasks"], report["total_tasks"])}
Percentage of the tasks assigned to the user that have completed :                             {percentage(report["users"][user]["completed"], report["users"][user]["n_of_tasks"])}
Percentage of the tasks assigned to the user that must still be completed :                    {percentage((report["users"][user]["n_of_tasks"] - report["users"][user]["completed"]), report["users"][user]["n_of_tasks"])}
Percentage of the tasks assigned to the user that have not yet been completed and are overdue: {percentage(report["users"][user]["overdue"], report["users"][user]["n_of_tasks"])}\n
-----------------------------------------------------------------------------------------------------\n""")
            except ZeroDivisionError:
                user_overview_file.write(f"""\nUsername : {user}\n
Total number of tasks assigned to the user :                                                   0
Percentage of the total number of tasks that have been assigned to the user :                  0%
Percentage of the tasks assigned to the user that have completed :                             0%
Percentage of the tasks assigned to the user that must still be completed :                    0%
Percentage of the tasks assigned to the user that have not yet been completed and are overdue: 0%
-----------------------------------------------------------------------------------------------------\n""")

    print("Reports generated in task_overview.txt and user_overview.txt files")



def display_statistics():
    with open("task_overview.txt", "r") as task_overview_file, open("user_overview.txt", "r") as user_overview_file:
        print("--------------------- Report ---------------------")
        print()
        for line, content in enumerate(task_overview_file):
            if line not in [0, 1, 3]:
                print(content[:-1])
        for line, content in enumerate(user_overview_file):
            if line not in [0, 1, 2, 3, 5]:
                print(content[:-1])



# ====Login Section====
# read username and password from the user.txt file to allow a user to login
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# convert to a dictionary
user_ppd = {user.split(";")[0]: user.split(";")[1] for user in user_data}

current_user = {}
current_pass = {}

logged_in = False
while not logged_in:

    current_user = input("Username: ")
    current_pass = input("Password: ")
    if current_user not in user_ppd.keys():
        print(f"User does not exist\n")
        continue
    elif user_ppd[current_user] != current_pass:
        print(f"Wrong password\n")
        continue
    else:
        print("Login Successful!")
        logged_in = True


# creating separate user menus
while True:
    print("\nSelect one of the following Options below:")
    if current_user == 'admin':
        menu_item = admin_menu
    else:
        menu_item = user_menu
    [print(f"{key} : {value}") for key, value in menu_item.items()]
    print()

    # request menu input
    menu_choice = input(':').lower()
    if menu_choice in menu_item.keys():
        print()
    else:
        print(f"{menu_choice} is not an option, please choose from the list")

    if menu_choice == 'r' and current_user == 'admin':
        '''If the user is an admin then they can register a new user'''
        reg_user()

    elif menu_choice == 'a':
        add_task()

    elif menu_choice == 'va':
        view_all()

    elif menu_choice == 'vm':
        view_mine()

    elif menu_choice == 'gr' and current_user == 'admin':
        ''' a user can generate reports ONLY if they have the admin role '''
        generate_report(task_list, user_data)

    elif menu_choice == 'ds' and current_user == 'admin':
        ''' a user can display statistics ONLY if they have the admin role '''
        # check if the reports have been generated, if not generate them
        if not (os.path.exists("task_overview.txt") or os.path.exists("user_overview.txt")):
            generate_report(task_list, user_data)
        display_statistics()

    elif menu_choice == 'e':
        print('Goodbye!!!')
        exit()

    # otherwise print a relevant message
    else:
        print("You have made a wrong choice, Please Try again")
