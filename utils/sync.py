import os
import shutil
import filecmp


def sync_db_file(network_path, local_path):
    """
    Sync database files from a network path to a local path
    with error handling and file comparison.
    """

    # check if the network source exists
    if not os.path.exists(network_path):
        print(f"network path '{network_path}' is unreachable or file is missing.")
        return False

    try:
        # ensure destination directory exists
        dest_dir = os.path.dirname(local_path)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        # If local file exists check if it is identical to the network source
        if os.path.exists(local_path):
            if filecmp.cmp(network_path, local_path, shallow=False):
                print(f"the file {local_path} is already up to date (no changes needed).")
                return True

        # attempt to copy the file while preserving metadata
        shutil.copy2(network_path, local_path)
        print(f"success updated {local_path} from network.")
        return True

    except PermissionError:
        print(f" permission denied! Check if {local_path} is open in another process.")
    except OSError as e:
        print(f"OS or Network error during synchronization of {local_path}: {e}")
    except Exception as e:
        print(f"Unexpected sync failure for {local_path}: {e}")

    return False