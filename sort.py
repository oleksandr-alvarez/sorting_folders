import os 
import sys
import shutil
import re

def normalize(string_to_tr):
    '''
    This function will produce a string transliterated from the Ukrainian alphabet to the English one.
    It will also replace any non-word characters with "_"
    '''
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {} 

    for c,t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = t
        TRANS[ord(c.upper())] = t.upper()
    
    string_to_tr = string_to_tr.translate(TRANS)

    pattern = '\W'
    
    string_to_tr = re.sub(pattern, '_', string_to_tr)
    
    return string_to_tr


def delete_empty_folders(path):
    '''
    This function will delete empty folder in the path.
    '''
    
    for folder_name in os.listdir(path):
        if folder_name not in ['audio', 'video', 'images', 'documents', 'unknowns', 'archives']:
            folder_path = os.path.join(path, folder_name)
            if os.path.isdir(folder_path):
                delete_empty_folders(folder_path) 
                if not os.listdir(folder_path):
                    os.rmdir(folder_path)

def unpack(archive_path, path_to_unpack):
    '''
    This function will unpack archive files using the shutil.unpack_archive function in the specified direction.
    '''
    shutil.unpack_archive(archive_path, path_to_unpack)

def get_path_of_files(path):

    '''
    This function will return set of paths of all files in the folder
    If the document is not a file, it will not be included in the set
    '''

    list_in_folder = [os.path.join(path, el) for el in os.listdir(path)]    
    set_of_files = {el for el in list_in_folder if os.path.isfile(el)}
    list_of_dir = [el for el in list_in_folder if os.path.isdir(el)]

    if len(list_of_dir) != 0:
        for dir in list_of_dir:
            set_of_files.update(get_path_of_files(dir))
    else: 
        return set_of_files
    
    return set_of_files
    
def sort_files_to_folders(path):
    '''
    Main function that:
    
    1) creates folders audio, video, images, documents, archives, unkowns
    2) sorts all files in the path to their respective folders
    3) delets the empty folders
    4) if a file was written in Ukrainian, renames it to its transliteration 
    5) prints out the list of files in each folder in the form of dictionary
    6) prints out the list of known extensions
    7) prints out the list of unkowon extensions 
    '''

    # We first find the pathes to all files 

    path_to_all_files = get_path_of_files(path)  
    
    image_extensions = ['jpeg', 'png', 'jpg', 'svg']
    video_extensions = ['avi', 'mp4', 'mov', 'mkv']
    document_extensions = ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']
    music_extensions = ['mp3', 'ogg', 'wav', 'amr']
    archive_extensions = ['zip', 'gz', 'tar']

    known_extensions = image_extensions + video_extensions + document_extensions + music_extensions + archive_extensions
    
    # We sort the pathes depending on their extensions

    pathes_to_images = [el 
                        for image in image_extensions 
                        for el in path_to_all_files
                        if image in el.split('\\')[-1].split('.')[-1]]
    
    pathes_to_videos = [el 
                        for video in video_extensions 
                        for el in path_to_all_files 
                        if video in el.split('\\')[-1].split('.')[-1]]
    
    pathes_to_documents = [el 
                        for video in document_extensions 
                        for el in path_to_all_files 
                        if video in el.split('\\')[-1].split('.')[-1]]
    pathes_to_music = [el 
                        for video in music_extensions 
                        for el in path_to_all_files
                        if video in el.split('\\')[-1].split('.')[-1]]
    
    pathes_to_archives = [el 
                        for video in archive_extensions 
                        for el in path_to_all_files
                        if video in el.split('\\')[-1].split('.')[-1]]
    
    pathes_to_knowns = pathes_to_archives + pathes_to_music + pathes_to_documents + pathes_to_videos + pathes_to_images
    
    for el in pathes_to_knowns:
        path_to_all_files.discard(el)
    
    pathes_to_unknowns = path_to_all_files
    
    # We create new dedicated folders
    image_folder = 'images'
    video_folder = 'video'
    document_folder = 'documents'
    music_folder = 'audio'
    archive_folder = 'archives'
    unknown_folder = 'unknowns'

    folder_names = ['images', 'video', 'documents',
                    'audio', 'archives', 'unknowns']
    
    for folder_name in folder_names:
        os.mkdir(os.path.join(path, folder_name))
    
    # moving files from pathes(_to_) to the newly created dedicated folders

    for image_source in pathes_to_images:
        shutil.move(image_source, os.path.join(path, image_folder))
    
    for video_source in pathes_to_videos:
        shutil.move(video_source, os.path.join(path, video_folder))

    for doc_source in pathes_to_documents:
        shutil.move(doc_source, os.path.join(path, document_folder))

    for music_source in pathes_to_music:
        shutil.move(music_source, os.path.join(path, music_folder))

    for archive_source in pathes_to_archives:
        shutil.move(archive_source, os.path.join(path, archive_folder))
    
    for unknown_source in pathes_to_unknowns:
        shutil.move(unknown_source, os.path.join(path, unknown_folder))
    
    for archive_path in os.listdir(os.path.join(path, archive_folder)):
        unpack(os.path.join(path, archive_folder, archive_path), os.path.join(path, archive_folder))
    
    # AFter moving files to their dedicated folders, there are empty folders which are deleted
    delete_empty_folders(path)

    path_to_all_files = get_path_of_files(path) 

    list_of_known_extensions = set()
    list_of_unknown_extensions = set()

    for file_path in path_to_all_files:
        file_name = file_path.split("\\")[-1].split(".")[0]
        file_extension = file_path.split("\\")[-1].split(".")[1]
        if file_extension in known_extensions:
            list_of_known_extensions.add(file_extension)
        else:
            list_of_unknown_extensions.add(file_extension)
        file_name_ext = normalize(file_name) + "." + file_extension
        os.rename(file_path, "\\".join(file_path.split('\\')[:-1]) + "\\" + file_name_ext)

    list_of_files_in_folder = dict()

    for folder in folder_names:
        direction = os.path.join(path, folder)
        list_of_files_in_folder[folder] = os.listdir(direction)
    
    print(f'List of files per folder: {list_of_files_in_folder}')
    print(f'List of known extensions: {list_of_known_extensions}')
    print(f'LIst of unknown extensions: {list_of_unknown_extensions}')    
    

def main():
    folder_to_sort = sys.argv[1]
    sort_files_to_folders(folder_to_sort)


if __name__ == '__main__':
    main()  