from .base_command import BaseCommand
import os
import shutil
from typing import List

class MoveCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize the MoveCommand object.

        Args:
            options (List[str]): List of command options.
            args (List[str]): List of command arguments.
        """
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'Move a file or directory to another location'
        self.usage = 'Usage: mv [source] [destination]'

        # TODO 5-1: Initialize any additional attributes you may need.
        # Refer to list_command.py, grep_command.py to implement this.
        # ...
        
        self.name = 'mv'
        self.options = options

        if (len(self.args) == 2):
            self.source_dir = self.args[0]
            self.dest_dir = self.args[1]

    def execute(self) -> None:
        """
        Execute the move command.
        Supported options:
            -i: Prompt the user before overwriting an existing file.
            -v: Enable verbose mode (print detailed information)
        
        TODO 5-2: Implement the functionality to move a file or directory to another location.
        You may need to handle exceptions and print relevant error messages.
        """
        
        file_name = self.source_dir.split(sep="\\")
        check_exists = self.file_exists(self.dest_dir, file_name[-1])
        
        try:
            
            if '-v' in self.options:
                print(f"mv: moving '{self.source_dir}' to '{self.dest_dir}'")

            if '-i' in self.options and check_exists:
                
                answer = input(f"mv: overwrite '{os.path.join(self.dest_dir, self.source_dir)}'? (y/n) ")
                
                if (answer.lower() == 'y'):
                    os.remove(os.path.join(self.current_path, self.dest_dir, self.source_dir))
                    shutil.move(os.path.join(self.current_path, self.source_dir), os.path.join(self.current_path, self.dest_dir))
                    return
                else: 
                    return
            
            if '-i' not in self.options and check_exists:
                print(f"mv: cannot move '{self.source_dir}' to '{self.dest_dir}': Destination path '{os.path.join(self.dest_dir, self.source_dir)}' already exists")
                return
            
            shutil.move(os.path.join(self.current_path, self.source_dir), os.path.join(self.current_path, self.dest_dir))
        
        except Exception as e :
            print(f"mv: cannot move '{self.source_dir}' to '{self.dest_dir}': Destination path '{os.path.join(self.dest_dir, self.source_dir)}' already exists")
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
