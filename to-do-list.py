from os import remove as osremove


# remove Python form file path b4 extraction to make it independent
# put all elifs in try: see exception handling proficiently
def listSave(value, fileName):  # saves and write the list to memory
    with open(f"Python/to-do-list/lists/{fileName}.txt", "w") as f:
        for element in value:
            f.write(element + "^")


def listX(value, fileName):  # saves the list to memory
    try:
        with open(f"Python/to-do-list/lists/{fileName}.txt", "x") as f:
            for element in value:
                f.write(element + "^")
    except FileExistsError:
        print(f'group name: "{fileName}" already used: group exists')


def listRead(fileName):  # reads the list from memory
    try:
        with open(f"Python/to-do-list/lists/{fileName}.txt", "r") as f:
            read = f.read()
        return read
    except FileNotFoundError:
        return "no task files found"


def printList(
    tasks, listName
):  # prints the list in the terminal and saves it to memory
    listSave(tasks, listName)
    for idx, task in enumerate(tasks, 1):
        print(f"{idx}. {task}")


def printGroup(groupName):
    print(f"list: {groupName}")
    if listRead(groupName) != "no task files found":
        sl = 1
        lenTest = []
        for i in listRead(groupName).split("^")[:-1]:
            lenTest.append(print(f"{sl}. {i}"))
            sl += 1
        if len(lenTest) < 1:
            print("EMPTY")
    else:
        print("no task files found")


# at = location of the task being added in the prompt
def appendItem(splitList, at, list, activated_List_Name):
    if len(splitList[at]) > 0:
        if splitList[at] not in list:
            list.append(splitList[at])
            printList(list, activated_List_Name)
        else:
            print("task already in list")
            printList(list, activated_List_Name)
    else:
        print("can't add empty task")


def putafter(tasks, splitList):
    """Moves a task after another task by their indices."""
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
    """Moves a task before another task by their indices."""
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
    if listRead(splitList[1]) != "no task files found":
        confirmation = input(
            f"""{printGroup(splitList[1])}\nconfirm deletion of {splitList[1]}:(yes/no): """
        )
        if confirmation == "yes":
            osremove(f"Python/to-do-list/lists/{splitList[1]}.txt")
    else:
        print("file not found")


def listCreate(listName):
    listX([], listName)


activated_List_Name: str = "main"
tasks: list = listRead(activated_List_Name).split("^")[:-1]
printList(tasks, activated_List_Name)
prompt = None
while prompt != "stop":
    tasks = listRead(activated_List_Name).split("^")[:-1]
    print(f"activated: {activated_List_Name}")
    prompt = input("\npromt: ")
    try:
        splitList = prompt.split("|")

        if splitList[0] == "add":  # add|<taskName>
            appendItem(splitList, 1, tasks, activated_List_Name)

        elif splitList[0] == "list":  # list|<listName>
            try:
                splitList[1]
                printGroup(splitList[1])
            except IndexError:
                (
                    printList(tasks, activated_List_Name)
                    if len(tasks) > 0
                    else print("no task listed")
                )

        elif splitList[0] == "pop":  # pop|<taskno>
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

        elif splitList[0] == "remove":  # remove|<taskno>
            deletedItem = tasks.pop(int(splitList[1]) - 1)
            print(f"removed {deletedItem}")
            printList(tasks, activated_List_Name)
            if len(tasks) == 0:
                print("list empty")

        elif splitList[0] == "switch":  # switch|<taskno>|<taskno>
            tasks[int(splitList[1]) - 1], tasks[int(splitList[2]) - 1] = (
                tasks[int(splitList[2]) - 1],
                tasks[int(splitList[1]) - 1],
            )
            printList(tasks, activated_List_Name)

        elif splitList[0] == "put":  # put|<taskno>(before/after)<taskno>
            try:
                putafter(tasks, splitList)
                printList(tasks, activated_List_Name)
            except:
                putb4(tasks, splitList)
                printList(tasks, activated_List_Name)

        elif splitList[0] == "group":  # group|<taskno>|<taskno>|<taskno>|as <groupname>
            nameFinder = splitList[-1].split("as ")
            if "as" in prompt:
                groupList = []
                d = 1
                tempoList = tasks.copy()
                for i in splitList[1:-1]:
                    groupList.append(tempoList[int(i) - 1])
                    tasks.pop(int(i) - d)
                    d += 1
                listX(groupList, nameFinder[-1])
                printGroup(nameFinder[-1])
                listSave(tasks, activated_List_Name)
            else:
                print("no name for group creation")

        elif splitList[0] == "call":  # call|<listName>
            if len(splitList) == 2:
                with open("Python/to-do-list/lists/activated_List_Name.txt", "w") as f:
                    f.write(splitList[1])
                if printGroup(splitList[1]) != "no task files found":
                    activated_List_Name = splitList[1]
            else:
                print("syntax length error")

        elif splitList[0] == "addmain":  # addmain|<taskName>
            list = listRead("main").split("^")[:-1]
            if len(splitList[1]) > 0:
                if splitList[1] not in list:
                    list.append(splitList[1])
                    printList(list, "main")
                else:
                    print("task already in main")
                    printList(list, "main")
            else:
                print("can't add empty task")

        elif splitList[0] == "addat":  # addat|3|code   not completed
            appendItem(splitList, 2, list, activated_List_Name)

        elif splitList[0] == "sort":
            listCopy = [tasks[int(i) - 1] for i in splitList[1:]]
            listValueCopy = tasks.copy()
            for i in splitList[1:]:
                tasks.remove(listValueCopy[int(i) - 1])
            listCopy.extend(tasks)
            tasks = listCopy
            printList(tasks, activated_List_Name)

        elif splitList[0] == "delete":
            deleteList(splitList)

        elif splitList[0] == "merge":
            if (
                listRead(splitList[1]) != "no task files found"
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
            listCreate(splitList[1])
            print(f"List created by name: {splitList[1]}")

        elif prompt == "stop":
            break

        else:
            print("function not recognised")

    except IndexError as e:
        try:
            (
                print(f"no task found in {splitList[1]}:", e)
                if int(splitList[1]) > len(tasks)
                else print(f"no task found in {splitList[2]}:", e)
            )
        except:
            print(f"no task index specified", e)
    except ValueError as e:
        print("incorrect values", "error: ", e)
    except Exception as e:
        print(f"an error occured: {e}")
    finally:
        print(splitList)
