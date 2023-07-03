import asyncio
import time

import aiofiles
import aiofiles.os
import aioshutil
from aiopath import AsyncPath

import os
import re
import unicodedata
from cleaner_consts import table
from typing import Tuple, Callable
from classes import TerminalView
from logger import get_logging

logger_ = get_logging(__name__)

cleaner_commands = TerminalView()
cleaner_commands_comm: str = '''
    To sort files, type the path to your folder according the pattern: <DISC:\\Folder\\Other folder...>
    To back to main menu, type: <back>
    To see instructions of this module, type: <help>'''
cleaner_commands.add_command(cleaner_commands_comm)
root: str = ''


async def process_directory(directory: str) -> None:
    logger_.info(f'Function process_directory: {directory}')
    async for path in AsyncPath(directory).iterdir():
        if await path.is_file():
            await process_file(directory, path.name)
        elif await path.is_dir() and path.name.lower() not in extensions.keys():
            await process_directory(path)

    '''for file in os.listdir(directory):
        file_path: str = os.path.join(directory, file)
        if await aiofiles.os.path.isfile(file_path):
            await process_file(directory, file)
        elif await aiofiles.os.path.isdir(file_path) and file.lower() not in extensions.keys():
            await process_directory(file_path)'''


async def process_file(file_path: str, file: str) -> None:
    logger_.info(f'Function process_file: {file} from {file_path}')
    name, extension = file.rsplit('.', 1)
    func_: tuple = handle_func(extension)
    await func_[0](file_path, f'{root}\\{func_[1]}', name, extension)
    await check_folder(file_path)
    await asyncio.sleep(0.001)


async def deal_with_copies(old_path: str, new_path: str, new_name: str, ext: str) -> None:
    i: int = 0
    while True:
        if f'{new_name}.{ext}' not in os.listdir(new_path):
            await aiofiles.os.replace(f'{old_path}\\{new_name}.{ext}', f'{new_path}\\{new_name}.{ext}')
            break
        else:
            i += 1
            file_name: str = new_name
            new_name = f'{file_name}_{i}'
            await aiofiles.os.rename(f'{old_path}\\{file_name}.{ext}', f'{old_path}\\{new_name}.{ext}')


async def move_to(old_path: str, new_path: str, file_name: str, ext: str) -> None:
    logger_.info(f'Function move_to: {file_name} from {old_path}')
    new_name: str = rename(file_name)
    await aiofiles.os.rename(f'{old_path}\\{file_name}.{ext}', f'{old_path}\\{new_name}.{ext}')
    await deal_with_copies(old_path, new_path, new_name, ext)


async def move_to_archive(old_path: str, new_path: str, file_name: str, ext: str) -> None:
    logger_.info(f'Function move_to_archive: {file_name} from {old_path}')
    new_name: str = rename(file_name)
    try:
        await aiofiles.os.makedirs('\\'.join((new_path, new_name.title())))
        await aioshutil.unpack_archive(f'{old_path}\\{file_name}.{ext}', '\\'.join((new_path, new_name.title())))
        await aiofiles.os.remove(f'{old_path}\\{file_name}.{ext}')
    except FileExistsError:
        await aiofiles.os.remove(f'{old_path}\\{file_name}.{ext}')


'''async def move_to_other(old_path: str, new_path: str, file_name: str, ext: str) -> None:
    logger_.info(f'Function move_to_other: {file_name}.{ext} from {old_path}')
    new_name: str = rename(file_name)
    await aiofiles.os.rename(f'{old_path}\\{file_name}.{ext}', f'{old_path}\\{new_name}.{ext}')
    await deal_with_copies(old_path, new_path, new_name, ext)'''


def rename(file_name: str) -> str:
    logger_.info(f'Function rename: {file_name}')
    pattern = r'[a-zA-Z0-9\.\-\(\)]'
    for char in file_name:
        if not re.match(pattern, char):
            if ord(unicodedata.normalize('NFC', char.lower())) in table.keys():
                file_name = file_name.replace(char, char.translate(table))
            else:
                file_name = file_name.replace(char, '_')
    return file_name


async def check_folder(old_path: str) -> None:
    logger_.info(f'Function check_folder: {old_path}')
    if not os.listdir(old_path):
        await aiofiles.os.rmdir(old_path)


extensions = dict(images=[('jpeg', 'png', 'jpg', 'svg'), move_to],
                  video=[('avi', 'mp4', 'mov', 'mkv'), move_to],
                  documents=[('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'), move_to],
                  audio=[('mp3', 'ogg', 'wav', 'amr', 'm4a'), move_to],
                  web=[('html', 'xml', 'csv', 'json'), move_to],
                  archive=[('zip', 'gz', 'tar'), move_to_archive])


def handle_func(file_extension: str) -> Tuple[Callable, str]:
    logger_.info(f'Function handle_func: {file_extension}')
    for category, extension in extensions.items():
        if file_extension in extension[0]:
            return extension[1], category.title()
    return move_to, 'Other'


async def after_check(path: str) -> None:
    logger_.info('Sorting was finished. After sorting checking is started')
    for folder in os.listdir(path):
        if get_folder_size(f'{path}\\{folder}') == 0:
            await aioshutil.rmtree(f'{path}\\{folder}')


def get_folder_size(folder_path: str) -> int:
    logger_.info('getting folder size')
    total_size: int = 0
    for roots, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(roots, file)
            total_size += os.path.getsize(file_path)
    return total_size


async def make_directories(path: str) -> None:
    logger_.info('Function make_directories')
    for key in extensions:
        await aiofiles.os.makedirs('\\'.join((path, key.title())), exist_ok=True)
    await aiofiles.os.makedirs('\\'.join((path, 'Other')), exist_ok=True)


async def check_path(path: str) -> str | None:
    logger_.info(f'Function check_path: {path}')
    if await aiofiles.os.path.exists(path):
        return path
    else:
        logger_.error(f'Error with an entered path: {path}')
        print('Something went wrong. Check a validity of the entered path.')


def instructions() -> None:
    logger_.info('Function instructions')
    for command in cleaner_commands.display_commands():
        print(command)


async def clean_folder(path: str):
    checked_path: str = await check_path(path)
    if checked_path:
        global root
        root = checked_path
        await make_directories(path)
        await process_directory(path)
        await after_check(path)
        print(f'The folder in path {checked_path} was cleaned.')


functions = {'help': instructions, 'path': clean_folder}


async def handler(command: str):
    logger_.debug(f'handling command: {command}')
    pattern = re.compile(r'([A-Z]:\\){1}(\w+\\)*(\w+){1}')
    if re.match(pattern, command):
        return await functions['path'](command)
    try:
        return functions[command]()
    except KeyError as error:
        logger_.error(f'Error occurred: {error}')
        print('I do not understand what you want to do. Please look at instructions, type <help>')


def greeting_cleaner() -> None:
    logger_.info('Function greeting_cleaner')
    print('''\n\tNow you are in the cleaning module. In this module I help you to sort all files 
    in the chosen directory thus cleaning your folder.''')


async def clean_folder_main() -> None:
    logger_.info('Function clean_folder_main')
    greeting_cleaner()
    instructions()
    while True:
        answer: str = input('\nType a path to a folder to clean or a command: ')
        if answer == 'back':
            print('\nYou returned to the main Menu.')
            break
        start = time.time()
        await handler(answer)
        finish = time.time()
        print(finish - start)
# Without handler() and dict functions:

'''async def clean_folder_main() -> None:
    logger_.info('Function clean_folder_main')
    greeting_cleaner()
    instructions()
    while True:
        answer: str = input('\nType a path to a folder to clean or a command: ')
        if answer == 'back':
            print('\nYou returned to the main Menu.')
            break
        elif answer == 'help':
            instructions()
        else:
            await clean_folder(answer)'''

# asyncio.run(clean_folder_main())
