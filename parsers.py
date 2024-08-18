"""
filename: parsers.py
Date: 04/09/2024
"""


class FileNotFound(Exception):
    '''
    Exception raised when a file is not found.
    '''
    def __init__(self, filename):
        super().__init__(f"The file {filename} was not found.")

class LineFormatError(Exception):
    '''
    Exception raised when a line in the .lrc file does not match the expected format.
    '''
    def __init__(self, line):
        super().__init__(f"Error in line format: {line}")

def read_lrc(filename):
    """
    Reads a lyrical file (.lrc) and supports multiple formats.
    :param filename (string): Name of the lrc file to read.
    :return (string): Song lyrics as a single string.
    """

    # Read the file contents and extract the lyrics
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            contents = f.read()
    except FileNotFoundError:
        raise FileNotFound(filename)

    song = []

    # Split the contents by newline characters
    for line in contents.split("\n"):
        if ']' in line:  # Check if the line contains a timestamp ending
            try:
                lyric = line.split(']', 1)[1].strip() # Extract the lyric part
                if lyric:
                    song.append(lyric)
            except IndexError:
                raise LineFormatError(line)
        # Skip empty lines and lines that contain only timestamps
        elif line.startswith('[') and ':' not in line:
            continue

    # Return the song lyrics as a single string
    return '\n'.join(song)