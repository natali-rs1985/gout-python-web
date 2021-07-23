import time
import sys
import os.path
from pathlib import Path
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
import threading

IMAGES = ['JPEG', 'PNG', 'JPG']
VIDEO = ['AVI', 'MP4', 'MOV']
DOCUMENTS = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'XLSX']
MUSIC = ['MP3', 'OGG', 'WAV', 'AMR']
ARCHIVES = ['ZIP', 'GZ', 'TAR']
FILE_DICT = {'IMAGES': 'images',
             'VIDEO': 'video',
             'DOCUMENTS': 'documents',
             'MUSIC': 'music',
             'ARCHIVES': 'archives'}

images_list = []
video_list = []
documents_list = []
music_list = []
archives_list = []
another = []

extensions = set()
unknown_extensions = set()


def normalize(string):
    dictionary = {
        ord('а'): 'a',
        ord('б'): 'b',
        ord('в'): 'v',
        ord('г'): 'g',
        ord('д'): 'd',
        ord('е'): 'e',
        ord('ё'): 'yo',
        ord('ж'): 'zh',
        ord('з'): 'z',
        ord('и'): 'i',
        ord('й'): 'y',
        ord('к'): 'k',
        ord('л'): 'l',
        ord('м'): 'm',
        ord('н'): 'n',
        ord('о'): 'o',
        ord('п'): 'p',
        ord('р'): 'r',
        ord('с'): 's',
        ord('т'): 't',
        ord('у'): 'u',
        ord('ф'): 'f',
        ord('х'): 'h',
        ord('ц'): 'ts',
        ord('ч'): 'ch',
        ord('ш'): 'sh',
        ord('щ'): 'shch',
        ord('ъ'): 'y',
        ord('ы'): 'y',
        ord('ь'): '',
        ord('э'): 'e',
        ord('ю'): 'yu',
        ord('я'): 'ya',

        ord('А'): 'A',
        ord('Б'): 'B',
        ord('В'): 'V',
        ord('Г'): 'G',
        ord('Д'): 'D',
        ord('Е'): 'Ye',
        ord('Ё'): 'Yo',
        ord('Ж'): 'Zh',
        ord('З'): 'Z',
        ord('И'): 'I',
        ord('Й'): 'Y',
        ord('К'): 'K',
        ord('Л'): 'L',
        ord('М'): 'M',
        ord('Н'): 'N',
        ord('О'): 'O',
        ord('П'): 'P',
        ord('Р'): 'R',
        ord('С'): 'S',
        ord('Т'): 'T',
        ord('У'): 'Yu',
        ord('Ф'): 'F',
        ord('Х'): 'H',
        ord('Ц'): 'Ts',
        ord('Ч'): 'Ch',
        ord('Ш'): 'Sh',
        ord('Щ'): 'Shch',
        ord('Ъ'): 'Y',
        ord('Ы'): 'Y',
        ord('Ь'): '',
        ord('Э'): 'E',
        ord('Ю'): 'Yu',
        ord('Я'): 'Ya',
    }
    transliterate_string = string.translate(dictionary)
    normalized_string = re.sub('[\W]', '_', transliterate_string)
    return normalized_string


def find_files(in_path):
    files = []
    if in_path.exists():
        for file in in_path.iterdir():
            if file.is_file():
                files.append(file)
            else:
                files.extend(find_files(file))

    return files


def find_dirs(in_path):
    if in_path.exists():
        files = len(find_files(in_path))
        object_list = in_path.iterdir()
        if object_list:
            for obj in object_list:
                if obj.is_dir():
                    find_dirs(obj)
        if files == 0:
            in_path.rmdir()


def get_file_attrs(fl):
    new_fl = fl[::-1]
    fl_ext, fl_nm = new_fl.split('.', maxsplit=1)
    return fl_nm[::-1], fl_ext[::-1]


def check_dir(path, file_type):
    full_name = os.path.join(path, file_type)
    if not os.path.exists(full_name):
        os.mkdir(full_name)


def unpack_archive(path, file_obj, file_name, file_type):
    unpack_path = os.path.join(path, file_type, normalize(file_name))
    try:
        shutil.unpack_archive(file_obj.absolute(), unpack_path)
        for file in find_files(Path(unpack_path)):
            new_file_name, new_file_ext = get_file_attrs(file.name)
            new_path = os.path.join(unpack_path, ".".join(
                [normalize(new_file_name), new_file_ext]))
            shutil.move(file.absolute(), new_path)
        file_obj.unlink()
    except shutil.ReadError:
        return


def move_file(path, file_obj, file_name, file_ext, file_type):
    check_dir(path, file_type)
    if file_type == 'archives':
        unpack_archive(path, file_obj, file_name, file_type)
    else:
        new_path = os.path.join(path, file_type, ".".join(
            [normalize(file_name), file_ext]))
        shutil.move(file_obj.absolute(), new_path)


def sort_by_extension(path, file):
    file_name, file_ext = get_file_attrs(file.name)
    if file_ext.upper() in IMAGES:
        file_type = 'images'
    elif file_ext.upper() in VIDEO:
        file_type = 'video'
    elif file_ext.upper() in DOCUMENTS:
        file_type = 'documents'
    elif file_ext.upper() in MUSIC:
        file_type = 'music'
    elif file_ext.upper() in ARCHIVES:
        file_type = 'archives'
    else:
        file_type = None
    if file_type:
        move_file(path, file, file_name, file_ext, file_type)


def main():
    path = sys.argv[1]
    path = Path(path)
    files = find_files(Path(path))
    path_list = [path] * len(files)
    if files:
        with ThreadPoolExecutor() as executor:
            executor.map(sort_by_extension, path_list, files)
            print(threading.active_count())
    else:
        print('Path does not exist')
    find_dirs(path)


if __name__ == '__main__':
    start = time.time()
    main()
    razn = time.time() - start
    print(razn)
