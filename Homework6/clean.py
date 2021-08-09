from aiopath import AsyncPath
import asyncio
import sys
import os.path
import re
import aioshutil

IMAGES = ['JPEG', 'PNG', 'JPG']
VIDEO = ['AVI', 'MP4', 'MOV']
DOCUMENTS = ['DOC', 'DOCX', 'TXT', 'PPTX', 'XLSX', 'PDF']
MUSIC = ['MP3', 'OGG', 'WAV', 'AMR']
ARCHIVES = ['ZIP', 'GZ', 'TAR']
FILE_DICT = {'IMAGES': 'images',
             'VIDEO': 'video',
             'DOCUMENTS': 'documents',
             'MUSIC': 'music',
             'ARCHIVES': 'archives'}


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


async def find_files(in_path):
    in_path = AsyncPath(in_path)
    files = []
    async for file in in_path.iterdir():
        is_dir = await file.is_dir()
        if is_dir:
            result = await find_files(file)
            files.extend(result)
        is_file = await file.is_file()
        if is_file:
            files.append(file.absolute())

    return files


async def find_dirs(in_path):
    in_path = AsyncPath(in_path)
    exist = await in_path.exists()
    if exist:
        files = len(await find_files(in_path))
        object_list = in_path.iterdir()
        if object_list:
            async for obj in object_list:
                is_dir = await obj.is_dir()
                if is_dir:
                    await find_dirs(obj)
        if files == 0:
            await in_path.rmdir()


def get_file_attrs(fl):
    new_fl = fl[::-1]
    fl_ext, fl_nm = new_fl.split('.', maxsplit=1)
    return fl_nm[::-1], fl_ext[::-1]


def check_dir(path, file_type):
    full_name = os.path.join(path, file_type)
    if not os.path.exists(full_name):
        os.mkdir(full_name)


async def unpack_archive(path, file_obj, file_name, file_type):
    unpack_path = os.path.join(path, file_type, normalize(file_name))
    try:
        await aioshutil.unpack_archive(file_obj.absolute(), AsyncPath(unpack_path))
        for file in await find_files(unpack_path):
            new_file_name, new_file_ext = get_file_attrs(file.name)
            new_path = AsyncPath(os.path.join(unpack_path, ".".join(
                [normalize(new_file_name), new_file_ext])))
            await aioshutil.move(file.absolute(), new_path)
        await file_obj.unlink()
    except aioshutil.Error:
        return


async def move_file(path, file_obj, file_name, file_ext, file_type):
    check_dir(path, file_type)
    if file_type == 'archives':
        await unpack_archive(path, file_obj, file_name, file_type)
    else:
        new_path = AsyncPath(os.path.join(path, file_type, ".".join(
            [normalize(file_name), file_ext])))
        await aioshutil.move(file_obj.absolute(), new_path)


async def sort_by_extension(path, files):
    for file in files:
        file_name, file_ext = get_file_attrs(file.name)
        if file_ext.upper() in IMAGES:
            file_type = 'images'
        elif file_ext.upper() in VIDEO:
            file_type = 'video'
        elif file_ext.upper() in DOCUMENTS:
            file_type = 'ducuments'
        elif file_ext.upper() in MUSIC:
            file_type = 'music'
        elif file_ext.upper() in ARCHIVES:
            file_type = 'archives'
        else:
            file_type = None
        if file_type:
            await move_file(path, file, file_name, file_ext, file_type)


async def main():
    path = sys.argv[1]
    path = AsyncPath(path)
    files = await find_files(path)
    if files:
        await sort_by_extension(path, files)
    else:
        print('Path does not exist')
    await find_dirs(path)


if __name__ == '__main__':
    asyncio.run(main())
