"""
Utility functions for reading files.
"""

def read_file(file_path) -> str:
    """
    Read a file and return its content.
    Will be used for reading corpus files.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f'File {file_path} not found.')
        return ""


def read_lines(file_path) -> list:
    """
    Read a file and return its lines.
    Will be used for reading dictionary files.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f'File {file_path} not found.')
        return []
