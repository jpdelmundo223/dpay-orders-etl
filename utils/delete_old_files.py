import os
import re

def delete_old_files(src: str, pattern: str, days: int) -> None:
    """
    Deletes files older than n days.

        Parameters:
            src (str): A string source path
            pattern (string): A string pattern
            days (int): Number of days to look up
            
        Returns:
            None
    """
    for _ in os.listdir(src):
        if re.match(pattern, _):
            os.system('forfiles /p {} /m {}*.csv /d -{} /c "cmd /c del /q @file"'.format(src, _[0:7], days))