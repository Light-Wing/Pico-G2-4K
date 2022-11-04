# Movies Folder

this folder contains the video files

each file should start with a number as an index, which determines its position in the headset software
each file should be an mp4 file.
example: `1.________.mp4`

ive added the VideoType (a piece of info that determines how the video file is proccessed)
its a number from 0 to 25 (see images VideoTypes1-5.jpeg, VideoTypes6-25.jpeg)

ive put the VideoType right after the index number
example: `1.20.________.mp4` (for video type "CubeMap" = 20)

Maybe:
ill add the thumbnail time in the file name, after the video type
example: `1.20.2321.________.mp4` (means thumbnail is taken from about 23 secounds (num is in milisec) into the video)

###

### 

# `MoviesList` Folder

this folder contains many folders, most are for panorama videos

we care about the `VideoUI` folder and the `DibblerList.txt` file

## `VideoUI` Folder

this folder contains the thumbnails for the videos in `Movies` folder

each file needs to match the video file name it belongs to...
except the file extension which needs to be .png

example: `1.20.________.png`


## `DibblerList.txt` file

this file is in json format (with .txt file extension)
it has 1 array with many objects
1 object for each video 
```
{
    "Id":"3", //index
    "Name":"3.火箭发射.mp4", //video file name, must start with the index and end with .mp4
    "VideoType":"20", //the file type
    "Program":"3.RocketLaunching" // the display name, also should start with the index number
}
```