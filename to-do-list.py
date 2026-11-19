import pathlib as pl

BASE_DIR = pl.Path(__file__).parent / "lists"


def error_msg(msg: str):
    """Prints an error message."""
    print(f"ERROR: {msg}")


def ensure_base_dir():
    """
    Ensures that the base directory for storing lists exists. If it doesn't, it creates it.
    """
    BASE_DIR.mkdir(parents=True, exist_ok=True)


def _list_path(list_name: str) -> pl.Path:
    """
    Return the full .txt path for a given list name (private).
    """
    return BASE_DIR / f"{list_name}.txt"


def create_empty_list(list_name: str) -> bool:
    """
    Create a new empty list file.\n
    Arguments: list name.\n
    Returns: True if successful and False otherwise.
    Prints errors if path exists.
    """
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    path = _list_path(list_name)

    try:
        path.touch(exist_ok=False)
        print(f"List created: {list_name}")
        return True
    except FileExistsError:
        print(f'List "{list_name}" already exists.')
        return False
    except OSError as e:
        print(f"Error creating list: {e}")
        return False


def write_list(tasks: list[str], list_name: str) -> bool:
    """
    Writes the list to a list file.\n
    Arguments: task list and list name.\n
    Returns: True if written successfully.\n
    Each task is separated by '^'.\n
    Overwrites the file if it already exists. Creates new if it doesn't.
    """
    ensure_base_dir()
    try:
        with open(_list_path(list_name), "w", encoding="utf-8") as f:
            for element in tasks:
                f.write(element + "^")
            return True
    except OSError:
        return False


def create_and_write_list(tasks: list[str], list_name: str) -> bool:
    """
    Creates a new list file and writes the list to it.\n
    Arguments: task list and list name.\n
    Returns: True if written successfully, False otherwise.\n
    Each task is separated by '^'.\n
    Raises FileExistsError if the file already exists.
    """
    ensure_base_dir()

    try:
        with open(_list_path(list_name), "x", encoding="utf-8") as f:
            for task in tasks:
                f.write(task + "^")
        return True
    except FileExistsError:
        error_msg(f'List "{list_name}" already exists.')
        return False


def read_list(list_name: str) -> str:
    """
    Reads the list from memory.\n
    Arguments: list name.\n
    Returns: the string containing tasks in the list, seperated by "^".\n
    Returns: "no task files found" if FileNotFoundError occurs.
    """
    try:
        with open(_list_path(list_name), "r", encoding="utf-8") as f:
            read = f.read()
        return read
    except FileNotFoundError:
        return "no task files found"


def print_list(tasks: list[str]) -> None:
    """Prints tasks supplied as a list."""
    for idx, task in enumerate(tasks, 1):
        print(f"{idx}. {task}")


def save_and_print_list(tasks: list[str], list_name: str) -> bool:
    """
    Saves the tasks in the list file and prints them.\n
    Each task is printed with its index (starting from sl no. 1).\n
    Arguments: task list and list name.\n
    Returns: True if saved and printed, False if not saved.\n
    """
    if not write_list(tasks, list_name):
        return False
    print_list(tasks)
    return True


def read_and_print_list(list_name: str) -> bool:
    """
    Prints all tasks in a saved list.\n
    If the list is empty or not found, prints an appropriate message.\n
    Arguments: list name.\n
    Returns: True if list is found in memory, False otherwise.
    """
    content = read_list(list_name)

    if content == "no task files found":
        print("no task files found")
        return False

    print(f"list: {list_name}")
    tasks = content.split("^")[:-1]

    if not tasks:
        print("EMPTY")
    else:
        print_list(tasks)
    return True


def add_new_task(new_task: str, tasks: list[str], list_name: str) -> bool:
    """
    Adds a new non-empty task to the list if it doesn't already exist in it.\n
    Arguments: new non-empty task, task list, and list name.\n
    Returns: False if empty task or save faliure, None if task already in list, True otherwise.\n
    Saves and prints the final list if task is added.
    """
    if not new_task:
        print("can't add empty task")
        return False
    if new_task in tasks:
        print("task already in list")
        return False
    tasks.append(new_task)
    if not save_and_print_list(tasks, list_name):
        tasks.pop()
        return False
    return True


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
        tasks.insert(idx_to - 1, pop_item)
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
        return tasks
    except (ValueError, IndexError):
        print("Invalid indices for 'putb4'.")
        return tasks


def delete_list(list_name: str) -> bool:  # type: ignore
    """
    Delete a list file after user confirmation.
    Prompts the user to confirm deletion
    Arguments: current name and new name of the list(in order).\n
    Returns: True if successful and False otherwise.
    Prints errors if path exists.
    """
    path = _list_path(list_name)

    if not path.exists():
        print("List does not exist.")
        return False

    read_and_print_list(list_name)
    confirmation = input(f"Confirm deletion of {list_name} (yes/no): ").strip().lower()

    if confirmation != "yes":
        print("Deletion cancelled.")
        return False
    try:
        path.unlink()
        print(f"Deleted list: {list_name}")
        return True
    except OSError as e:
        print(f"Error deleting list: {e}")
        return False


def rename_list(old_name: str, new_name: str) -> bool:
    """
    Rename an existing list file to a new name.\n
    Arguments: current name and new name of the list(in order).\n
    Returns: True if successful and False otherwise.
    Prints errors if path exists.
    """
    old_path = _list_path(old_name)
    new_path = _list_path(new_name)

    if not old_path.is_file():
        print(f'Cannot rename: List "{old_name}" does not exist.')
        return False
    if new_path.is_file():
        print(f"Cannot rename: A list with the name {new_name} already exists.")
        return False

    try:
        old_path.rename(new_path)
    except OSError as e:
        error_msg(f"Could not rename list: {e}")
        return False

    print(f'Renamed list from "{old_name}" to "{new_name}"')
    return True


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
    "rename": 2,
    "sort": "variable",
    "group": "variable",
}


activated_list_name = "main"

if read_list(activated_list_name) == "no task files found":
    create_empty_list(activated_list_name)

tasks = read_list(activated_list_name).split("^")[:-1]
save_and_print_list(tasks, activated_list_name)
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
                    add_new_task(split_list[1], tasks, activated_list_name)

                elif split_list[0] == "list":  # list|<listname>
                    try:
                        read_and_print_list(split_list[1])
                    except IndexError:
                        (
                            save_and_print_list(tasks, activated_list_name)
                            if len(tasks) > 0
                            else print("no task listed")
                        )

                elif split_list[0] == "pop":  # pop|<taskno>
                    try:
                        deleted_item = tasks.pop(int(split_list[1]) - 1)
                        print(f"finished {deleted_item}")
                        save_and_print_list(tasks, activated_list_name)
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
                        save_and_print_list(tasks, activated_list_name)
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
                        save_and_print_list(tasks, activated_list_name)
                    except Exception as e:
                        print(f"Error in put command: {e}")

                elif split_list[0] == "delete":
                    delete_list(split_list[1])

                elif split_list[0] == "call":  # call|<list name>
                    with open(
                        _list_path("activated_List_Name"),
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.write(split_list[1])
                    if read_list(split_list[1]) != "no task files found":
                        activated_list_name = split_list[1]
                        tasks = read_list(activated_list_name).split("^")[:-1]
                        save_and_print_list(tasks, activated_list_name)
                    else:
                        print("List does not exist.")

                elif split_list[0] == "addmain":  # addmain|<taskName>
                    main_tasks = read_list("main").split("^")[:-1]
                    add_new_task(split_list[1], main_tasks, "main")

                elif split_list[0] == "create":
                    if len(split_list) > 1:
                        create_empty_list(split_list[1])
                        print(f"List created by name: {split_list[1]}")
                    else:
                        print("No list name provided for create.")

        elif split_list[0] == "switch":  # switch|<taskno>|<taskno>
            try:
                idx1 = int(split_list[1]) - 1
                idx2 = int(split_list[2]) - 1
                tasks[idx1], tasks[idx2] = tasks[idx2], tasks[idx1]
                save_and_print_list(tasks, activated_list_name)
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
                    read_and_print_list(name_finder[-1])
                    write_list(tasks, activated_list_name)
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
                            save_and_print_list(main_tasks, activated_list_name)
                            write_list(main_tasks, activated_list_name)
                        else:
                            print("task already in list")
                            save_and_print_list(main_tasks, activated_list_name)
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
                    save_and_print_list(main_tasks, activated_list_name)
                    write_list(main_tasks, activated_list_name)
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
            if rename_list(split_list[1], split_list[2]):
                print("List renamed successfully")
            else:
                print("List rename aborted")

        elif split_list[0] == "info":
            print(f"Activated list: {activated_list_name}")
            read_and_print_list(activated_list_name)

        elif split_list[0] == "help":
            print("""Available commands:
 - add | <taskname>
 - list | <listname>
 - pop | <taskno>
 - remove | <taskno>
 - switch | <taskno> | <taskno>
 - put | <taskno> before/after <taskno>
 - group | <taskno> as <groupname>
 - call | <listname>
 - create | <listname>
 - addat | <index> | <taskname>
 - addmain | <taskname>
 - sort | <taskno> <taskno> ...
 - delete | <listname>
 - merge | <list1> | <list2> | <newlist>
 - rename | <oldlist> | <newlist>
 - info
 - help
 - stop
Note: Commands are case-sensitive and should be entered in the specified format.
        Don't use spaces around '|' in commands.""")

        elif prompt == "stop":
            break

        # Save changes to the current list after each command that modifies it
        if split_list[0] in ["add", "pop", "remove", "switch", "put", "group"]:
            write_list(tasks, activated_list_name)

    except IndexError as e:
        try:
            (
                print(f"no task found in {split_list[1]}:", e)  # type: ignore
                if len(split_list) > 1 and int(split_list[1]) > len(tasks)  # type: ignore
                else print(f"no task found in {split_list[2]}:", e)  # type: ignore
            )
        except Exception:
            print(f"no task index specified", e)

    except ValueError as e:
        print(f"Unexpected values;\nError: {e}")
    except Exception as e:
        print(f"an error occurred: {e}")
