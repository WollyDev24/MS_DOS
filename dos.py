import os
import shutil
import time
import random

# ===== CONFIG =====
# Get the directory of the script file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the virtual drive path relative to the script directory
BASEDIR_NAME = "VIRTUAL_DRIVE"
BASEDIR = os.path.join(SCRIPT_DIR, BASEDIR_NAME)
TRASH = os.path.join(BASEDIR, "$TRASH")
PROMPT = " > "
VERSION = "DOS-E 1.0"
COMPUTERNAME = "MY-PC"
OSNAME = "MSDOS E"
OWNER = "User"

# ===== RESERVED NAMES =====
RESERVED = [
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "LPT1",
    "LPT2",
    "LPT3",
]

# Global variable to track the current virtual directory
current_virtual_dir = BASEDIR


def init_virtual_drive():
    """Initializes the virtual drive structure."""
    if not os.path.exists(BASEDIR):
        os.makedirs(BASEDIR, exist_ok=True)
        os.makedirs(TRASH, exist_ok=True)
        files_dir = os.path.join(BASEDIR, "FILES")
        os.makedirs(files_dir, exist_ok=True)
        readme_path = os.path.join(files_dir, "README.TXT")
        with open(readme_path, "w") as f:
            f.write(
                "Note: this isnt emulating anything, just simulating. this .py "
                "uses only VIRTUAL_DRIVE, doesnt touch your main drive\n"
            )
        print("Note: Virtual drive initialized.")


def get_full_path(path):
    """Converts a relative virtual path to an absolute system path."""
    global current_virtual_dir
    if not path:
        return current_virtual_dir
    # Join the current virtual directory with the path
    full_path = os.path.join(current_virtual_dir, path)
    # Normalize the path to handle '..' and '.'
    return os.path.normpath(full_path)


def is_inside_base_dir(path):
    """Checks if the given path is a subpath of BASEDIR."""
    # os.path.commonpath will return the longest common path
    # If the common path is not the BASEDIR, it means the path escapes the virtual drive.
    return os.path.commonpath([BASEDIR, path]) == BASEDIR


# ===== COMMAND HANDLERS =====


def cmd_help(args):
    """Display available commands."""
    print("\nAvailable commands:")
    print("  DIR [path]        - List directory contents")
    print("  CD [path]         - Change directory")
    print("  MD|MKDIR name     - Create directory")
    print("  RD|RMDIR name     - Remove directory (empty only)")
    print("  TYPE file         - Display text file")
    print("  COPY src dst      - Copy file")
    print("  DEL|ERASE file    - Move file to trash")
    print("  REN|RENAME a b    - Rename file/folder")
    print("  CLS               - Clear screen")
    print("  DATE              - Show date (simulated)")
    print("  TIME              - Show time (simulated)")
    print("  VER               - Show version")
    print("  PROMPT text       - Set command prompt")
    print("  SYSINFO           - Show system info")
    print("  TRASH             - List trash contents")
    print("  CLEARTRASH        - Empty trash")
    print("  CALC              - Mini calculator")
    print("  NOTEPAD <file>    - Open text file (uses real notepad)")
    print("  GAME              - Play mini game (Guess the number)")
    print("  EXIT              - Quit emulator")


def cmd_dir(args):
    """List directory contents."""
    global current_virtual_dir
    if not args:
        target_path = current_virtual_dir
    else:
        target_path = get_full_path(args[0])

    if not os.path.exists(target_path) or not is_inside_base_dir(target_path):
        print(f"Path not found: {args[0] if args else ''}")
        return

    try:
        contents = os.listdir(target_path)
        if not contents:
            print("Directory empty.")
            return

        # Print the directory name at the top
        print(f"\nDirectory of {os.path.relpath(target_path, BASEDIR_NAME)}:\n")

        # Simulate DOS-like DIR output (no file sizes/timestamps for simplicity)
        for item in contents:
            full_item_path = os.path.join(target_path, item)
            if os.path.isdir(full_item_path):
                print(f"  <DIR>    {item}")
            else:
                print(f"           {item}")
    except Exception as e:
        print(f"Error listing directory: {e}")


def cmd_cd(args):
    """Change current virtual directory."""
    global current_virtual_dir
    if not args:
        # Show current directory
        # Display as a relative path from the script's root for a clean look
        print(os.path.relpath(current_virtual_dir, SCRIPT_DIR))
        return

    target_path = get_full_path(args[0])

    if os.path.isdir(target_path) and is_inside_base_dir(target_path):
        current_virtual_dir = target_path
    else:
        print(f"Path not found or access denied: {args[0]}")


def cmd_md(args):
    """Create directory (MD/MKDIR)."""
    if not args:
        print("Syntax: MD folder")
        return

    dir_name = args[0]
    # Check reserved names (case-insensitive)
    if dir_name.upper() in RESERVED:
        print(f"Cannot create reserved name: {dir_name}")
        return

    target_path = get_full_path(dir_name)

    if os.path.exists(target_path):
        print(f"Folder already exists: {dir_name}")
        return

    try:
        os.mkdir(target_path)
        print(f"Directory created: {dir_name}")
    except Exception:
        print("Could not create directory.")


def cmd_rd(args):
    """Remove directory (RD/RMDIR)."""
    if not args:
        print("Syntax: RD folder")
        return

    dir_name = args[0]
    target_path = get_full_path(dir_name)

    if os.path.isdir(target_path) and is_inside_base_dir(target_path):
        try:
            # os.rmdir only removes empty directories, simulating RD/RMDIR behavior
            os.rmdir(target_path)
            print(f"Directory removed: {dir_name}")
        except OSError:
            print("Could not remove (maybe not empty).")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Folder not found: {dir_name}")


def cmd_type(args):
    """Display text file contents."""
    if not args:
        print("Syntax: TYPE file")
        return

    file_name = args[0]
    target_path = get_full_path(file_name)

    if os.path.isfile(target_path) and is_inside_base_dir(target_path):
        try:
            with open(target_path, "r") as f:
                print(f.read())
        except Exception:
            print("Error reading file.")
    else:
        print(f"File not found: {file_name}")


def cmd_copy(args):
    """Copy file."""
    if len(args) < 2:
        print("Syntax: COPY source destination")
        return

    src_name = args[0]
    dst_name = args[1]
    src_path = get_full_path(src_name)
    dst_path = get_full_path(dst_name)

    if os.path.exists(src_path) and is_inside_base_dir(src_path):
        try:
            shutil.copy2(src_path, dst_path)  # copy2 attempts to preserve metadata
            print("File copied.")
        except Exception as e:
            print(f"Copy failed: {e}")
    else:
        print(f"Source file not found: {src_name}")


def cmd_del(args):
    """Move file to trash (DEL/ERASE)."""
    if not args:
        print("Syntax: DEL file")
        return

    file_name = args[0]
    target_path = get_full_path(file_name)

    if os.path.isfile(target_path) and is_inside_base_dir(target_path):
        try:
            if not os.path.exists(TRASH):
                os.makedirs(TRASH, exist_ok=True)

            # Move file to trash. Renaming to avoid simple conflicts.
            trash_path = os.path.join(TRASH, f"{file_name}_{int(time.time())}")
            shutil.move(target_path, trash_path)
            print("File moved to trash.")
        except Exception as e:
            print(f"Error moving to trash: {e}")
    else:
        print(f"File not found: {file_name}")


def cmd_ren(args):
    """Rename file/folder."""
    if len(args) < 2:
        print("Syntax: REN old_name new_name")
        return

    old_name = args[0]
    new_name = args[1]
    old_path = get_full_path(old_name)
    new_path = get_full_path(new_name)

    if os.path.exists(old_path) and is_inside_base_dir(old_path):
        # Prevent reserved names (case-insensitive)
        if new_name.upper() in RESERVED:
            print(f"Cannot rename to reserved name: {new_name}")
            return
        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {old_name} -> {new_name}")
        except Exception:
            print("Rename failed.")
    else:
        print(f"File not found: {old_name}")


def cmd_date(args):
    """Show date (simulated)."""
    print(f"Current date (simulated): {time.strftime('%Y-%m-%d')}")


def cmd_time(args):
    """Show time (simulated)."""
    print(f"Current time (simulated): {time.strftime('%H:%M:%S')}")


def cmd_ver(args):
    """Show version."""
    print(VERSION)


def cmd_prompt(args):
    """Set command prompt."""
    global PROMPT
    if not args:
        print(f"Current prompt: {PROMPT.strip()}")
        return

    # Use the rest of the arguments joined by space as the new prompt
    PROMPT = " ".join(args) + " "
    print(f"Prompt set to: {PROMPT.strip()}")


def cmd_sysinfo(args):
    """Show system info."""
    global current_virtual_dir
    print(f"Computer Name: {COMPUTERNAME}")
    print(f"OS: {OSNAME}")
    print(f"Version: {VERSION}")
    print(f"Directory: {os.path.relpath(current_virtual_dir, BASEDIR)}")


def cmd_trash(args):
    """List trash contents."""
    print("Trash contents:")
    if os.path.exists(TRASH):
        contents = os.listdir(TRASH)
        if contents:
            for item in contents:
                print(f"  {item}")
        else:
            print("Trash is empty.")
    else:
        print("Trash is empty.")


def cmd_cleartrash(args):
    """Empty trash."""
    if os.path.exists(TRASH):
        try:
            # Delete all contents inside the trash folder
            for item in os.listdir(TRASH):
                item_path = os.path.join(TRASH, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            print("Trash emptied.")
        except Exception as e:
            print(f"Error emptying trash: {e}")
    else:
        print("Trash folder not found.")


def cmd_calc(args):
    """Mini calculator."""
    print("Mini Calculator (type 'exit' to leave)")
    while True:
        try:
            expr = input("> ")
            if expr.lower() == "exit":
                break

            try:
                code = compile(expr, "<string>", "eval")
                if any(name in code.co_names for name in ('__import__', 'eval', 'exec', 'open')):
                    print("Unsafe expression")
                    continue
                
                result = eval(expr)
                print(f"Result: {result}")
            except SyntaxError:
                print("Invalid expression")
            except NameError:
                print("Invalid expression (name error)")
            except ZeroDivisionError:
                print("Error: Division by zero")
            except Exception:
                print("Invalid expression")

        except EOFError:
            break


def cmd_notepad(args):
    """Open text file with system's notepad."""
    if not args:
        print("Syntax: NOTEPAD filename")
        return

    file_name = args[0]
    target_path = get_full_path(file_name)

    try:
        # Use subprocess or os.startfile for Windows to open Notepad
        os.startfile(target_path, "open")
    except Exception as e:
        print(f"Could not open Notepad for file: {e}")


def cmd_game(args):
    """Play mini number guessing game."""
    target = random.randint(1, 100)
    print("Guess a number between 1 and 100. Type 'exit' to quit.")
    while True:
        try:
            guess = input("GUESS> ")
            if guess.lower() == "exit":
                break

            try:
                guess_num = int(guess)
            except ValueError:
                print("Please enter a valid number or 'exit'.")
                continue

            if guess_num < target:
                print("Too low!")
            elif guess_num > target:
                print("Too high!")
            else:
                print(f"Congratulations! You guessed the number {target}!")
                break
        except EOFError:
            break


# Dictionary to map command names (case-insensitive) to handler functions
COMMANDS = {
    "cls": lambda a: os.system("cls" if os.name == "nt" else "clear"),
    "exit": lambda a: print("Goodbye!") and quit(),
    "help": cmd_help,
    "dir": cmd_dir,
    "cd": cmd_cd,
    "md": cmd_md,
    "mkdir": cmd_md,
    "rd": cmd_rd,
    "rmdir": cmd_rd,
    "type": cmd_type,
    "copy": cmd_copy,
    "del": cmd_del,
    "erase": cmd_del,
    "ren": cmd_ren,
    "rename": cmd_ren,
    "date": cmd_date,
    "time": cmd_time,
    "ver": cmd_ver,
    "prompt": cmd_prompt,
    "sysinfo": cmd_sysinfo,
    "trash": cmd_trash,
    "cleartrash": cmd_cleartrash,
    "calc": cmd_calc,
    "notepad": cmd_notepad,
    "game": cmd_game,
}


def main():
    """Main loop for the simulated DOS-E environment."""
    global PROMPT

    # Set terminal title (Windows only) and color (simulated)
    if os.name == "nt":
        os.system(f"title {OSNAME} - {VERSION}")
        os.system("color 0a") # Green on black

    init_virtual_drive()

    # Initial display
    print(f"{OSNAME} [Version {VERSION}]")
    print(f"(C) 2025 {OWNER}. All rights reserved.")
    print('Type "help" for a list of commands.')
    print()

    while True:
        try:
            # Display current path in the prompt (simulating C:\> or similar)
            prompt_text = os.path.relpath(current_virtual_dir, BASEDIR)
            if prompt_text == ".": # If at the root of BASEDIR
                prompt_text = BASEDIR_NAME
            
            # Use the set PROMPT variable with the path prefix
            user_input = input(f"{prompt_text}{PROMPT}")

            if not user_input.strip():
                continue

            # Split command and arguments
            parts = user_input.split(maxsplit=1)
            cmd = parts[0].lower()
            args = parts[1].split() if len(parts) > 1 else []

            # Execute command
            if cmd in COMMANDS:
                COMMANDS[cmd](args)
            else:
                print(f"Unknown command: {cmd}")

        except EOFError:
            # Handle Ctrl+Z/Ctrl+D exit
            print("Goodbye!")
            break
        except KeyboardInterrupt:
            # Handle Ctrl+C
            print("\n")
            continue
        except Exception as e:
            # Catch unexpected errors gracefully
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()