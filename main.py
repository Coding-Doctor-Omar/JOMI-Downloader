from jomi_scraper import JomiScraper
import asyncio
import os, sys, json

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
* 2. Settings             *
* 3. How to Use           *
* 4. About                *
* 5. Exit                 *
***************************
"""

settings_menu = r"""
***************************
*        SETTINGS         *
***************************
* 1. Video Quality        *
* 2. Back to Main Menu    *
***************************
"""

quality_options = r"""
***************************
*  Change Video Quality   *
***************************
* 1. Low                  *
* 2. Medium (recommended) *
* 3. High                 *
* 4. Back to Main Menu    *
***************************
"""

how_to_use_text = r"""
1. In the main menu, type '1' and press ENTER.
2. You will be asked to provide the URL for the video page and to provide your desired video name.
3. Grab a cup of tea and rest until the video is downloaded.
4. Wait until you see 'Download Complete!'.
5. The video file (.mp4) and subtitles file (.srt) will be saved in the same folder.

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

[v1.2.1]


Press ENTER to return to the main menu.
"""


GREEN = "\033[32m"
AQUA = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def ask_user_choice() -> str:
    return input("\nChoose an option: ").strip()

def ask_video_url() -> str:
    return input("\nVideo URL: ").lower().strip()

def ask_video_name() -> str:
    return input("Video Name: ").strip().replace(" ", "_")

async def download_video(vid_name, vid_url):
    settings = get_user_settings()
    quality = settings.get("videoQuality")

    scraper = JomiScraper(vid_name=vid_name, vid_url=vid_url, quality=quality)

    print(f"{YELLOW}Initializing Download...\n")
    await scraper.download_video()
    print(f"\nDownload Complete!")
    print("=======================================================")
    print(f"{AQUA}The following files have been saved in the same folder:\n\n")

    print("[Video]")
    print(f"{vid_name}.mp4\n")

    print("[Subtitles]")
    print(f"{vid_name}.srt")

    input(f"\n{GREEN}Press ENTER to return to the main menu.")
    
def get_user_settings() -> dict:
    try:
        with open("settings.json", mode="r") as settings_file:
            settings = json.load(settings_file)
    except Exception:
        settings = {
            "videoQuality": "medium"
        }
        with open("settings.json", mode="w", encoding="utf-8") as settings_file:
            json.dump(settings, settings_file, indent=4)

    try:
        _ = settings["videoQuality"]

        if settings["videoQuality"] not in ["low", "medium", "high"]:
            settings = {
                "videoQuality": "medium"
            }
            with open("settings.json", mode="w", encoding="utf-8") as settings_file:
                json.dump(settings, settings_file, indent=4)

    except KeyError:
        settings = {
            "videoQuality": "medium"
        }
        with open("settings.json", mode="w", encoding="utf-8") as settings_file:
            json.dump(settings, settings_file, indent=4)
    
    return settings

def set_video_quality(user_choice: str) -> None:
    choice_dict = {
        "1": "low",
        "2": "medium",
        "3": "high"
    }
    new_quality = choice_dict[user_choice]

    settings: dict = get_user_settings()
    settings.update({"videoQuality": new_quality})

    with open("settings.json", mode="w", encoding="utf-8") as settings_file:
        json.dump(settings, settings_file, indent=4)
    


async def main():
    while True:
        settings = get_user_settings()
        
        clear_screen()
        print(f"{GREEN}{logo}")
        print(menu_options)

        menu_choice = ask_user_choice()

        if menu_choice == "5":
            sys.exit(0)
        elif menu_choice == "1":
            vid_url = ask_video_url()
            vid_name = ask_video_name()

            if not vid_name: # Video name cannot be empty
                input("\nInvalid video name. Press ENTER to retry.")
                continue
            else:
                try: # Video name has to be a valid name
                    with open(f"{vid_name}.mp4", mode="w") as vid:
                        pass
                except Exception:
                    input("\nInvalid video name. Press ENTER to retry.")
                    continue
                else:
                    clear_screen()
                    print(logo)
                    await download_video(vid_name, vid_url)
                    continue
        elif menu_choice == "2":
            clear_screen()
            print(logo)
            print(settings_menu)
            
            settings_menu_choice = ask_user_choice()
            
            if settings_menu_choice == "2":
                continue
            elif settings_menu_choice == "1":
                quality = settings.get("videoQuality")
                clear_screen()
                print(logo)
                print(f"{GREEN}Current Video Quality: {YELLOW}{quality.title()}{GREEN}\n")
                print(quality_options)
                
                quality_choice = ask_user_choice()
                
                if quality_choice not in ["1", "2", "3", "4"]:
                    input("\nInvalid option. Press ENTER to go back to the main menu.")
                elif quality_choice == "4":
                    continue
                else:
                    set_video_quality(user_choice=quality_choice)
                    settings = get_user_settings()
                    quality = settings.get("videoQuality")
                    clear_screen()
                    print(logo)
                    print(f"{GREEN}Current Video Quality: {YELLOW}{quality.title()}{GREEN}\n")
                    print(quality_options)
                    input("\nVideo quality has been updated. Press ENTER to go back to the main menu.")
            
            else:
                input("\nInvalid option. Press ENTER to go back to the main menu.")
                continue
        
        elif menu_choice == "3":
            clear_screen()
            print(logo)
            input(how_to_use_text)
            continue
        elif menu_choice == "4":
            clear_screen()
            print(logo)
            input(about_text)
            continue
        else:
            input("\nInvalid menu choice. Press ENTER to retry.")
            continue

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        input(f"\n{RED}Error: {e}")