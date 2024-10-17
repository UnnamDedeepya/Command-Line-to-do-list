import json
from datetime import datetime, timedelta

# File where tasks will be saved
TASKS_FILE = 'tasks1.json'

# Priority levels
PRIORITY_LEVELS = ['low', 'medium', 'high']


# Load tasks from file
def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            tasks1 = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks1 = []
    return tasks1


# Save tasks to file
def save_tasks(tasks1):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks1, file, indent=4)


# Add a new task
def add_task(tasks1):
    description = input("Enter the task description: ")
    due_date = input("Enter the due date (YYYY-MM-DD) or leave blank: ")

    if due_date:
        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Task not added.")
            return

    priority = input(f"Enter priority (low, medium, high): ").lower()
    if priority not in PRIORITY_LEVELS:
        print("Invalid priority. Task not added.")
        return

    task = {
        'description': description,
        'due_date': due_date or None,
        'completed': False,
        'priority': priority
    }
    tasks1.append(task)
    save_tasks(tasks1)
    print("Task added successfully!")

# View tasks based on filter
def view_tasks(tasks1, filter_by=None):
    if not tasks1:
        print("No tasks available.")
        return

    filtered_tasks = tasks1

    if filter_by == 'completed':
        filtered_tasks = [task for task in tasks1 if task['completed']]
    elif filter_by == 'pending':
        filtered_tasks = [task for task in tasks1 if not task['completed']]
    elif filter_by == 'due_soon':
        today = datetime.now().date()
        soon = today + timedelta(days=3)
        filtered_tasks = [task for task in tasks1 if task['due_date'] and datetime.strptime(task['due_date'], '%Y-%m-%d').date() <= soon and not task['completed']]

    if not filtered_tasks:
        print("No tasks found for the selected filter.")
        return

    for idx, task in enumerate(filtered_tasks, 1):
        status = "Completed" if task['completed'] else "Pending"
        print(f"{idx}. {task['description']} | Due: {task['due_date']} | Status: {status} | Priority: {task['priority']}")


# Mark task as complete
def mark_task_completed(tasks1):
    view_tasks(tasks1, filter_by='pending')
    task_index = int(input("Enter task number to mark as completed: ")) - 1

    if 0 <= task_index < len(tasks1):
        tasks1[task_index]['completed'] = True
        save_tasks(tasks1)
        print("Task marked as completed!")
    else:
        print("Invalid task number.")


# Edit a task
def edit_task(tasks1):
    view_tasks(tasks1)
    task_index = int(input("Enter task number to edit: ")) - 1

    if 0 <= task_index < len(tasks1):
        task = tasks1[task_index]
        print(f"Editing task: {task['description']}")
        description = input(f"Enter new description (leave blank to keep '{task['description']}'): ")
        due_date = input(f"Enter new due date (YYYY-MM-DD) or leave blank to keep '{task['due_date']}': ")

        if due_date:
            try:
                due_date = datetime.strptime(due_date, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Task not updated.")
                return

        priority = input(f"Enter new priority (low, medium, high) or leave blank to keep '{task['priority']}': ").lower()
        if priority and priority not in PRIORITY_LEVELS:
            print("Invalid priority. Task not updated.")
            return

        # Apply changes
        task['description'] = description or task['description']
        task['due_date'] = due_date or task['due_date']
        task['priority'] = priority or task['priority']

        save_tasks(tasks1)
        print("Task updated successfully!")
    else:
        print("Invalid task number.")


# Delete a task
def delete_task(tasks1):
    view_tasks(tasks1)
    task_index = int(input("Enter task number to delete: ")) - 1

    if 0 <= task_index < len(tasks1):
        tasks1.pop(task_index)
        save_tasks(tasks1)
        print("Task deleted successfully!")
    else:
        print("Invalid task number.")


# User Menu
def display_menu():
    print("\nTo-Do List Manager")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Completed Tasks")
    print("4. View Pending Tasks")
    print("5. View Tasks Due Soon")
    print("6. Mark Task as Completed")
    print("7. Edit Task")
    print("8. Delete Task")
    print("9. Exit")


# Main function
def main():
    tasks1 = load_tasks()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            add_task(tasks1)
        elif choice == '2':
            view_tasks(tasks1)
        elif choice == '3':
            view_tasks(tasks1, filter_by='completed')
        elif choice == '4':
            view_tasks(tasks1, filter_by='pending')
        elif choice == '5':
            view_tasks(tasks1, filter_by='due_soon')
        elif choice == '6':
            mark_task_completed(tasks1)
        elif choice == '7':
            edit_task(tasks1)
        elif choice == '8':
            delete_task(tasks1)
        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()