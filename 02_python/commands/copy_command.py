from .base_command import BaseCommand
import os
import shutil
from typing import List

class CopyCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize the CopyCommand object.

        Args:
            options (List[str]): List of command options.
            args (List[str]): List of command arguments.
        """
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'Copy a file or directory to another location'
        self.usage = 'Usage: cp [source] [destination]'

        # TODO 6-1: Initialize any additional attributes you may need.
        # Refer to list_command.py, grep_command.py to implement this.
        # ...
        
        self.name = 'cp'
        self.options = options

        if (len(self.args) == 2):
            self.source_dir = self.args[0]
            self.dest_dir = self.args[1]

    def execute(self) -> None:
        """
        Execute the copy command.
        Supported options:
            -i: Prompt the user before overwriting an existing file.
            -v: Enable verbose mode (print detailed information)
        
        TODO 6-2: Implement the functionality to copy a file or directory to another location.
        You may need to handle exceptions and print relevant error messages.
        You may use the file_exists() method to check if the destination file already exists.
        """
        
        file_name = self.source_dir.split(sep="\\")
        check_exists = self.file_exists(self.dest_dir, file_name[-1])
        
        try:
            
            if '-v' in self.options:
                print(f"cp: copying '{self.source_dir}' to '{self.dest_dir}'")
                
            
            if '-i' in self.options and check_exists:
                
                answer = input(f"cp: overwrite '{os.path.join(self.dest_dir, self.source_dir)}'? (y/n) ")
                
                if (answer.lower() == 'y'):
                    os.remove(os.path.join(self.current_path, self.dest_dir, self.source_dir))
                    shutil.copy2(os.path.join(self.current_path, self.source_dir), os.path.join(self.current_path, self.dest_dir))
                    return
                else: 
                    return
            
            shutil.copy2(os.path.join(self.current_path, self.source_dir), os.path.join(self.current_path, self.dest_dir))
        
        except Exception as e:
            return
        
    def file_exists(self, directory: str, file_name: str) -> bool:
        """
        Check if a file exists in a directory.
        Feel free to use this method in your execute() method.

        Args:
            directory (str): The directory to check.
            file_name (str): The name of the file.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        file_path = os.path.join(directory, file_name)
        return os.path.exists(file_path)
