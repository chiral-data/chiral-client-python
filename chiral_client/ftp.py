import ftplib
import enum
import typing
import pathlib

class PathType(enum.Enum):
    NotExist = 0
    File = 1
    Directory = 2

class FtpClient:
    def __init__(self, ftp_addr: str, ftp_port: int, user_email: str, token_api: str, user_id: str):
        self.ftp_addr = ftp_addr
        self.ftp_port = ftp_port
        self.user_email = user_email
        self.token_api = token_api
        self.user_id = user_id
        self.ftp = ftplib.FTP()
        self.root_dir = None

    def connect(self):
        self.ftp.connect(self.ftp_addr, self.ftp_port)
        self.ftp.login(self.user_email, self.token_api)
        self.ftp.cwd(self.user_id)
        self.root_dir = self.ftp.pwd()

    def disconnect(self):
        self.ftp.quit()
        self.root_dir = None

    def cwd_root(self):
        if self.root_dir == None:
            self.connect()
        else:
            try:
                self.ftp.cwd(self.root_dir)
            except Exception:
                print('reconnecting ...')
                self.connect()

    def path_exist(self, pathname: str) -> PathType:
        if not pathname in self.ftp.nlst():
            return PathType.NotExist
        else:
            current_dir = self.ftp.pwd()
            try:
                self.ftp.cwd(pathname)
                self.ftp.cwd(current_dir)
                return PathType.Directory
            except BaseException:
                return PathType.File

    def upload_file(self, local_dir: str, filename: str, overwrite: bool = True):
        path_type = self.path_exist(filename)
        if path_type == PathType.File:
            if overwrite:
                self.ftp.delete(filename)
                with open(pathlib.Path(local_dir).joinpath(filename), 'rb') as file:
                    self.ftp.storbinary(f'STOR {filename}', file)
            else:
                print(f'file {filename} exists in remote server, no overwrite')
        elif pathlib == PathType.Directory:
            print(f'directory with name {filename} exists in remote server')
        else:
            with open(pathlib.Path(local_dir).joinpath(filename), 'rb') as file:
                self.ftp.storbinary(f'STOR {filename}', file)

    def download_file(self, local_dir: str, filename: str):
        with open(pathlib.Path(local_dir).joinpath(filename), 'wb') as file:
            self.ftp.retrbinary(f'RETR {filename}', file.write)

    def remove_dir_all(self, dirname: str):
        parent_dir = self.ftp.pwd()
        self.ftp.cwd(dirname)
        for pathname in self.ftp.nlst():
            if self.path_exist(pathname) == PathType.File:
                self.ftp.delete(pathname)
            else:
                current_dir = self.ftp.pwd()
                self.remove_dir_all(pathname)
                self.ftp.cwd(current_dir)
        self.ftp.cwd(parent_dir)
        self.ftp.rmd(dirname)
