# Capstone-III

# Task Manager

A simple Task Manager application written in Python. This application allows users to manage tasks through a command-line interface. It supports various functionalities like adding tasks, editing tasks, marking tasks as complete, viewing all tasks, and generating reports.

## Features

- **User Authentication:** Users must log in with their credentials to interact with the system.
- **Task Management:** Users can add new tasks, edit tasks, mark tasks as complete, and view tasks.
- **Admin Privileges:** Admin users can register new users and access additional features like generating reports and viewing statistics.
- **Reports:** Admin users can generate task and user overview reports.
- **Statistics:** Admin users can display statistics related to tasks and users.


## Functions

- `percentage(parts, whole)`: Calculate and return a string with the percentage.
- `edit_due_date()`: Allows editing of a task's due date.
- `edit_username()`: Allows editing of the username a task is assigned to.
- `write_task_file(tasks)`: Writes task data to `tasks.txt`.
- `reg_user()`: Allows an admin user to register a new user.
- `add_task()`: Adds a new task to `tasks.txt`.
- `view_all()`: Allows a user to view all tasks.
- `view_mine()`: Allows a user to view tasks assigned to them.
- `generate_report(tasks, users)`: Generates task and user overview reports.
- `display_statistics()`: Displays statistics from generated reports.


## Files

- `tasks.txt`: Stores task-related data.
- `user.txt`: Stores user credentials.
- `task_overview.txt`: Stores the task overview report.
- `user_overview.txt`: Stores the user overview report.

