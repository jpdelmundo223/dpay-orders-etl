import shutil
import os

def move_files(src: str, dst: str) -> None:
    """
    Move files from one directory to another.

        Parameters:
            src (str): A string source path
            dst (dst): A string destination path

        Returns:
            None
    """
    for filename in os.listdir(src):
        if "txnlist" in filename:
            source = "{}\{}".format(src, filename)
            destination = "{}\{}".format(dst, filename)
            shutil.move(source, destination)
        
def copy_files(src: str, dst: str) -> None:
    """
    Copy files from source to destination.

        Parameters:
            src (str): A string source path
            dst (dst): A string destination path
            
        Returns:
            None
    """
    for filename in os.listdir(src):
        if "txnlist" in filename:
            source = "{}\{}".format(src, filename)
            destination = "{}\{}".format(dst, filename)
            shutil.copy(source, destination)