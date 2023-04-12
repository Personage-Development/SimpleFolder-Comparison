import os
import filecmp
import hashlib
from collections import defaultdict
from tkinter import Tk, filedialog

# Function to open folder dialog
def choose_folder():
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path

# Function that computes the SHA-1 hash of a file for comparison
def hash_file(filepath):
    with open(filepath, 'rb') as file:
        file_hash = hashlib.sha1(file.read()).hexdigest()
    return file_hash

# Function to recursively collect file information (hashes, relative paths, and file paths) from a folder
def get_files_recursive(folder):
    file_data = defaultdict(list)
    for root, dirs, files in os.walk(folder):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = hash_file(filepath)
            relative_path = os.path.relpath(root, folder)
            file_data[file_hash].append((relative_path, filepath))
    return file_data

# Function to compare two folders and return the common folders and common files
def compare_folders(folder1, folder2):
    folder1_files = get_files_recursive(folder1)
    folder2_files = get_files_recursive(folder2)

    common_folders = set()
    common_files = set()
    for file_hash, folder1_data in folder1_files.items():
        folder2_data = folder2_files.get(file_hash, [])
        if folder2_data:
            for relpath1, filepath1 in folder1_data:
                for relpath2, filepath2 in folder2_data:
                    # Check if relative paths are equal and not the main directories
                    if relpath1 == relpath2 and relpath1 != '.':
                        common_folders.add((os.path.join(folder1, relpath1), os.path.join(folder2, relpath2)))
                    common_files.add((filepath1, filepath2))
    return common_folders, common_files

def main():
    print("Choose the first folder:")
    folder1 = choose_folder()
    print(f"First folder: {folder1}")

    print("Choose the second folder:")
    folder2 = choose_folder()
    print(f"Second folder: {folder2}")

    # Compares the folders and returns the common folders and common files
    common_folders, common_files = compare_folders(folder1, folder2)
    
    # Prints out the folders that are in common
    if common_folders:
        print("\nCommon Folders:")
        for folder1_path, folder2_path in common_folders:
            print(f"{folder1_path}")
            print(f"{folder2_path}\n")
    else:
        print("There are no common folders with the same content.")
    
    # Prints out the files that are common
    if common_files:
        print("\nCommon Files:")
        for file1_path, file2_path in common_files:
            print(f"{file1_path}")
            print(f"{file2_path}\n")
    else:
        print("There are no common files.")

if __name__ == "__main__":
    main()
