file structure:
#
## & => original file

## $ => my files
#



#


[list_of_folders]: "list of folders, each folder has **folder_name** match to name in one of the Panorama videos..."
- MoviesList/
    + Config/
        - [list_of_folders]
        (folders start with numbers is a good way to handle the ordering of the files)
        - each folder has at least 1 json file...
        - [TODO] need to ask and find out what the paramaters in the json file are for and how to use and manipulate them.
        - example: 01_some_video_name/
            1. some_file_1.json
            1. another-file.json
    + EditMusic/ 
        - [list_of_folders]
        - each folder has mp3 files
        - example: 01_some_video_name/
            1. ad01.mp3
            1. ad02.mp3
    + Music/
        - [list_of_folders] 
        - stores background music for the panorama videos
    + MusicConfig/
        - [list_of_folders] 
        - each folder stores background music config in .json files, most are empty
        - need to learn how and what these json files do
    + PanoramicAtlas/
        - [list_of_folders] 
        - each folder stores stores the 360deg image files (10MB avrage 8k image)
    + PictureUI/
        - has a list of .jpg files with **file_name** as the name mathcing panorama games
    + VideoUI/
        - has a list of .png files with **file_name** as the name mathcing video files

    + DibblerList.txt.json = a .json file struture for _ needs to .txt on the headset, so make sure to change it back (using json for vs code to properly recognize the file)  
        - file has list of VideoUI files names and their position on screen 
        - example: [{
            "Id":"1",
            "Name":"1.大报恩寺.mp4", //Dabaoen Temple
            "VideoType":"2",
            "Program":"1.Daihouonji"
        }, 
        ..., 
        {
            "Id":"8",
            "Name":"2.遨游海底.mp4",
            "VideoType":"20",
            "Program":"2.TravelSeabed"
        },]

    + PanoramaList.txt.json = same as above, file is for _


