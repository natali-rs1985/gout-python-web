import time
import sys
import os
import os.path
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor
import threading


IMAGES = ['JPEG', 'PNG', 'JPG']
VIDEO = ['AVI', 'MP4', 'MOV']
DOCUMENTS = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'XLSX', 'PPTX']
MUSIC = ['MP3', 'OGG', 'WAV', 'AMR']
ARCHIVES = ['ZIP', 'GZ', 'TAR']
FILE_DICT = {'IMAGES': 'images',
             'VIDEO': 'video',
             'DOCUMENTS': 'documents',
             'MUSIC': 'music',
             'ARCHIVES': 'archives'}


def find_dirs(in_path):
    dirs_lst = []
    for dirpath, dirs, f_files in os.walk(in_path):
        dirs_lst.append(Path(dirpath))
    return dirs_lst


def find_files(dir):
    files = []
    if dir.exists():
        for file in dir.iterdir():
            if file.is_file():
                files.append(file)
    return files


def conc_find_files(in_path):
    files = list()
    dirs = find_dirs(in_path)

    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_path = list(executor.map(find_files, dirs))
        print(threading.active_count())

    for x in future_to_path:
        files.extend(x)

    return files


def del_dirs(in_path):
    if in_path.exists():
        files = len(conc_find_files(in_path))
        object_list = in_path.iterdir()
        if object_list:
            for obj in object_list:
                if obj.is_dir():
                    del_dirs(obj)
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
    unpack_path = os.path.join(path, file_type, file_name)
    try:
        shutil.unpack_archive(file_obj.absolute(), unpack_path)
        for file in find_files(Path(unpack_path)):
            new_file_name, new_file_ext = get_file_attrs(file.name)
            new_path = os.path.join(unpack_path, ".".join(
                [new_file_name, new_file_ext]))
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
            [file_name, file_ext]))
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
    files = conc_find_files(path)
    path_list = [path] * len(files)
    if files:
        with ThreadPoolExecutor() as executor:
            executor.map(sort_by_extension, path_list, files)
            print(threading.active_count())
    else:
        print('Path does not exist')
    del_dirs(path)


if __name__ == '__main__':
    start = time.time()
    main()
    razn = time.time() - start
    print(razn)
