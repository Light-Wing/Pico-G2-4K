import logging
import traceback
import cv2
import re
import json
import os
import shutil
from pathlib import Path


HeadsetFolder = Path(__file__).parent / "./for_headset"

MoviesFolder = os.path.join(HeadsetFolder, "Movies")
MoviesListFolder = os.path.join(HeadsetFolder, "MoviesList")
VideoUIFolder = os.path.join(MoviesListFolder, "VideoUI")
DibblerListFile = os.path.join(MoviesListFolder, "DibblerList.txt")

ImportMoviesFolder = Path(__file__).parent / "./videos"
ImportThumbnailFolder = Path(__file__).parent / "./thumbnails"

folders_to_clean = [ImportThumbnailFolder, VideoUIFolder, MoviesFolder]

# list to store files
counter = 1
used_indexes = []
data = []

for f in folders_to_clean:
    try:
        shutil.rmtree(f)
    except FileNotFoundError:
        print(f, "already deleted")
    os.mkdir(f)


def with_opencv(filename):
    video = cv2.VideoCapture(filename)

    duration = video.get(cv2.CAP_PROP_POS_frame)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    video.release()

    return duration, frame_count


def ask_if_headset_connected():
    print('is the headset connected?')
    is_connected = 'x'
    while (is_connected not in ['y', 'n']):
        is_connected = input('type Y or N: ').lower()

    if is_connected == 'y':
        return True
    elif is_connected == 'n':
        return False
    else:
        print('how did the user bypass the is_connected while loop?')


def ask_if_did_backup():
    print('did you backup the original files (for example: add .bak to each file/folder)?')
    print('files that are modified are:')
    print('Movies/, MoviesList/DibblerList.txt, MoviesList/VideoUI/')

    is_connected = 'x'
    while (is_connected not in ['y']):
        is_connected = input('type Y or N: ').lower()
        if is_connected == 'n':
            print('then go back up... if you want to finish here, just press ctrl+c')

    return True


def push_stuff_to_headset():

    from ppadb.client import Client as AdbClient

    # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.devices()[0]
    # print(device)

    device.push(DibblerListFile, '/sdcard/MoviesList/DibblerList.txt')
    device.push(VideoUIFolder, '/sdcard/MoviesList/VideoUI')
    device.push(MoviesFolder, '/sdcard/Movies')

    print('copied all files to headset')


def copy_to_headset():
    is_connected = ask_if_headset_connected()
    if is_connected:
        ask_if_did_backup()
    else:
        return
    push_stuff_to_headset()


def save_frame_from_video(import_video_path, final_video_path, frame_num, frame_file_path):
    vidcap = cv2.VideoCapture(import_video_path)

    og_frame_num = frame_num

    needToReplaceFileNames = False
    if og_frame_num == "ReplaceTimeStamp":
        video_length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        print("video frame amount:", video_length)
        frame_num = round(video_length * 0.5)
        # cap.set(cv2.CAP_PROP_POS_FRAMES, round(video_length * 0.5))
        print("video frame half time:", frame_num)
        needToReplaceFileNames = True
        frame_file_path.replace(og_frame_num, str(frame_num))

    vidcap.set(cv2.CAP_PROP_POS_FRAMES, float(frame_num))

    # print('video_path', final_video_path)
    # print('vidcap', vidcap)

    success, image = vidcap.read()

    # save image to temp file
    # cv2.imwrite(frame_file_path, image)
    if success:
        cv2.imwrite('%s.png' % frame_file_path, image)
        print("image saved for=>", final_video_path)
    else:
        print("image was not saved for=>", final_video_path)

    vidcap.release()
    if needToReplaceFileNames:
        os.rename(final_video_path, final_video_path.replace(
            og_frame_num, str(frame_num)))
        os.rename(import_video_path, import_video_path.replace(
            og_frame_num, str(frame_num)))

    return


def get_file_info(video_file_name):
    """
    1st group of number(s) = the file index, where it will appear in the list, if missing, will generate a new number, can be manually set
    2nd group of number(s) = VideoType of file (check which on it is), if missing, will be replaced with "VideoTypeToReplace"
    3rd group of number(s) = thumbnail frame_num, if not found, it set to "ReplaceTimeStamp" and will be replaced by the default = the half time of the video
    """
    Default_Index = 0
    Default_VideoType = "VideoTypeToReplace"
    Default_Thumbframe = "ReplaceTimeStamp"
    regex = '(^(\d+)\.)((\d+|(%s))\.)?((\d+|(%s))\.)?' % (Default_VideoType,
                                                          Default_Thumbframe)
    file = re.search(regex, video_file_name)
    # print('file', file)
    # print('video_file_name', video_file_name)
    if hasattr(file, 'group'):
        # ('0.', '0',
        # 'VideoTypeToReplace.', 'VideoTypeToReplace', 'VideoTypeToReplace',
        # 'ReplaceTimeStamp.', 'ReplaceTimeStamp', 'ReplaceTimeStamp')
        # print(file.groups())  # ^
        file_index = file.group(2) if file.group(2) else Default_Index
        video_type = file.group(4) if file.group(4) else Default_VideoType
        thumbnail_frame = file.group(7) if file.group(
            7) else Default_Thumbframe
    else:
        print('file has no groups', file)

        file_index = Default_Index
        video_type = Default_VideoType
        thumbnail_frame = Default_Thumbframe
    global counter
    while (counter in used_indexes):
        print("while (counter in new_index):", counter, used_indexes)
        counter += 1

    new_index = counter if (int(file_index) == 0) else int(file_index)
    while new_index in used_indexes:
        new_index += 1

    used_indexes.append(int(new_index))
    print('used_indexes', used_indexes)
    print('new_index', new_index)
    print('counter', counter)
    print('file_index == 0', (int(file_index) == 0))
    if (new_index == counter):
        counter += 1

    print('video_file_name', video_file_name)
    clean_file_name = re.sub(regex, "", video_file_name)

    print('clean_file_name', clean_file_name)

    # zero_padded_index = str(file_index).zfill(2)+"."
    new_index_str = str(new_index) + "."
    video_type_str = str(video_type) + "."
    thumbnail_frame_str = str(thumbnail_frame) + "."
    file_name_with_info = new_index_str + \
        video_type_str + thumbnail_frame_str + clean_file_name

    renamed_file = rename_file(file_name_with_info)

    og_file = os.path.join(
        ImportMoviesFolder, video_file_name)
    new_file = os.path.join(
        ImportMoviesFolder, file_name_with_info)

    os.rename(og_file, new_file)

    print('new_index: =>', new_index)
    print('video_type: =>', video_type)
    print('thumbnail_frame: =>', thumbnail_frame)
    # print('new_file: =>', new_file)
    print('clean_file_name: =>', clean_file_name)
    # print('renamed_file: =>', renamed_file)
    print("\n----\n")

    return new_index, video_type, thumbnail_frame, new_file, clean_file_name, renamed_file


def rename_file(file_name_with_info):
    replacements = [
        ('(_\.mp4)+', '.mp4'),
        (' ', '_'),
        (',', ''),
        ('\._', '_'),
        ('360°', '360'),
        ('_-_', '__'),
        ('\.mkv$', '_mkv.mp4'),
    ]

    for old, new in replacements:
        file_name_with_info = re.sub(old, new, file_name_with_info)

    print('\n----\nfile_name_with_info:', file_name_with_info)
    return file_name_with_info


# VideoType's
vid_360_all_around = "2"
vid_split_in2_horizontal = "20"
vid_split_in4_vertical = "21"
# Iterate directory

list_of_video_to_save = []
try:
    for file_name in os.listdir(ImportMoviesFolder):  # MoviesFolder

        # check if current path is a file
        file_name_path = os.path.join(ImportMoviesFolder, file_name)
        if not os.path.isfile(file_name_path):
            print('found '+file_name+' that is not a file, so skipping.')
            continue

        # if os.path.isfile(file_in_import_folder):
        # new_file -        is the same file in the videos folder, with added index, video type and thumbnail time, without changing the video name
        # clean_file_name - is the file name on its own, without any extra manipulation, without info of file
        # renamed_file -    is the final file name to be saved in movies
        new_index, video_type, thumbnail_frame, new_file, clean_file_name, renamed_file = get_file_info(
            file_name)

        # check if the file was properly saved with new_file name
        file_in_import_folder = os.path.join(ImportMoviesFolder, new_file)
        if os.path.isfile(file_in_import_folder):
            print("[v] [import] file ==> %s found in ImportMoviesFolder" %
                  str(new_file)[0:10])
        else:
            print("[!] [import] file ==> %s NOT found in ImportMoviesFolder" %
                  str(new_file)[0:10])
            print("need to check why this happend, breaking")
            break

        # check if the file exists in the movies folder, and if not, delete it.
        file_in_final_folder = os.path.join(MoviesFolder, renamed_file)

        # this is so that i can delete the other files...
        list_of_video_to_save.append(file_in_final_folder)

        if os.path.isfile(file_in_final_folder):
            print("[v] [final] file ==> %s found in MoviesFolder" %
                  str(renamed_file)[0:10])
        else:
            print("[!] [final] file ==> %s NOT found in MoviesFolder" %
                  str(renamed_file)[0:10])
            print('copying the file to the movies folder')
            shutil.copy2(file_in_import_folder, file_in_final_folder)
            print('Done copying.', file_in_final_folder)

        thumbnail_file_path = os.path.join(
            VideoUIFolder, renamed_file).replace('.mp4', '')

        # print('thumbnail_file_path', thumbnail_file_path)

        save_frame_from_video(import_video_path=file_in_import_folder,
                              final_video_path=file_in_final_folder,
                              frame_num=thumbnail_frame, frame_file_path=thumbnail_file_path)
        # video_to_frames(new__full_file_path, thumbnail_file_path)

        #  example = {
        #     "Id": "1",
        #     "Name": "1.大报恩寺.mp4",
        #     "VideoType": "2",
        #     "Program": "1.Daihouonji"
        #     }
        newData = {
            "Id": str(new_index),
            "Name": renamed_file,
            "VideoType": video_type,
            "Program": str(new_index) + "." + clean_file_name
        }
        # counter = counter+1
        data.append(newData)
except FileNotFoundError:
    print("Directory: {0} does not exist".format(MoviesFolder))
except Exception as e:
    logging.error(traceback.format_exc())

with open(DibblerListFile, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

copy_to_headset()

# def image_to_thumbs(img):
#     """Create thumbs from image"""
#     height, width, channels = img.shape
#     thumbs = {"original": img}
#     print('thumbs', thumbs)
#     sizes = [640, 1080]
#     for size in sizes:
#         if (width >= size):
#             r = (size + 0.0) / width
#             max_size = (size, int(height * r))
#             thumbs[str(size)] = cv2.resize(
#                 img, max_size, interpolation=cv2.INTER_AREA)

#     return thumbs


# def video_to_frames(video_filename, thumbnail_file_path):
#     """Extract frames from video"""
#     print('\n\n----\nvideo_filename', video_filename)
#     cap = cv2.VideoCapture(video_filename)
#     video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
#     print('vid cap', cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     print('vid length', video_length)
#     frames = []
#     if cap and cap.isOpened() and video_length > 0:
#         cap.set(cv2.CAP_PROP_POS_FRAMES, round(video_length * 0.5))
#         success, frame = cap.read()
#         cv2.imwrite('%s.png' % thumbnail_file_path, frame)
#     return  # frames
