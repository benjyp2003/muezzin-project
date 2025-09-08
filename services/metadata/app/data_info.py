import datetime
from pathlib import Path
import mimetypes


class DataInfo:
    def __init__(self, folder_path):
        self.folder_path = folder_path


    def initialize_file_info_dict(self, file_path: str) -> dict:
        """Initialize a dict/json that will contain the files path and meta data"""
        try:
            metadata_dict = {"path": "",
                             "metadata": {}}

            path = self.get_path(file_path)
            metadata_dict["path"] = str(path.resolve())
            metadata_dict["metadata"]["file_name"] = path.name
            size = self.get_size_in_bytes(path)
            metadata_dict["metadata"]["size_in_bytes"] = size
            metadata_dict["metadata"]["size_in_mb"] = size / 1000000   # divide the size by a million to get the size in mb
            metadata_dict["metadata"]["type"] = self.get_file_type(path)
            metadata_dict["metadata"]["media_type"] = self.get_file_media_type(path)
            metadata_dict["metadata"]["creation_date"] = self.get_creation_date(path)
            metadata_dict["metadata"]["last_modified_date"] = self.last_modified(path)

            return metadata_dict
        except FileNotFoundError:
            print("The file does not exist.")
        except Exception as e:
            raise Exception(f"Error during json metadata initializing: {e}")


    def get_path(self, file_name):
        return Path(self.folder_path) / file_name

    @staticmethod
    def get_size_in_bytes(path: Path):
        return path.stat().st_size

    @staticmethod
    def get_file_type(path: Path):
        return path.suffix

    @staticmethod
    def get_file_media_type(path):
        """Returns the media type of the file for example audio/wav"""
        mime_type, encoding = mimetypes.guess_type(path)
        return mime_type

    @staticmethod
    def get_creation_date(path):
        # Access the st_ctime attribute for the creation timestamp
        creation_timestamp = path.stat().st_ctime
        # Convert the timestamp to a human-readable datetime object with miliseconds
        return datetime.datetime.fromtimestamp(creation_timestamp).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def last_modified(path):
        mod_time_timestamp = path.stat().st_mtime
        mod_time = datetime.datetime.fromtimestamp(mod_time_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        return mod_time



