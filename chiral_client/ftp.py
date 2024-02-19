import ftplib
import enum

class PathType(enum.Enum):
    NotExist = 0
    File = 1
    Directory = 2

def exist(ftp: ftplib.FTP, pathname: str) -> PathType:
    if pathname in ftp.nlst():
        return PathType.Directory
    else:
        try:
            ftp.size(pathname)
            return PathType.File
        except Exception:
            return PathType.Directory

# def upload_file(ftp: ftplib.FTP, filename: str, overwrite: bool):
#     try: self.client
