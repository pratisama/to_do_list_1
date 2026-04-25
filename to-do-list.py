import os

# Use os.path.join for cross-platform file paths
BASE_DIR = os.path.join("Python", "to-do-list", "lists")


def listSave(value, fileName):
    """
    Saves and writes the list to memory.
    Each element is written to a file, separated by '^'.
    Overwrites the file if it already exists.
    """
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(os.path.join(BASE_DIR, f"{fileName}.txt"), "w", encoding="utf-8") as f:
        for element in value:
            f.write(element + "^")


def listX(value, fileName):
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


def listRead(fileName):
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


def printList(tasks, listName):
    """
    Prints the tasks in the list and saves them to file.
    Each task is printed with its index (starting from 1).
    """
    listSave(tasks, listName)
    for idx, task in enumerate(tasks, 1):
        print(f"{idx}. {task}")


def printGroup(groupName):
    """
    Prints all tasks in a group/list by name.
    If the list is empty or not found, prints an appropriate message.
    """
    print(f"list: {groupName}")
    content = listRead(groupName)
    if content != "no task files found":
        tasks = content.split("^")[:-1]
        if tasks:
            for idx, task in enumerate(tasks, 1):
                print(f"{idx}. {task}")
        else:
            print("EMPTY")
    else:
        print("no task files found")


def appendItem(splitList, at, tasks, activated_List_Name):
    """
    Add a new task to the list if it doesn't already exist and is not empty.
    Prints the updated list after addition or if the task already exists.
    """
    new_task = splitList[at]
    if len(new_task) > 0:
        if new_task not in tasks:
            tasks.append(new_task)
            printList(tasks, activated_List_Name)
        else:
            print("task already in list")
            printList(tasks, activated_List_Name)
    else:
        print("can't add empty task")


def putafter(tasks, splitList):
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


def putb4(tasks, splitList):
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


def deleteList(splitList):
    """
    Delete a list file after user confirmation.
    Prompts the user to confirm deletion.
    """
    if len(splitList) < 2:
        print("No list specified for deletion.")
        return
    if listRead(splitList[1]) != "no task files found":
        printGroup(splitList[1])
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


activated_List_Name = "main"

if listRead(activated_List_Name) == "no task files found":
    listCreate(activated_List_Name)

tasks = listRead(activated_List_Name).split("^")[:-1]
printList(tasks, activated_List_Name)
prompt = None

while prompt != "stop":
    tasks = listRead(activated_List_Name).split("^")[:-1]
    print(f"activated: {activated_List_Name}")
    prompt = input("\nprompt: ")
    try:
        splitList = prompt.split("|")

        if (
            splitList[0] == "add"
        ):  # add|<taskName> TODO:apply if len cond for first four together
            (
                appendItem(splitList, 1, tasks, activated_List_Name)
                if len(splitList) == 1
                else print(
                    f"add takes one args -> task name\nGiven args: {len(splitList)-1}"
                )
            )

        elif splitList[0] == "list":  # list|<listName>
            try:
                printGroup(splitList[1])
            except IndexError:
                (
                    printList(tasks, activated_List_Name)
                    if len(tasks) > 0
                    else print("no task listed")
                )

        elif splitList[0] == "pop":  # pop|<taskno>
            try:
                deletedItem = tasks.pop(int(splitList[1]) - 1)
                print(f"finished {deletedItem}")
                printList(tasks, activated_List_Name)
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
                printList(tasks, activated_List_Name)
                if len(tasks) == 0:
                    print("list empty")
            except (IndexError, ValueError):
                print("Invalid task number for remove.")

        elif splitList[0] == "switch":  # switch|<taskno>|<taskno>
            try:
                idx1 = int(splitList[1]) - 1
                idx2 = int(splitList[2]) - 1
                tasks[idx1], tasks[idx2] = tasks[idx2], tasks[idx1]
                printList(tasks, activated_List_Name)
            except (IndexError, ValueError):
                print("Invalid indices for switch.")

        elif splitList[0] == "put":  # put|<taskno>(before/after)<taskno>
            try:
                if "after" in splitList[1]:
                    putafter(tasks, splitList)
                elif "before" in splitList[1]:
                    putb4(tasks, splitList)
                else:
                    print("Specify 'before' or 'after' in put command.")
                printList(tasks, activated_List_Name)
            except Exception as e:
                print(f"Error in put command: {e}")

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
                    listX(groupList, nameFinder[-1])
                    printGroup(nameFinder[-1])
                    listSave(tasks, activated_List_Name)
                except Exception as e:
                    print(f"Error creating group: {e}")
            else:
                print("no name for group creation")

        elif splitList[0] == "call":  # call|<listName>
            if len(splitList) == 2:
                with open(
                    os.path.join(BASE_DIR, "activated_List_Name.txt"),
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(splitList[1])
                if listRead(splitList[1]) != "no task files found":
                    activated_List_Name = splitList[1]
                    tasks = listRead(activated_List_Name).split("^")[:-1]
                    printList(tasks, activated_List_Name)
                else:
                    print("List does not exist.")
            else:
                print("syntax length error")

        elif splitList[0] == "addmain":  # addmain|<taskName>
            appendItem(splitList, 1, tasks, "main")

        elif splitList[0] == "addat":
            # addat|<index>|<taskName>
            main_tasks = listRead(activated_List_Name).split("^")[:-1]
            if len(splitList) >= 3:
                try:
                    index = int(splitList[1]) - 1
                    task_to_add = splitList[2]
                    if len(task_to_add) > 0:
                        if task_to_add not in main_tasks:
                            main_tasks.insert(index, task_to_add)
                            printList(main_tasks, activated_List_Name)
                            listSave(main_tasks, activated_List_Name)
                        else:
                            print("task already in list")
                            printList(main_tasks, activated_List_Name)
                    else:
                        print("can't add empty task")
                except (ValueError, IndexError):
                    print("Invalid index for addat.")
            else:
                print("Insufficient arguments for addat.")

        elif splitList[0] == "sort":
            main_tasks = listRead(activated_List_Name).split("^")[:-1]
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
                    printList(main_tasks, activated_List_Name)
                    listSave(main_tasks, activated_List_Name)
            except ValueError:
                print("Invalid indices for sort.")

        elif splitList[0] == "delete":
            deleteList(splitList)

        elif splitList[0] == "merge":
            if (
                len(splitList) >= 3
                and listRead(splitList[1]) != "no task files found"
                and listRead(splitList[2]) != "no task files found"
            ):
                mergedList = listRead(splitList[1]).split("^")[:-1]
                mergedList.extend(listRead(splitList[2]).split("^")[:-1])
                try:
                    splitList[3]
                    listX(mergedList, splitList[3])
                except IndexError:
                    print("The file name was not given")
            else:
                print("please enter correct file names")

        elif splitList[0] == "create":
            if len(splitList) > 1:
                listCreate(splitList[1])
                print(f"List created by name: {splitList[1]}")
            else:
                print("No list name provided for create.")

        elif prompt == "stop":
            break

        else:
            print("function not recognised")

        # Save changes to the current list after each command that modifies it
        if splitList[0] in ["add", "pop", "remove", "switch", "put", "group"]:
            listSave(tasks, activated_List_Name)

    except IndexError as e:
        try:
            (
                print(f"no task found in {splitList[1]}:", e)
                if len(splitList) > 1 and int(splitList[1]) > len(tasks)
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
