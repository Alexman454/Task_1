import os
import tarfile
import csv
from datetime import datetime

class VirtualFileSystem:
    def __init__(self, tar_path, log_path):
        self.current_path = "/"
        self.fs_root = "./vfs_root"
        self.log_path = log_path
        self._extract_tar(tar_path)
        self._log_action("VFS initialized")

    def _extract_tar(self, tar_path):
        if not os.path.exists(self.fs_root):
            os.mkdir(self.fs_root)
        with tarfile.open(tar_path, "r") as tar:
            tar.extractall(self.fs_root)

    def _log_action(self, action):
        with open(self.log_path, "a", newline="") as csvfile:
            log_writer = csv.writer(csvfile)
            log_writer.writerow([datetime.now().isoformat(), action])

    def change_directory(self, path):
        new_path = os.path.normpath(os.path.join(self.fs_root, self.current_path.strip("/"), path))
        if os.path.isdir(new_path):
            self.current_path = os.path.relpath(new_path, self.fs_root)
            self._log_action(f"cd {path}")
        else:
            raise FileNotFoundError("No such directory")

    def list_directory(self):
        dir_path = os.path.join(self.fs_root, self.current_path.strip("/"))
        if not os.path.exists(dir_path):
            raise FileNotFoundError("Current directory does not exist")
        contents = os.listdir(dir_path)
        self._log_action("ls")
        return contents

    def read_file(self, filename):
        file_path = os.path.join(self.fs_root, self.current_path.strip("/"), filename)
        if not os.path.isfile(file_path):
            raise FileNotFoundError("No such file")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.readlines()
        except UnicodeDecodeError:
            with open(file_path, "rb") as file:
                raw_content = file.readlines()
            return [line.decode("utf-8", errors="replace") for line in raw_content]
