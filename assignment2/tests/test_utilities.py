""" Test script executing all the necessary unit tests for the functions in analytic_tools/utilities.py module
    which is a part of the analytic_tools package
"""

# Include the necessary packages here
from pathlib import Path
import pytest

# This should work if analytic_tools has been installed properly in your environment
from analytic_tools.utilities import (
    get_dest_dir_from_csv_file,
    get_diagnostics,
    is_gas_csv,
    merge_parent_and_basename,
)


@pytest.mark.task12
def test_get_diagnostics(example_config):
    """Test functionality of get_diagnostics in utilities module

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
                                     from Figure 1 in assignment2.md

    Returns:
    None
    """
    
    function = get_diagnostics(example_config)

    expected =  {
        "files": 10,
        "subdirectories": 5,
        ".csv files": 8,
        ".txt files": 0,
        ".npy files": 2,
        ".md files": 0,
        "other files": 0,
    }

    assert function == expected


@pytest.mark.task12
@pytest.mark.parametrize(
    "exception, dir",
    [
        (NotADirectoryError, "/Not_a_real_directory"),
        (NotADirectoryError, "/Not_a_real_directory.csv"),
        (TypeError, 3),
        # add more combinations of (exception, dir) here
    ],
)



def test_get_diagnostics_exceptions(exception, dir):
    """Test the error handling of get_diagnostics function

    Parameters:
        exception (concrete exception): The exception to raise
        dir (str or pathlib.Path): The parameter to pass as 'dir' to the function

    Returns:
        None
    """
    with pytest.raises(exception):
        get_diagnostics(dir)

@pytest.mark.task22
def test_is_gas_csv():
    """Test functionality of is_gas_csv from utilities module

    Parameters:
        None

    Returns:
        None
    """
    # Remove if you implement this task
    function = is_gas_csv('/pollution_data/by_src/src_agriculture/CH4.csv')
    expected = True
    assert function == expected
    
    function2 = is_gas_csv('N4110/ch4.csv')
    expected2 = False
    assert function2 == expected2

    #here = Path(__file__).absolute()
    function3 = is_gas_csv('H2.csv')
    expected3 = True
    assert function3 == expected3




@pytest.mark.task22
@pytest.mark.parametrize(
    "exception, path",
    [
        (ValueError, Path(__file__).parent.absolute()),
        (TypeError, 3),
        # add more combinations of (exception, path) here
    ],
)
def test_is_gas_csv_exceptions(exception, path):
    """Test the error handling of is_gas_csv function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'path' to function

    Returns:
        None
    """

    with pytest.raises(exception):
        is_gas_csv(path)


@pytest.mark.task24
def test_get_dest_dir_from_csv_file(example_config):
    """Test functionality of get_dest_dir_from_csv_file in utilities module.

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
            from Figure 1 in assignment2.md

    Returns:
        None
    """
   
    function = get_dest_dir_from_csv_file(example_config, example_config/'pollution_data'/'by_src'/'src_agriculture'/'H2.csv')  
    expected = example_config/'gas_H2'
    assert function == expected


@pytest.mark.task24
@pytest.mark.parametrize(
    "exception, dest_parent, file_path",
    [
        (ValueError, Path(__file__).parent.absolute(), "foo.txt"),
        (ValueError, Path(__file__).parent.absolute(), '/dirc'),
        (NotADirectoryError, Path(__file__).parent.absolute()/"foo.txt", Path(__file__).parent.absolute()),
        (TypeError, 5, 3),
        # add more combinations of (exception, dest_parent, file_path) here
    ],

)
def test_get_dest_dir_from_csv_file_exceptions(exception, dest_parent, file_path):
    """Test the error handling of get_dest_dir_from_csv_file function

    Parameters:
        exception (concrete exception): The exception to raise
        dest_parent (str or pathlib.Path): The parameter to pass as 'dest_parent' to the function
        file_path (str or pathlib.Path): The parameter to pass as 'file_path' to the function

    Returns:
        None
    """
    with pytest.raises(exception):
        get_dest_dir_from_csv_file(dest_parent, file_path)


@pytest.mark.task26
def test_merge_parent_and_basename():
    """Test functionality of merge_parent_and_basename from utilities module

    Parameters:
        None

    Returns:
        None
    """
    function = merge_parent_and_basename('assignment2/pollution_data/by_src/src_agriculture/CH4.csv')
    expected = 'src_agriculture_CH4.csv'
    assert function == expected


@pytest.mark.task26
@pytest.mark.parametrize(
    "exception, path",
    [
        (TypeError, 33),
        (ValueError, '/src_agriculture/'),
        (ValueError, 'CH4.csv/'),
        # add more combinations of (exception, path) here
    ],
)
def test_merge_parent_and_basename_exceptions(exception, path):
    """Test the error handling of merge_parent_and_basename function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'pass' to the function

    Returns:
        None
    """
    with pytest.raises(exception):
        merge_parent_and_basename(path)

