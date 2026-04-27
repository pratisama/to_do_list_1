import os
import pathlib as pl

# Use os.path.join for cross-platform file paths
BASE_DIR = pl.Path(__file__).parent / "lists"


def save_list(value, fileName):
    """
    Saves and writes the list to memory.
    Each element is written to a file, separated by '^'.
    Overwrites the file if it already exists.
    """
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(os.path.join(BASE_DIR, f"{fileName}.txt"), "w", encoding="utf-8") as f:
        for element in value:
            f.write(element + "^")


def create_and_write_list(value, fileName):
    """
    Creates a new list file and writes the list to it.
    Raises FileExistsError if the file already exists.
    """
    os.makedirs(BASE_DIR, exist_ok=True)
    try:
        with open(
            os.path.join(BASE_DIR, f"{fileName}.txt"), "x", encoding="utf-8"
        ) as f:
            for element in value:
                f.write(element + "^")
    except FileExistsError:
        print(f'group name: "{fileName}" already used: group exists')


def read_list(fileName):
    """
    Reads the list from memory.
    Returns the file content as a string, or a message if not found.
    """
    try:
        with open(
            os.path.join(BASE_DIR, f"{fileName}.txt"), "r", encoding="utf-8"
        ) as f:
            read = f.read()
        return read
    except FileNotFoundError:
        return "no task files found"


def print_list(tasks, listName):
    """
    input type: list[str], str
    Prints the tasks in the list and saves them to file.
    Each task is printed with its index (starting from 1).
    """
    save_list(tasks, listName)
    for idx, task in enumerate(tasks, 1):
        print(f"{idx}. {task}")


def print_group(groupName):
    """
    input type: str
    Prints all tasks in a group/list by its name.
    If the list is empty or not found, prints an appropriate message.
    """
    print(f"list: {groupName}")
    content = read_list(groupName)
    if content != "no task files found":
        tasks = content.split("^")[:-1]
        if tasks:
            for idx, task in enumerate(tasks, 1):
                print(f"{idx}. {task}")
        else:
            print("EMPTY")
    else:
        print("no task files found")


def append_tem(splitList, at, tasks, activated_List_Name):
    """
    Add a new task to the list if it doesn't already exist and is not empty.
    Prints the updated list after addition or if the task already exists.
    """
    new_task = splitList[at]
    if len(new_task) > 0:
        if new_task not in tasks:
            tasks.append(new_task)
            print_list(tasks, activated_List_Name)
        else:
            print("task already in list")
            print_list(tasks, activated_List_Name)
    else:
        print("can't add empty task")


def put_after(tasks, splitList):
    """
    Move a task after another task by their indices.
    Indices are 1-based in the user prompt.
    """
    try:
        afterFinder = splitList[1].split("after")
        idx_from = int(afterFinder[0]) - 1
        idx_to = int(afterFinder[1])
        popItem = tasks.pop(idx_from)
        tasks.insert(idx_to, popItem)
        return tasks
    except (ValueError, IndexError):
        print("Invalid indices for 'putafter'.")
        return tasks


def put_b4(tasks, splitList):
    """
    Move a task before another task by their indices.
    Indices are 1-based in the user prompt.
    """
    try:
        b4Finder = splitList[1].split("before")
        idx_from = int(b4Finder[0]) - 1
        idx_to = int(b4Finder[1]) - 1
        popItem = tasks.pop(idx_from)
        if idx_from > idx_to:
            tasks.insert(idx_to, popItem)
        else:
            tasks.insert(idx_to - 1, popItem)
    except (ValueError, IndexError):
        print("Invalid indices for 'putb4'.")


def delete_list(splitList):
    """
    Delete a list file after user confirmation.
    Prompts the user to confirm deletion.
    """
    if len(splitList) < 2:
        print("No list specified for deletion.")
        return
    if read_list(splitList[1]) != "no task files found":
        print_group(splitList[1])
        confirmation = input(f"confirm deletion of {splitList[1]}:(yes/no): ")
        if confirmation.lower() == "yes":
            try:
                os.remove(os.path.join(BASE_DIR, f"{splitList[1]}.txt"))
                print(f"Deleted list: {splitList[1]}")
            except Exception as e:
                print(f"Error deleting list: {e}")


def listCreate(listName):
    """
    Create a new empty list file.
    """
    os.makedirs(BASE_DIR, exist_ok=True)
    try:
        with open(
            os.path.join(BASE_DIR, f"{listName}.txt"), "x", encoding="utf-8"
        ) as f:
            pass
    except FileExistsError:
        print(f'list name: "{listName}" already used: list exists')


def arg_error_msg(splitList):
    """Prints an argument error message based on the command and expected number of arguments."""
    print(
        f"ARGUMENT ERROR:\n{splitList[0]} takes {args_counter[splitList[0]]} args -> \nGiven args: {len(splitList)-1}"
    )


args_counter = {
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
activated_List_Name = "main"

if read_list(activated_List_Name) == "no task files found":
    listCreate(activated_List_Name)

tasks = read_list(activated_List_Name).split("^")[:-1]
print_list(tasks, activated_List_Name)
prompt = None

while prompt != "stop":
    tasks = read_list(activated_List_Name).split("^")[:-1]
    print(f"activated: {activated_List_Name}")
    prompt = input("\nprompt: ")

    try:
        splitList = prompt.split("|")

        if splitList[0] not in args_counter:
            print(f"Unknown command: {splitList[0]}")
            continue

        elif splitList[0] in [
            "add",
            "list",
            "pop",
            "remove",
            "delete",
            "call",
            "addmain",
            "create",
        ]:

            if len(splitList) != 2:
                arg_error_msg(splitList)

            else:
                if splitList[0] == "add":  # add|<taskName>
                    append_tem(splitList, 1, tasks, activated_List_Name)

                elif splitList[0] == "list":  # list|<listName>
                    try:
                        print_group(splitList[1])
                    except IndexError:
                        (
                            print_list(tasks, activated_List_Name)
                            if len(tasks) > 0
                            else print("no task listed")
                        )

                elif splitList[0] == "pop":  # pop|<taskno>
                    try:
                        deletedItem = tasks.pop(int(splitList[1]) - 1)
                        print(f"finished {deletedItem}")
                        print_list(tasks, activated_List_Name)
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

                elif splitList[0] == "remove":  # remove|<taskno>
                    try:
                        deletedItem = tasks.pop(int(splitList[1]) - 1)
                        print(f"removed {deletedItem}")
                        print_list(tasks, activated_List_Name)
                        if len(tasks) == 0:
                            print("list empty")
                    except (IndexError, ValueError):
                        print("Invalid task number for remove.")

                elif splitList[0] == "put":  # put|<taskno>(before/after)<taskno>
                    try:
                        if "after" in splitList[1]:
                            tasks = put_after(tasks, splitList)
                        elif "before" in splitList[1]:
                            tasks = put_b4(tasks, splitList)
                        else:
                            print("Specify 'before' or 'after' in put command.")
                        print_list(tasks, activated_List_Name)
                    except Exception as e:
                        print(f"Error in put command: {e}")

                elif splitList[0] == "delete":
                    delete_list(splitList)

                elif splitList[0] == "call":  # call|<listName>
                    with open(
                        os.path.join(BASE_DIR, "activated_List_Name.txt"),
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.write(splitList[1])
                    if read_list(splitList[1]) != "no task files found":
                        activated_List_Name = splitList[1]
                        tasks = read_list(activated_List_Name).split("^")[:-1]
                        print_list(tasks, activated_List_Name)
                    else:
                        print("List does not exist.")

                elif splitList[0] == "addmain":  # addmain|<taskName>
                    main_tasks = read_list("main").split("^")[:-1]
                    append_tem(splitList, 1, main_tasks, "main")

                elif splitList[0] == "create":
                    if len(splitList) > 1:
                        listCreate(splitList[1])
                        print(f"List created by name: {splitList[1]}")
                    else:
                        print("No list name provided for create.")

        elif splitList[0] == "switch":  # switch|<taskno>|<taskno>
            try:
                idx1 = int(splitList[1]) - 1
                idx2 = int(splitList[2]) - 1
                tasks[idx1], tasks[idx2] = tasks[idx2], tasks[idx1]
                print_list(tasks, activated_List_Name)
            except (IndexError, ValueError):
                print("Invalid indices for switch.")

        # FIXME:
        elif splitList[0] == "group":  # group|<taskno>|<taskno>|<taskno>|as <groupname>
            nameFinder = splitList[-1].split("as ")
            if "as" in prompt and len(nameFinder) > 1:
                groupList = []
                d = 1
                tempoList = tasks.copy()
                try:
                    for i in splitList[1:-1]:
                        groupList.append(tempoList[int(i) - 1])
                        tasks.pop(int(i) - d)
                        d += 1
                    create_and_write_list(groupList, nameFinder[-1])
                    print_group(nameFinder[-1])
                    save_list(tasks, activated_List_Name)
                except Exception as e:
                    print(f"Error creating group: {e}")
            else:
                print("no name for group creation")

        elif splitList[0] == "addat":
            # addat|<index>|<taskName>
            main_tasks = read_list(activated_List_Name).split("^")[:-1]
            if len(splitList) >= 3:
                try:
                    index = int(splitList[1]) - 1
                    task_to_add = splitList[2]
                    if len(task_to_add) > 0:
                        if task_to_add not in main_tasks:
                            main_tasks.insert(index, task_to_add)
                            print_list(main_tasks, activated_List_Name)
                            save_list(main_tasks, activated_List_Name)
                        else:
                            print("task already in list")
                            print_list(main_tasks, activated_List_Name)
                    else:
                        print("can't add empty task")
                except (ValueError, IndexError):
                    print("Invalid index for addat.")
            else:
                print("Insufficient arguments for addat.")

        elif splitList[0] == "sort":
            main_tasks = read_list(activated_List_Name).split("^")[:-1]
            try:
                indices = [int(i) - 1 for i in splitList[1:]]
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
                    print_list(main_tasks, activated_List_Name)
                    save_list(main_tasks, activated_List_Name)
            except ValueError:
                print("Invalid indices for sort.")

        elif splitList[0] == "merge":
            if (
                len(splitList) >= 3
                and read_list(splitList[1]) != "no task files found"
                and read_list(splitList[2]) != "no task files found"
            ):
                mergedList = read_list(splitList[1]).split("^")[:-1]
                mergedList.extend(read_list(splitList[2]).split("^")[:-1])
                try:
                    splitList[3]
                    create_and_write_list(mergedList, splitList[3])
                except IndexError:
                    print("The file name was not given")
            else:
                print("please enter correct file names")

        elif splitList[0] == "info":
            print(f"Activated list: {activated_List_Name}")
            print_group(activated_List_Name)

        elif splitList[0] == "help":
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
        if splitList[0] in ["add", "pop", "remove", "switch", "put", "group"]:
            save_list(tasks, activated_List_Name)

    except IndexError as e:
        try:
            (
                print(f"no task found in {splitList[1]}:", e)
                if len(splitList) > 1 and int(splitList[1]) > len(tasks)  # type: ignore
                else print(f"no task found in {splitList[2]}:", e)
            )
        except Exception:
            print(f"no task index specified", e)
    except ValueError as e:
        print("incorrect values", "error: ", e)
    except Exception as e:
        print(f"an error occurred: {e}")
    finally:
        print(splitList)
