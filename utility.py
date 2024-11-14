import os, shutil

def rm_directory(dir_path):
    """Empties all contents of the specified directory.

    Args:
    dir_path (str): Path to the directory to empty.
    """
    # Check if the directory exists
    if not os.path.exists(dir_path):
        print(f"Directory not found: {dir_path}")
        return

    # Iterate over each item in the directory
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)  # Remove files and links
                print(f"Removed file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove directories
                print(f"Removed directory: {item_path}")
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")

    os.rmdir(dir_path)