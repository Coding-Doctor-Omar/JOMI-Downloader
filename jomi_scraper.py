from curl_cffi import AsyncSession, requests
from tqdm import tqdm



YELLOW = "\033[33m"


class JomiScraper:
    def __init__(self, vid_name: str, quality: str, vid_url: str):
        self.initialize_scraper(vid_name=vid_name, quality=quality, vid_url=vid_url)

    def initialize_scraper(self, vid_name: str, quality: str, vid_url: str):
        self.video_data_url = ""
        self.subtitle_data_url = ""
        self.vid_name = vid_name
        self.vid_quality = quality
        self.vid_url = vid_url
        self.pbar_fmt = f"{YELLOW}" + "Downloading video: {l_bar}{bar}|{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt} ]"

    async def get_video_data_url(self, session: AsyncSession) -> None:
        vid_types = {
            "low": "IphoneVideoFile",
            "medium": "HdMp4VideoFile",
            "high": "OriginalFile"
        }

        r = await session.get(self.vid_url, impersonate="edge")
        separator = f'"contentType":"video/mp4","type":"{vid_types[self.vid_quality]}"'

        self.video_data_url = r.text.split(separator)[0].split('"url":"')[-1].split(".bin")[0] + ".bin"




    async def download_mp4(self, session: AsyncSession) -> None:
        with open(f"{self.vid_name}.mp4", mode="wb") as vid_file:
            pass

        r = await session.get(self.video_data_url, stream=True)

        total_size = int(r.headers["Content-Length"])
        pbar = tqdm(unit="B", total=total_size, unit_scale=True, bar_format=self.pbar_fmt)

        async for chunk in r.aiter_content(chunk_size=1024 * 512):
            with open(f"{self.vid_name}.mp4", mode="ab") as vid_file:
                vid_file.write(chunk)

            pbar.update(len(chunk))

        pbar.close()

    async def download_video(self) -> None:
        async with AsyncSession(impersonate="edge", timeout=120000) as session:
            await self.get_video_data_url(session)
            await self.download_mp4(session)

        print(f"\n{YELLOW}Downloading subtitles...")
        self.download_subtitles()


    def download_subtitles(self):
        r = requests.get(self.vid_url, impersonate="edge")
        video_id = r.text.split("/embed/iframe/")[-1].split(",")[0].replace('"', "").split("}")[0].strip()
        self.subtitle_data_url = f"https://fast.wistia.com/embed/captions/{video_id}.json"

        r = requests.get(self.subtitle_data_url, impersonate="edge")
        data = r.json()

        subtitles = [sub["hash"]["lines"] for sub in data["captions"] if sub["familyName"] == "English"][0]

        with open(f"{self.vid_name}.srt", mode="w", encoding="utf-8") as subtitle_file:
            for ind, line in enumerate(subtitles):
                line_num = ind + 1
                start_raw = line["start"]
                end_raw = line["end"]

                start_hrs = int(start_raw // 3600)
                start_mins = int((start_raw % 3600) // 60)
                start_secs = int(start_raw % 60)
                start_ms = int((start_raw - int(start_raw)) * 1000)
                start_string = f"{start_hrs:02}:{start_mins:02}:{start_secs:02},{start_ms:03}"

                end_hrs = int(end_raw // 3600)
                end_mins = int((end_raw % 3600) // 60)
                end_secs = int(end_raw % 60)
                end_ms = int((end_raw - int(end_raw)) * 1000)
                end_string = f"{end_hrs:02}:{end_mins:02}:{end_secs:02},{end_ms:03}"

                time_string = f"{start_string} --> {end_string}"
                line_text = "\n".join(line["text"])

                block_text = f"{line_num}\n{time_string}\n{line_text}\n\n"

                subtitle_file.write(block_text)

        self.initialize_scraper("", "", "")
