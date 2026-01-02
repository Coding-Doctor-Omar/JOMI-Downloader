# JOMI Downloader
![logo](Jomi_logo.ico)

## NEWS
--- SOFTWARE UPGRADE ON DECEMBER 29, 2025 (v1.2.0) ---

**New Features**
1. Audio stuttering bug has been fixed (audio is now completely smooth).
2. Videos are now saved as ".mp4" instead of ".ts"
3. New "settings" feature added to the main menu (currently has video quality adjustment only).


--- SOFTWARE UPGRADE ON DECEMBER 25, 2025 (v1.1.0) ---



JOMI Downloader now shows a neat progress bar for the download progress, instead of the primitive text spam display.

--- SOFTWARE UPGRADE ON DECEMBER 16, 2025 ---



JOMI Downloader now also downloads the video captions and saves them in a ".srt" file in the same directory as the video file and with the same name as the video file.

You can now watch your surgical video with captions by just enabling captions in your video player and selecting the ".srt" file!

## Background
[JOMI](https://jomi.com/) stands for *Journal Of Medical Insight*. This journal is an online educational platform focused on high-quality surgical education. It provides peer-reviewed, step-by-step videos of real surgical procedures, performed by expert surgeons and accompanied by detailed explanations of anatomy, indications, operative steps, and postoperative considerations.

JOMI is designed primarily for medical students, residents, and practicing surgeons, offering a realistic view of surgery as it happens in the operating room. The platform covers multiple specialties (e.g., general surgery, orthopedics, OB/GYN, urology, neurosurgery) and emphasizes clinical decision-making, surgical technique, and intraoperative anatomy.

Access is typically paid and requires subscriptions. This is what this software intends to solve. It allows any medical student to access any video on the website for FREE, in HD quality, and with subtitles
by simply entering the URL for the video page. Note that this software is for educational purposes only.

## Installation
If you are not interested in going over the details of local Python setup and would like to easily and quickly use JOMI Downloader,
check the latest release [here](https://github.com/Coding-Doctor-Omar/JOMI-Downloader/releases/tag/v1.2.0).

Otherwise, if you like to setup Python on your device and run the Python files directly, follow the 4 steps below:

1. Make sure you have [Python](https://www.python.org/) installed on your computer.
2. Make sure 'main.py', 'jomi_scraper.py', 'setup.py', and 'requirements.txt' are downloaded and in a common folder.
3. Run 'setup.py' to automatically install the required dependencies for the software.
4. Run 'main.py' to launch the application.

## Usage
To navigate the different menu screens in the app, simply type the number of the option you want and press
ENTER. This rule applies to all menu pages in the app. Below is an example for how to download a video using JOMI Downloader
(use the same logic for the settings page).

To download a JOMI video, follow these steps (screenshots are shown at the end):

1. Once you launch the software, type '1' and press ENTER.
2. You will be asked to provide the URL for the JOMI video page. Paste the URL and press ENTER.
3. You will then be asked to provide a name for the output video. Type the name without an extension and press ENTER.
4. Sit back and relax while the downloader downloads the video and its captions for you.
5. Once the video is downloaded, you will see a message saying 'Download Complete!'. Once you see this, press ENTER to go back to the main menu.
6. The video will be saved in the same folder as a ".mp4" video file, and the subtitles file will be saved in the same folder as a ".srt" file with the same name as the video.

## Screenshots

Step 1:
![Step 1](images/menu.png)

Step 2:
![Step 2](images/copy_url.png)
![Step 2](images/write_vid_details.png)

Step 3:
![Downloading Progess](images/scraper_begin.png)
![Downloading Progress](images/scraper_progress.png)

Step 4:
![Download Complete](images/download_complete.png)

Video Played after Being Downloaded:
![Video in Folder](images/video_folder.png)
![captions 1](images/video_captions_1.png)
![captions 2](images/video_captions_2.png)
![captions 3](images/video_captions_3.png)

## Settings
Currently, the settings menu has 1 item: the Video Quality. This option allows the user
to choose the quality of the videos that are downloaded. The user's preferences are retained even if the user restarts the app.
There are 3 options for the
quality: Low, Medium, and High. 

The **low quality** option downloads a low quality (360p) video with a small size and fast download.

The **medium quality** option downloads an HD video (720p) with a moderate size and a moderate download time. This is the recommended option.

The **high quality** option downloads a full HD video (1080p), but with a huge size and much longer download time.

![settings 1](images/settings_1.png)
![settings 2](images/settings_2.png)
![quality 1](images/quality_1.png)
![quality 2](images/quality_2.png)





## Other Screenshots
About Screen:
![about screen](images/about.png)

How to Use Screen:
![how to use](images/how_to_use.png)