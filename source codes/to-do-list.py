import os
import pathlib as pl

# Use os.path.join for cross-platform file paths
BASE_DIR = pl.Path(__file__).parent.parent / "lists"


def save_list(value, file_name):
    """
    Saves and writes the list to memory.
    Each element is written to a file, separated by '^'.
    Overwrites the file if it already exists.
    """
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(os.path.join(BASE_DIR, f"{file_name}.txt"), "w", encoding="utf-8") as f:
        for element in value:
            f.write(element + "^")


def create_and_write_list(value, file_name):
    """
    Creates a new list file and writes the list to it.
    Raises FileExistsError if the file already exists.
    """
    os.makedirs(BASE_DIR, exist_ok=True)
    try:
        with open(
            os.path.join(BASE_DIR, f"{file_name}.txt"), "x", encoding="utf-8"
        ) as f:
            for element in value:
                f.write(element + "^")
    except FileExistsError:
        print(f'group name: "{file_name}" already used: group exists')


def read_list(file_name):
    """
    Reads the list from memory.
    Returns the file content as a string, or a message if not found.
    """
    try:
        with open(
            os.path.join(BASE_DIR, f"{file_name}.txt"), "r", encoding="utf-8"
        ) as f:
            read = f.read()
        return read
    except FileNotFoundError:
        return "no task files found"


def print_list(tasks, list_name):
    """
    input type: list[str], str
    Prints the tasks in the list and saves them to file.
    Each task is printed with its index (starting from 1).
    """
    save_list(tasks, list_name)
    for idx, task in enumerate(tasks, 1):
        print(f"{idx}. {task}")


def print_group(group_name):
    """
    input type: str
    Prints all tasks in a group/list by its name.
    If the list is empty or not found, prints an appropriate message.
    """
    print(f"list: {group_name}")
    content = read_list(group_name)
    if content != "no task files found":
        tasks = content.split("^")[:-1]
        if tasks:
            for idx, task in enumerate(tasks, 1):
                print(f"{idx}. {task}")
        else:
            print("EMPTY")
    else:
        print("no task files found")


def append_item(split_list, at, tasks, activated_list_name):
    """
    Add a new task to the list if it doesn't already exist and is not empty.
    Prints the updated list after addition or if the task already exists.
    """
    new_task = split_list[at]
    if len(new_task) > 0:
        if new_task not in tasks:
            tasks.append(new_task)
            print_list(tasks, activated_list_name)
        else:
            print("task already in list")
            print_list(tasks, activated_list_name)
    else:
        print("can't add empty task")


def put_after(tasks, split_list):
    """
    Move a task after another task by their indices.
    Indices are 1-based in the user prompt.
    """
    try:
        after_finder = split_list[1].split("after")
        idx_from = int(after_finder[0]) - 1
        idx_to = int(after_finder[1])
        pop_item = tasks.pop(idx_from)
        tasks.insert(idx_to, pop_item)
        return tasks
    except (ValueError, IndexError):
        print("Invalid indices for 'putafter'.")
        return tasks


def put_before(tasks, split_list):
    """
    Move a task before another task by their indices.
    Indices are 1-based in the user prompt.
    """
    try:
        before_finder = split_list[1].split("before")
        idx_from = int(before_finder[0]) - 1
        idx_to = int(before_finder[1]) - 1
        pop_item = tasks.pop(idx_from)
        if idx_from > idx_to:
            tasks.insert(idx_to, pop_item)
        else:
            tasks.insert(idx_to - 1, pop_item)
    except (ValueError, IndexError):
        print("Invalid indices for 'putb4'.")


def delete_list(split_list):
    """
    Delete a list file after user confirmation.
    Prompts the user to confirm deletion.
    """
    if len(split_list) < 2:
        print("No list specified for deletion.")
        return
    if read_list(split_list[1]) != "no task files found":
        print_group(split_list[1])
        confirmation = input(f"confirm deletion of {split_list[1]}:(yes/no): ")
        if confirmation.lower() == "yes":
            try:
                os.remove(os.path.join(BASE_DIR, f"{split_list[1]}.txt"))
                print(f"Deleted list: {split_list[1]}")
            except Exception as e:
                print(f"Error deleting list: {e}")


def list_create(list_name):
    """
    Create a new empty list file.
    """
    os.makedirs(BASE_DIR, exist_ok=True)
    try:
        with open(
            os.path.join(BASE_DIR, f"{list_name}.txt"), "x", encoding="utf-8"
        ) as f:
            pass
    except FileExistsError:
        print(f'list name: "{list_name}" already used: list exists')


def rename_list(old_name, new_name):
    """
    Rename an existing list file to a new name.
    """
    old_path = os.path.join(BASE_DIR, f"{old_name}.txt")
    new_path = os.path.join(BASE_DIR, f"{new_name}.txt")
    if not os.path.exists(old_path):
        print(f"Cannot rename: List {old_name} does not exist.")
        return
    if os.path.exists(new_path):
        print(f"Cannot rename: A list with the name {new_name} already exists.")
        return
    os.rename(old_path, new_path)
    print(f"Renamed list from {old_name} to {new_name}")


def error_msg(msg: str):
    """Prints an error message."""
    print(f"ERROR: {msg}")


def arg_error_msg(split_list):
    """Prints an argument error message based on the command and expected number of arguments."""
    print(
        f"ARGUMENT ERROR:\n{split_list[0]} takes {ARGS_COUNTER[split_list[0]]} args -> \nGiven args: {len(split_list)-1}"
    )


ARGS_COUNTER = {
    "help": 0,
    "info": 0,
    "stop": 0,
    "add": 1,
    "list": 1,
    "pop": 1,
    "remove": 1,
    "put": 1,
    "delete": 1,
    "call": 1,
    "addmain": 1,
    "create": 1,
    "switch": 2,
    "merge": 2,
    "addat": 2,
    "sort": "variable",
    "group": "variable",
}
activated_list_name = "main"

if read_list(activated_list_name) == "no task files found":
    list_create(activated_list_name)

tasks = read_list(activated_list_name).split("^")[:-1]
print_list(tasks, activated_list_name)
prompt = None

while prompt != "stop":
    tasks = read_list(activated_list_name).split("^")[:-1]
    print(f"activated: {activated_list_name}")
    prompt = input("\nprompt: ")

    try:
        split_list = prompt.split("|")

        if split_list[0] not in ARGS_COUNTER:
            print(f"Unknown command: {split_list[0]}")
            continue

        elif split_list[0] in [
            "add",
            "list",
            "pop",
            "remove",
            "delete",
            "call",
            "addmain",
            "create",
        ]:

            if len(split_list) != 2:
                arg_error_msg(split_list)

            else:
                if split_list[0] == "add":  # add|<taskName>
                    append_item(split_list, 1, tasks, activated_list_name)

                elif split_list[0] == "list":  # list|<listname>
                    try:
                        print_group(split_list[1])
                    except IndexError:
                        (
                            print_list(tasks, activated_list_name)
                            if len(tasks) > 0
                            else print("no task listed")
                        )

                elif split_list[0] == "pop":  # pop|<taskno>
                    try:
                        deleted_item = tasks.pop(int(split_list[1]) - 1)
                        print(f"finished {deleted_item}")
                        print_list(tasks, activated_list_name)
                        if len(tasks) == 0:
                            print(
                                "All your tasks are completed"
                                "\n"
                                "Nothing more today..."
                                "\n"
                                "Enjoy the day"
                            )
                    except (IndexError, ValueError):
                        print("Invalid task number for pop.")

                elif split_list[0] == "remove":  # remove|<taskno>
                    try:
                        deleted_item = tasks.pop(int(split_list[1]) - 1)
                        print(f"removed {deleted_item}")
                        print_list(tasks, activated_list_name)
                        if len(tasks) == 0:
                            print("list empty")
                    except (IndexError, ValueError):
                        print("Invalid task number for remove.")

                elif split_list[0] == "put":  # put|<taskno>(before/after)<taskno>
                    try:
                        if "after" in split_list[1]:
                            tasks = put_after(tasks, split_list)
                        elif "before" in split_list[1]:
                            tasks = put_before(tasks, split_list)
                        else:
                            print("Specify 'before' or 'after' in put command.")
                        print_list(tasks, activated_list_name)
                    except Exception as e:
                        print(f"Error in put command: {e}")

                elif split_list[0] == "delete":
                    delete_list(split_list)

                elif split_list[0] == "call":  # call|<list name>
                    with open(
                        os.path.join(BASE_DIR, "activated_list_name.txt"),
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.write(split_list[1])
                    if read_list(split_list[1]) != "no task files found":
                        activated_list_name = split_list[1]
                        tasks = read_list(activated_list_name).split("^")[:-1]
                        print_list(tasks, activated_list_name)
                    else:
                        print("List does not exist.")

                elif split_list[0] == "addmain":  # addmain|<taskName>
                    main_tasks = read_list("main").split("^")[:-1]
                    append_item(split_list, 1, main_tasks, "main")

                elif split_list[0] == "create":
                    if len(split_list) > 1:
                        list_create(split_list[1])
                        print(f"List created by name: {split_list[1]}")
                    else:
                        print("No list name provided for create.")

        elif split_list[0] == "switch":  # switch|<taskno>|<taskno>
            try:
                idx1 = int(split_list[1]) - 1
                idx2 = int(split_list[2]) - 1
                tasks[idx1], tasks[idx2] = tasks[idx2], tasks[idx1]
                print_list(tasks, activated_list_name)
            except (IndexError, ValueError):
                print("Invalid indices for switch.")

        elif (
            split_list[0] == "group"
        ):  # group|<taskno>|<taskno>|<taskno>|as <groupname>
            name_finder = split_list[-1].split("as ")
            if "as" in prompt and len(name_finder) > 1:
                group_list = []
                temp_list = tasks.copy()
                try:
                    indices = sorted(
                        [int(i) - 1 for i in split_list[1:-1]], reverse=True
                    )
                    for idx in indices:
                        group_list.insert(0, temp_list[idx])  # maintain original order
                        tasks.pop(idx)
                    create_and_write_list(group_list, name_finder[-1])
                    print_group(name_finder[-1])
                    save_list(tasks, activated_list_name)
                except Exception as e:
                    print(f"Error creating group: {e}")
            else:
                print("no name for group creation")

        elif split_list[0] == "addat":
            # addat|<index>|<taskName>
            main_tasks = read_list(activated_list_name).split("^")[:-1]
            if len(split_list) >= 3:
                try:
                    index = int(split_list[1]) - 1
                    task_to_add = split_list[2]
                    if len(task_to_add) > 0:
                        if task_to_add not in main_tasks:
                            main_tasks.insert(index, task_to_add)
                            print_list(main_tasks, activated_list_name)
                            save_list(main_tasks, activated_list_name)
                        else:
                            print("task already in list")
                            print_list(main_tasks, activated_list_name)
                    else:
                        print("can't add empty task")
                except (ValueError, IndexError):
                    print("Invalid index for addat.")
            else:
                print("Insufficient arguments for addat.")

        elif split_list[0] == "sort":
            main_tasks = read_list(activated_list_name).split("^")[:-1]
            try:
                indices = [int(i) - 1 for i in split_list[1:]]
                if any(i < 0 or i >= len(main_tasks) for i in indices):
                    print("One or more indices out of range.")
                else:
                    sorted_tasks = [main_tasks[i] for i in indices]
                    remaining_tasks = [
                        task
                        for idx, task in enumerate(main_tasks)
                        if idx not in indices
                    ]
                    main_tasks = sorted_tasks + remaining_tasks
                    print_list(main_tasks, activated_list_name)
                    save_list(main_tasks, activated_list_name)
            except ValueError:
                print("Invalid indices for sort.")

        elif split_list[0] == "merge":
            if (
                len(split_list) >= 3
                and read_list(split_list[1]) != "no task files found"
                and read_list(split_list[2]) != "no task files found"
            ):
                merged_list = read_list(split_list[1]).split("^")[:-1]
                merged_list.extend(read_list(split_list[2]).split("^")[:-1])
                try:
                    split_list[3]
                    create_and_write_list(merged_list, split_list[3])
                except IndexError:
                    print("The file name was not given")
            else:
                print("please enter correct file names")

        elif split_list[0] == "rename":
            rename_list(split_list[1], split_list[2])

        elif split_list[0] == "info":
            print(f"Activated list: {activated_list_name}")
            print_group(activated_list_name)

        elif split_list[0] == "help":
            print("Available commands:")
            print(" - add | <taskname>")
            print(" - list | <listname>")
            print(" - pop | <taskno>")
            print(" - remove | <taskno>")
            print(" - switch | <taskno> | <taskno>")
            print(" - put | <taskno> before/after <taskno>")
            print(" - group | <taskno> as <groupname>")
            print(" - call | <listname>")
            print(" - addat | <index> | <taskname>")
            print(" - addmain | <taskname>")
            print(" - sort | <taskno> <taskno> ...")
            print(" - delete | <listname>")
            print(" - merge | <list1> | <list2> | <newlist>")
            print(" - info")
            print(" - help")
            print(" - stop")
            print(
                "Note: Commands are case-sensitive and should be entered in the specified format.\n\tDon't use spaces around '|' in commands."
            )

        elif prompt == "stop":
            break

        # Save changes to the current list after each command that modifies it
        if split_list[0] in ["add", "pop", "remove", "switch", "put", "group"]:
            save_list(tasks, activated_list_name)

    except IndexError as e:
        try:
            (
                print(f"no task found in {split_list[1]}:", e)
                if len(split_list) > 1 and int(split_list[1]) > len(tasks)  # type: ignore
                else print(f"no task found in {split_list[2]}:", e)
            )
        except Exception:
            print(f"no task index specified", e)
    except ValueError as e:
        print("incorrect values", "error: ", e)
    except Exception as e:
        print(f"an error occurred: {e}")
    finally:
        print(split_list)
