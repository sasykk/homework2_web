import os
import re
import shutil
from pathlib import Path


class Cleaner:

    def __init__(self, path_to_clean):
        self.image_files = list()
        self.video_files = list()
        self.document_files = list()
        self.music_files = list()
        self.archives = list()
        self.folders = list()
        self.others = list()
        self.unknown = set()
        self.extensions = set()
        self.path_to_clean = path_to_clean

        self.registered_extensions = {
            'JPEG': self.image_files,
            'PNG': self.image_files,
            'JPG': self.image_files,
            'SVG': self.image_files,
            'AVI': self.video_files,
            'MP4': self.video_files,
            'MOV': self.video_files,
            'MKV': self.video_files,
            'DOC': self.document_files,
            'DOCX': self.document_files,
            'TXT': self.document_files,
            'PDF': self.document_files,
            'XLS': self.document_files,
            'XLSX': self.document_files,
            'PPTX': self.document_files,
            'MP3': self.music_files,
            'OGG': self.music_files,
            'WAW': self.music_files,
            'AMR': self.music_files,
            'ZIP': self.archives,
            'GZ': self.archives,
            'TAR': self.archives
        }

        self.UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
        self.TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y","i",
                       "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
                       "u", "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

        self.TRANS = {}

        for key, value in zip(self.UKRAINIAN_SYMBOLS, self.TRANSLATION):
            self.TRANS[ord(key)] = value
            self.TRANS[ord(key.upper())] = value.upper()

    def normalize(self, name: str) -> str:
        name, *extension = name.split('.')
        new_name = name.translate(self.TRANS)
        new_name = re.sub(r'\W', '_', new_name)
        if not extension:
            return new_name
        return f"{new_name}.{'.'.join(extension)}"

    def get_extensions(self, file_name):
        return Path(file_name).suffix[1:].upper()

    def scan(self, folder):
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('images', 'video', 'audio', 'documents', 'archives', 'other'):
                    self.folders.append(item)
                    self.scan(item)
                continue

            extension = self.get_extensions(file_name=item.name)
            new_name = folder/item.name
            if not extension:
                self.others.append(new_name)
            else:
                try:
                    container = self.registered_extensions[extension]
                    self.extensions.add(extension)
                    container.append(new_name)
                except KeyError:
                    self.unknown.add(extension)
                    self.others.append(new_name)

    def handle_file(self, path, root_folder, dist):
        target_folder = root_folder/dist
        target_folder.mkdir(exist_ok=True)
        path.replace(target_folder/self.normalize(path.name))

    def handle_archive(self, path, root_folder, dist):
        target_folder = root_folder / dist
        target_folder.mkdir(exist_ok=True)
        new_name = path.name
        for i in ['.zip', '.tar.gz', '.tar']:
            new_name = self.normalize(new_name.replace(i, ''))

        archive_folder = target_folder / new_name
        archive_folder.mkdir(exist_ok=True)

        try:
            shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
        except shutil.ReadError:
            archive_folder.rmdir()
            os.remove(str(path.resolve()))
            return
        except FileNotFoundError:
            archive_folder.rmdir()
            return
        path.unlink()

    def remove_empty_folders(self, path):
        for item in path.iterdir():
            if item.is_dir():
                self.remove_empty_folders(item)
                try:
                    item.rmdir()
                except OSError:
                    pass

    def clean(self):
        folder_path = Path(self.path_to_clean)
        print(folder_path)
        self.scan(folder_path)

        items = {'images': self.image_files,
                 'video': self.video_files,
                 'audio': self.music_files,
                 'documents': self.document_files,
                 'other': self.others}

        for key, val in items.items():
            for file in items[key]:
                self.handle_file(file, folder_path, key)

        for file in self.archives:
            self.handle_archive(file, folder_path, "archives")

        self.remove_empty_folders(folder_path)

    def print_result(self, folder):
        for item in folder.iterdir():
            # print(item.name)
            if item.is_dir():
                self.print_result(item)
            continue
