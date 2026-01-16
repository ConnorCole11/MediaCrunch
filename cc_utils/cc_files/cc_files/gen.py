from pathlib import Path
import shutil
import json


def rename(
    filename: str,
    removables: list[str],
    replacements: list[str],
    iter_max: int = 10,
    all: bool = False
) -> str:
    """
    Rename a string by repeatedly applying replacements to substrings.

    Args:
        filename (str): The original string.
        removables (list[str]): Substrings to remove/replace.
        replacements (list[str]): Corresponding replacements.
        iter_max (int): Maximum number of iterations to apply replacements.
        all (bool): If True, replace all occurrences of each substring.
                    If False, replace only the first occurrence per iteration.

    Returns:
        str: The renamed string.
    """
    for _ in range(iter_max):
        old_filename = filename
        for old, new in zip(removables, replacements):
            if old in filename:
                if all:
                    filename = filename.replace(old, new)
                else:
                    filename = filename.replace(old, new, 1)
        if filename == old_filename:
            break
    return filename

def read_lines(
    txtfile: str,
    line_i: int = 0,
    line_f: int | None = None,
    print_lines: bool = False
) -> list[str] | None:
    """
    Reads lines from a text file, optionally within a line range.

    Args:
        txtfile (str): Path to the text file.
        line_i (int, optional): Starting line index (0-based). Defaults to 0.
        line_f (int | None, optional): Ending line index (exclusive). 
            If None, reads until the end of the file. Defaults to None.
        print_lines (bool, optional): If True, prints lines instead of storing them. Defaults to False.

    Returns:
        list[str] | None: A list of lines if print_lines is False, otherwise None.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(txtfile)
    if not path.is_file():
        raise FileNotFoundError(f"No such file: '{txtfile}'")

    results = [] if not print_lines else None

    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if idx < line_i:
                continue
            if line_f is not None and idx >= line_f:
                break

            if print_lines:
                print(line.rstrip())
            else:
                results.append(line.rstrip())

    return results

def all_names(folder_path: str, extension: str | None = None) -> list[str]:
    """
    Returns a list of all filenames in a folder, optionally filtered by extension.

    Args:
        folder_path (str): Path to the folder.
        extension (str, optional): Only include files ending with this extension (e.g., "mp3").
                                   Defaults to None (include all files).

    Returns:
        list[str]: List of filenames in the folder.
    """
    path = Path(folder_path)
    files = [f.name for f in path.iterdir() if f.is_file()]

    if extension is not None:
        # Normalize extension to start with a dot
        ext = extension if extension.startswith(".") else f".{extension}"
        files = [f for f in files if f.lower().endswith(ext.lower())]

    return files


from pathlib import Path

def all_paths(folder_path: str, extension: str | None = None, abs_path: bool = False) -> list[str]:
    """
    Returns a list of all file paths in a folder, optionally filtered by extension.

    Args:
        folder_path (str): Path to the folder.
        extension (str, optional): Only include files ending with this extension (e.g., "mp3"). Defaults to None.
        abs_path (bool, optional): If True, return absolute paths. Defaults to False.

    Returns:
        list[str]: List of file paths as strings.
    """
    # Use all_names to handle extension filtering
    filenames = all_names(folder_path, extension=extension)
    folder = Path(folder_path)
    
    paths = []
    for filename in filenames:
        filepath = folder / filename
        if abs_path:
            filepath = filepath.resolve()
        paths.append(str(filepath))
    
    return paths


def mv_all(src: str, dst: str, extension: str | None = None) -> None:
    """
    Move all files from src to dst, optionally filtering by extension.

    Args:
        src (str): Source folder path.
        dst (str): Destination folder path.
        extension (str, optional): Only move files ending with this extension. Defaults to None.
    """
    src_path = Path(src)
    dst_path = Path(dst)
    dst_path.mkdir(parents=True, exist_ok=True)  # Ensure destination exists

    for file_path in src_path.iterdir():
        if file_path.is_file():
            if extension is None or file_path.suffix.lower() == f".{extension.lower()}":
                shutil.move(str(file_path), str(dst_path / file_path.name))
    return None


def delete_empty_folders(folder_path: str) -> None:
    """
    Recursively deletes all empty folders inside the given folder.

    Args:
        folder_path (str): Path to the folder to clean up.
    """
    folder = Path(folder_path)

    for subfolder in folder.rglob("*"):
        if subfolder.is_dir() and not any(subfolder.iterdir()):
            subfolder.rmdir()  # Only removes empty directories

    return None

def get_file_size(path: str, human_readable: bool = True) -> str | int:
    """
    Returns the size of a file in bytes or in a human-readable format.

    Args:
        path (str): Path to the file.
        human_readable (bool, optional): If True, returns size in KB/MB/GB etc.
                                         If False, returns size in bytes. Defaults to True.

    Returns:
        str | int: File size as string (human-readable) or int (bytes).

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"No such file: '{path}'")

    size_bytes = file_path.stat().st_size

    if not human_readable:
        return size_bytes

    # Human-readable conversion
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


import re

def make_safe_filename(name: str, replacement: str = "_") -> str:
    """
    Return a filesystem-safe version of a filename by replacing illegal characters.

    Args:
        name (str): Original filename.
        replacement (str, optional): Character to replace illegal characters with. Defaults to "_".

    Returns:
        str: Safe filename.
    """
    # Windows illegal characters: \ / : * ? " < > |
    # On Unix, mostly just /
    illegal_chars_pattern = r'[\\/:*?"<>|]'
    safe_name = re.sub(illegal_chars_pattern, replacement, name)

    # Also strip leading/trailing whitespace
    safe_name = safe_name.strip()

    # Optional: collapse multiple replacements into a single one
    safe_name = re.sub(rf'{re.escape(replacement)}+', replacement, safe_name)

    return safe_name


from pathlib import Path

def increment_name_if_exists(path: str) -> str:
    """
    If the given file path already exists, appends (1), (2), etc. to the filename until a free name is found.

    Args:
        path (str): Original file path.

    Returns:
        str: A file path that does not already exist.
    """
    file_path = Path(path)
    parent = file_path.parent
    stem = file_path.stem  # filename without suffix
    suffix = file_path.suffix  # including the dot, e.g., ".txt"

    counter = 1
    new_path = file_path

    while new_path.exists():
        new_name = f"{stem}({counter}){suffix}"
        new_path = parent / new_name
        counter += 1

    return str(new_path)


def path_to_filename(filepath: str, extension: bool = True) -> str:
    """
    Returns the filename from a path, optionally keeping or removing the extension.

    Args:
        filepath (str): Full path or filename.
        extension (bool, optional): If True, keep the file extension. Defaults to True.

    Returns:
        str: Filename with or without extension.
    """
    path = Path(filepath)
    return path.name if extension else path.stem

def read_json(filepath: str) -> dict:
    """
    Reads a JSON file and returns its contents as a Python dictionary.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict: The parsed JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"No such file: '{filepath}'")
    
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(filepath: str, data: dict, indent: int = 4) -> None:
    """
    Writes a Python dictionary to a JSON file.

    Args:
        filepath (str): Path to the JSON file to write.
        data (dict): Data to write to the JSON file.
        indent (int, optional): Number of spaces for indentation. Defaults to 4.

    Raises:
        TypeError: If the data is not JSON-serializable.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)
    return None