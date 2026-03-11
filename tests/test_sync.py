import os
import shutil
import filecmp

from unittest.mock import patch
from utils.sync import sync_db_file


@patch('os.path.exists')
def test_network_path_missing(mock_exists):
    mock_exists.return_value = False
    result = sync_db_file(r'C:\missing\file.mmdb', 'local.mmdb')
    assert result is False
    print("\nhandled missing network path correctly.")


@patch('shutil.copy2')
@patch('filecmp.cmp')
@patch('os.path.exists')
def test_files_already_identical(mock_exists, mock_cmp, mock_copy):
    mock_exists.return_value = True  # File exists
    mock_cmp.return_value = True  # Files are identical
    result = sync_db_file('source.mmdb', 'dest.mmdb')
    assert result is True
    mock_copy.assert_not_called()
    print("\n skipped copy when files are identical.")


@patch('shutil.copy2')
@patch('os.path.exists')
@patch('os.makedirs')
def test_success_copy(mock_makedirs, mock_exists, mock_copy):
    mock_exists.side_effect = [True, False]
    result = sync_db_file('source.mmdb', 'dest.mmdb')
    assert result is True
    mock_copy.assert_called_once()
    print("\n success sync and copy.")



@patch('shutil.copy2')
@patch('os.path.exists')
def test_permission_error(mock_exists, mock_copy):
    mock_exists.side_effect = [True, False]  # Source exists, dest doesn't
    mock_copy.side_effect = PermissionError("access denied")

    # We expect the function to catch the error and return False instead of crashing
    result = sync_db_file('source.mmdb', 'dest.mmdb')

    assert result is False
    print("\n handled permission error.")



@patch('os.path.getsize')
@patch('os.path.exists')
def test_empty_source_file(mock_exists, mock_getsize):
    mock_exists.return_value = True
    mock_getsize.return_value = 0  # Empty file
    result = sync_db_file('source.mmdb', 'dest.mmdb')
    assert result is False
    print("\n rejected empty source file.")


@patch('shutil.copy2')
@patch('os.path.exists')
def test_io_error_during_copy(mock_exists, mock_copy):
    mock_exists.side_effect = [True, False]
    mock_copy.side_effect = IOError("network disconnected")
    result = sync_db_file('source.mmdb', 'dest.mmdb')
    assert result is False
    print("\n handled IO error (network drop) during copy.")