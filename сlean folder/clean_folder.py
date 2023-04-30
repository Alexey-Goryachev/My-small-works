#импорт библиотек и модулей 
import sys, shutil, re, stat
from pathlib import Path
#################################


#списки хранения файлов для сортировки по каждой категории
IMAGES = []
VIDEOS = []
DOCUMENTS = []
MUSICS = []
ARCHIVES = []
UNKNOWN = []
#################################################


#кортежи расширений сортируемых файлов согласно условия
img = ('JPEG', 'PNG', 'JPG', 'SVG')
vid = ('AVI', 'MP4', 'MOV', 'MKV')
doc = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
mus = ('MP3', 'OGG', 'WAV', 'AMR')
arc = ('ZIP', 'GZ', 'TAR')
#######################################################


#множества для хранения известных и не известных расширений файлов
know_extensions = set()
unknown_extensions = set()
########################################################


#словарь для хранение значений путей отсортированных папок
dict_new_folders = {}
#########################################################


#список для временного хранения путей папок, их которых переносим файлы в отсортированные папки
folders = []
########################################################################


#функция для сканирования заданной папки которую нужно отсортировать
def scan_folder(path):
    
    p = Path(path)
    for i in p.iterdir():
        if i.is_file():
            ext = i.suffix[1:]
            if ext.upper() in img:
                shutil.move(processing_file_images(i), dict_new_folders.get('images'))
            elif ext.upper() in vid:
                shutil.move(processing_file_video(i), dict_new_folders.get('video'))
            elif ext.upper() in doc:
                shutil.move(processing_file_documents(i), dict_new_folders.get('documents'))
            elif ext.upper() in mus:
                shutil.move(processing_file_audio(i), dict_new_folders.get('audio'))
            elif ext.upper() in arc:
                shutil.move(processing_file_archives(i), dict_new_folders.get('archives'))
            else:
                shutil.move(processing_file_unknown(i), dict_new_folders.get('unknown'))
        else:
            if i.name not in ('images', 'documents', 'audio', 'video', 'archives', 'unknown'):
                folders.append(i)
                scan_folder(i)
            else:
                continue
    
################################################################################################


#функции для обработки файлов каждого типа:
def processing_file_images(path):
    know_extensions.add(path.suffix[1:])
    t = (str(path.parent) + '\\' + normalize(path.stem) + path.suffix)
    IMAGES.append(path.name)
    return path.rename(t)

def processing_file_documents(path):
    know_extensions.add(path.suffix[1:])
    t = (str(path.parent) + '\\' + normalize(path.stem) + path.suffix)
    DOCUMENTS.append(path.name)
    return path.rename(t)

def processing_file_audio(path):
    know_extensions.add(path.suffix[1:])
    t = (str(path.parent) + '\\' + normalize(path.stem) + path.suffix)
    MUSICS.append(path.name)
    return path.rename(t)

def processing_file_video(path):
    know_extensions.add(path.suffix[1:])
    t = (str(path.parent) + '\\' + normalize(path.stem) + path.suffix)
    VIDEOS.append(path.name)
    return path.rename(t)

def processing_file_archives(path):
    know_extensions.add(path.suffix[1:])
    t = (str(path.parent) + '\\' + normalize(path.stem) + path.suffix)
    ARCHIVES.append(path.name)
    return path.rename(t)

def processing_file_unknown(path):
    unknown_extensions.add(path.suffix[1:])
    t = (str(path.parent) + '\\' + normalize(path.stem) + path.suffix)
    UNKNOWN.append(path.name)
    return path.rename(t)
###############################################


# функция для создание отсортированных папок  в внутри папки в которой проводим сортировку:
def create_sort_folders(path):
    pathimg = Path(path)/'images'
    dict_new_folders.update({'images': pathimg})
    pathimg.mkdir(exist_ok=True)

    pathdocuments = Path(path)/'documents'
    dict_new_folders.update({'documents': pathdocuments})
    pathdocuments.mkdir(exist_ok=True)

    pathaudio = Path(path)/'audio'
    dict_new_folders.update({'audio': pathaudio})
    pathaudio.mkdir(exist_ok=True)

    pathvideo = Path(path)/'video'
    dict_new_folders.update({'video': pathvideo})
    pathvideo.mkdir(exist_ok=True)

    patharchives = Path(path)/'archives'
    dict_new_folders.update({'archives': patharchives})
    patharchives.mkdir(exist_ok=True)
    
    pathunknown = Path(path)/'unknown'
    dict_new_folders.update({'unknown': pathunknown})
    pathunknown.mkdir(exist_ok=True)
#############################################################


# реализация функции normalize:
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", 'i', "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name
####################################################################
   

#функция распаковки архива  в папку с названием архива
def unpack_archives(path):

    archives = Path(path)/'archives'
    for i in archives.iterdir():
       
        name_folder = Path(i.parent)/i.stem
        name_folder.mkdir(exist_ok=True)
        if i.suffix[1:] == 'gz':
             shutil.unpack_archive(i, name_folder, 'gztar')
             i.unlink()
        else:
            shutil.unpack_archive(i, name_folder)
            i.unlink()
####################################################################


#функция  удаления пустых папок после переноса всех файлов в отсортированные папки
def delete_empty_folders(spisok_folders):
    for i in spisok_folders[::-1]:
        Path.chmod(i, stat.S_IWRITE)
        i.rmdir()
##########################################


# фуункция для вывода данных названий и расширений файлов 
def print_information():
    print(f'известные расширения {know_extensions}') #вывод известных расширений
    print(f'неизвестные расширения {unknown_extensions}')#вывод неизвестных расширений
    print(f'изображения {IMAGES}') # вывод списков файлов  для сортировки по каждой категории
    print(f'видео {VIDEOS}')
    print(f'документы{DOCUMENTS}')
    print(f'музыка{MUSICS}')
    print(f'архивы{ARCHIVES}')
    print(f'неизвестно{UNKNOWN}')

####################################################


#функция для запуска скрипта из консоли 
def run():
    create_sort_folders(sys.argv[1])
    scan_folder(sys.argv[1])
    unpack_archives(sys.argv[1])
    delete_empty_folders(folders)
    print_information()
###########################################


#точка входа
if __name__ == '__main__':
    run()
