from jomi_scraper import JomiScraper
import asyncio
import os, sys

logo = r"""
       _                 _   _____                      _                 _           
      | |               (_) |  __ \                    | |               | |          
      | | ___  _ __ ___  _  | |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
  _   | |/ _ \| '_ ` _ \| | | |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
 | |__| | (_) | | | | | | | | |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
  \____/ \___/|_| |_| |_|_| |_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
                                                                                      
                                                                                      
"""

menu_options = r"""
***************************
*        MAIN MENU        *
***************************
* 1. Download Video       *
* 2. How to Use           *
* 3. About                *
* 4. Exit                 *
***************************
"""

how_to_use_text = r"""
1. In the main menu, type '1' and press ENTER.
2. You will be asked to provide the URL for the video page and to provide your desired video name.
3. Grab a cup of tea and rest until the video is downloaded.
4. The video will be saved in the same directory as the 'main.py'.
5. Once you see 'Done! ....', congratulations, the video has been downloaded.

Press ENTER to return to the main menu.
"""

about_text = r"""
Developed by Omar Abdelhamid (Coding-Doctor-Omar)
GitHub: https://github.com/Coding-Doctor-Omar

JOMI stands for 'Journal Of Medical Insight'

This app offers a simple command-line interface (CLI) that allows the user to type the URL of any pay-walled JOMI
surgical video and downloads the full video in HD quality, bypassing the paywall.

WARNING:- This software is for educational purposes only. Review the TOS of JOMI before using.
I am not responsible for any misuse on your part.

Press ENTER to return to the main menu.
"""


GREEN = "\033[32m"
AQUA = "\033[36m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def ask_main_menu() -> str:
    return input("\nChoose an option: ").strip()

def ask_video_url() -> str:
    return input("\nVideo URL: ").lower().strip()

def ask_video_name() -> str:
    return input("Video Name: ").strip().replace(" ", "_")

async def download_video(vid_name, vid_url):
    scraper = JomiScraper(video_name=vid_name)

    print(f"{YELLOW}Fetching video segment URLs...")
    vid_data_url = await scraper.get_video_data_url(vid_url)
    vid_segment_urls = await scraper.get_video_segment_urls(vid_data_url)
    print(f"Fetched {scraper.total_segments} video segment URLs.")

    print(f"\nInitializing Download...")
    await scraper.download_video_segments(vid_segment_urls)
    print(f"Successfully downloaded all {scraper.total_segments} video segments.")

    print(f"Packing data into video file...")
    scraper.pack_video()
    scraper.download_subtitles(vid_url)
    input(f"{AQUA}\nDone! The video has been saved as '{vid_name}.ts' in the same directory, and the subtitles have been saved as '{vid_name}.srt' in the same directory!\nPress ENTER to go back to the main menu.")


async def main():
    while True:
        clear_screen()
        print(f"{GREEN}{logo}")
        print(menu_options)

        menu_choice = ask_main_menu()

        if menu_choice == "4":
            sys.exit(0)
        elif menu_choice == "1":
            vid_url = ask_video_url()
            vid_name = ask_video_name()

            if not vid_name:
                input("Invalid video name. Press ENTER to retry.")
                continue
            else:
                try:
                    with open(f"{vid_name}.ts", mode="w") as vid:
                        pass
                except Exception:
                    input("Invalid video name. Press ENTER to retry.")
                    continue
                else:
                    clear_screen()
                    print(logo)
                    await download_video(vid_name, vid_url)
                    continue
        elif menu_choice == "2":
            clear_screen()
            print(logo)
            input(how_to_use_text)
            continue
        elif menu_choice == "3":
            clear_screen()
            print(logo)
            input(about_text)
            continue
        else:
            input("Invalid menu choice. Press ENTER to retry.")
            continue

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        input(f"Error: {e}")