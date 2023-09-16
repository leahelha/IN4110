"""Module containing functions used to achieve the desired restructuring of the pollution_data directory
"""
# Include the necessary packages here
from pathlib import Path
from typing import Dict, List


def get_diagnostics(dir: str | Path) -> Dict[str, int]:
    """Get diagnostics for the directory tree, with root directory pointed to by dir.
       Counts up all the files, subdirectories, and specifically .csv, .txt, .npy, .md and other files in the whole directory tree.

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest

    Returns:
        res (Dict[str, int]) : a dictionary of the findings with following keys: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    """

    # Dictionary to return
    res = {
        "files": 0,
        "subdirectories": 0,
        ".csv files": 0,
        ".txt files": 0,
        ".npy files": 0,
        ".md files": 0,
        "other files": 0,
    }

    
    
    # Remember error handling
    if not isinstance(dir, (str, Path)):
        raise TypeError('Object is not path. Expected a string or a Path.')
    
    directory = Path(dir)

    if not directory.exists():
        raise NotADirectoryError(f'The path "{directory}" does not exist.')

    if not directory.is_dir():
        raise NotADirectoryError(f' "{directory}" is not a directory')

    
    # Count folders and total num. of files using this function
    def counter(directory):
        
        # Traverse the directory and find its contents
        contents = directory.iterdir() 
        
        for path in contents:

            #If the item in contents is a file, then sort the type
            if path.is_file():
                res["files"] +=1
                suffi = path.suffix.lower()
                suffix = f'{suffi} files'

                if suffix in res:

                    res[suffix] += 1
                else:
                    res["other files"] += 1

            #If the item in contents is a subdirectory, then count it and run counter on the subdirectory
            elif path.is_dir():
                res["subdirectories"] += 1
                counter(path)
        
        return 

    count = counter(directory)

    return res

def display_diagnostics(dir: str | Path, contents: Dict[str, int]) -> None:
    """Display diagnostics for the directory tree, with root directory pointed to by dir.
        Objects to display: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    Parameters:
        dir (str or pathlib.Path) : Absolute path the directory of interest
        contents (Dict[str, int]) : a dictionary of the same type as return type of get_diagnostics, has the form:

            .. highlight:: python
            .. code-block:: python

                {
                    "files": 0,
                    "subdirectories": 0,
                    ".csv files": 0,
                    ".txt files": 0,
                    ".npy files": 0,
                    ".md files": 0,
                    "other files": 0,
                }

    Returns:
        None
    """
     # Remember error handling
    if not isinstance(dir, (str, Path)):
        raise TypeError('Object is not path. Expected a string or a Path.')
    
    if not isinstance(contents, (dict)):
        raise TypeError('Object is not a dictionary. Expected a dictionary.')
    
    path = Path(dir)

    if not path.exists():
        raise NotADirectoryError(f'The path "{path}" does not exist.')

    if not path.is_dir():
        raise NotADirectoryError(f' "{path}" is not a directory')

    print('------------------------------------------------------------------------')
    print(f'Diagnostics for: {path} \n')
    print('------------------------------------------------------------------------')
    
    # Print the summary to the terminal
    for key, value in contents.items():
        print(f'Number of {key}: {value}')

    print('------------------------------------------------------------------------')
    return

def display_directory_tree(dir: str | Path, maxfiles: int = 3) -> None:
    """Display a directory tree, with root directory pointed to by dir.
       Limit the number of files to be displayed for convenience to maxfiles.
       This tree is built with inspiration from the code written by "Flimm" at https://stackoverflow.com/questions/6639394/what-is-the-python-way-to-walk-a-directory-tree

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest
        maxfiles (int) : Maximum number of files to be displayed at each level in the tree, default to three.

    Returns:
        None

    """


    #ERROR HANDLING
    if not isinstance(dir, (str, Path)):
        raise TypeError(f'Object is not path. Expected a string or a Path.')
    
    if not isinstance(maxfiles, (int)):
        raise TypeError('The second parameter, maxfiles, needs to be an integer.')
    
    if not maxfiles>1:
        raise ValueError('The second parameter, maxfiles, cannot be smaller than 1.')
    
    directory = Path(dir)


    if not directory.exists():
        raise NotADirectoryError(f'The path "{path}" does not exist.')

    if not directory.is_dir():
        raise NotADirectoryError(f' "{path}" is not a directory')

    
    print('\n')
    print(f"{directory}/")

    # Recursive function which traverses the directory and makes a tree structure of the directory
    def directory_tree(directory, counter = 0):
        contents = directory.iterdir()
        nr_files = 0

        for path in contents:
            
            if path.is_file() and nr_files==(maxfiles) and counter>0:
                nr_files += 1
                print(f"{'    '*counter}...")

            if path.is_file() and nr_files<=maxfiles:
                nr_files += 1
                print(f"{'    '*counter}- {path.name}")   

            elif path.is_dir():
                print(f"{'    '*counter}> {path.name}")  
                count = counter
                
                directory_tree(path, count+1)

    directory_tree = directory_tree(directory)
    return

def is_gas_csv(path: str | Path) -> bool:
    """Checks if a csv file pointed to by path is an original gas statistics file.
        An original file must be called '[gas_formula].csv' where [gas_formula] is
        in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
         - path (str of pathlib.Path) : Absolute path to .csv file that will be checked

    Returns
         - (bool) : Truth value of whether the file is an original gas file
    """
    # Do correct error handling first
    if not isinstance(path, (Path, str)):
        raise TypeError(f'Object "{path}" is not path. Expected a string or a Path.')
    
    directory = Path(path)

    if not directory.name.endswith('.csv'):
        raise ValueError('The path does not lead to a .csv file.')
    
    # Extract the filename from the .csv file and check if it is a valid greenhouse gas
    file = str(directory.name)
    filename = file[:-4]

    # List of greenhouse gasses, correct filenames in front of a .csv ending
    gasses = ["CO2", "CH4", "N2O", "SF6", "H2"]

    if filename in gasses:
        return True
    else:
        return False

def get_dest_dir_from_csv_file(dest_parent: str | Path, file_path: str | Path) -> Path:
    """Given a file pointed to by file_path, derive the correct gas_[gas_formula] directory name.
        Checks if a directory "gas_[gas_formula]", exists and if not, it creates one as a subdirectory under dest_parent.

        The file pointed to by file_path must be a valid file. A valid file must be called '[gas_formula].csv' where [gas_formula]
        is in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
        - dest_parent (str or pathlib.Path) : Absolute path to parent directory where gas_[gas_formula] should/will exist
        - file_path (str or pathlib.Path) : Absolute path to file that gas_[gas_formula] directory will be derived from

    Returns:
        - (pathlib.Path) : Absolute path to the derived directory

    """

    # Do correct error handling first
    if not (isinstance(dest_parent, (Path, str)) and isinstance(file_path, (Path, str))):
        raise TypeError(f'Object "{dest_parent}" or "{file_path}" is not path. Expected a string or a Path.')
    
    file_path = Path(file_path)

    if not dest_parent.is_dir() or not dest_parent.exists():
       raise NotADirectoryError(f'Directory {dest_parent} does not exist, or is not the path to a directory.')

    if not file_path.is_file():
        raise ValueError(f'The path {file_path} does not lead to a file.')

    allowed_list = ['CO2.csv', 'CH4.csv', 'N2O.csv', 'SF6.csv', 'H2.csv']

    if file_path.name not in allowed_list:
        raise ValueError(f'The path {file_path} does not lead to an origianl .csv file.')

    # If the input file is valid:

    filename = str(file_path.name)

    # Derive the name of the directory, pattern: gas_[gas_formula] directory
    dest_name = filename[:-4]
    

    parent = Path(dest_parent)
   
    # Derive its absolute path
    dest_path = parent/f'gas_{dest_name}'

    # Check if the directory already exists, and create one of not
    if dest_path.exists():
        return dest_path
    if not dest_path.exists():
        dest_path.mkdir()
        return dest_path

def merge_parent_and_basename(path: str | Path) -> str:
    """This function merges the basename and the parent-name of a path into one, uniting them with "_" character.
       It then returns the basename of the resulting path.

    Parameters:
        - path (str or pathlib.Path) : Absolute path to modify

    Returns:
        - new_base (str) : New basename of the path
    """

    if not isinstance(path, (Path, str)):
        raise TypeError(f'Object "{path}" is not path. Expected a string or a Path.')
    
    path = Path(path)
    
    #see if there is a better way to do this ***
    contents = list(path.parts)

    if len(contents)<3:
        raise ValueError('Expected a filename and a parent-name.')
    

    filename = path.name
    parentname = path.parent.name
    # New, merged, basename of the path, which will be the new filename
    new_base = f'{parentname}_{filename}'
    return new_base

def delete_directories(path_list: List[str | Path]) -> None:
    """Prompt the user for permission and delete the objects pointed to by the paths in path_list if
       permission is given. If the object is a directory, its whole directory tree is removed.

    Parameters:
        - path_list (List[str | Path]) : a list of absolute paths to all the objects to be removed.


    Returns:
    None
    """
    # note: This is an optional task, no points assigned. If you are skipping it, remove `raise NotImplementedError` in the function body
    
