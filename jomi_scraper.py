from curl_cffi import AsyncSession, requests
from zendriver.cdp.network import enable, RequestWillBeSent
from asyncio import Event, Semaphore, Lock
from functools import wraps
import asyncio
import zendriver as zd

download_limit = Semaphore(120)
lock = Lock()


def limit_concurrency(async_func):
    """Concurrency limiter decorator."""
    @wraps(async_func)
    async def wrapper(*args, **kwargs):
        async with download_limit:
            await async_func(*args, **kwargs)

    return wrapper


class JomiScraper:
    def __init__(self, video_name: str="video"):
        self.initialize_scraper(video_name=video_name)

    def initialize_scraper(self, video_name: str="video"):
        self.total_segments = 0
        self.video_data_url = ""
        self.subtitle_data_url = ""
        self.video_segment_urls = []
        self.video_data = []
        self.vid_name = video_name
        self.video_data_url_seen = Event()

    async def get_video_data_url(self, video_url) -> str:
        browser = await zd.start(headless=True)
        page = await browser.get(url="https://jomi.com")
        await page.send(enable())

        def handle_req(event, _conn):
            try:
                req_url = event.request.url
            except AttributeError:
                pass
            else:
                if ".m3u8" in req_url and "embed-cloudfront.wistia.com" in req_url:
                    self.video_data_url = "https://embed-cloudfront.wistia.com/deliveries/" + req_url.split("deliveries/")[-1].split(".m3u8")[0] + ".m3u8"
                    self.video_data_url_seen.set()

        page.add_handler(RequestWillBeSent, handle_req)
        await page.get(video_url)
        await page.wait_for_ready_state(until="complete", timeout=60000)

        await page.evaluate('const el = document.querySelector("img[decoding=async]"); el.click();')
        await self.video_data_url_seen.wait()
        await browser.stop()

        return self.video_data_url

    async def get_video_segment_urls(self, video_data_url) -> list:
        async with AsyncSession(impersonate="edge", timeout=120000) as session:
            r = await session.get(video_data_url)
            with open("temp_data.txt", mode="w") as txt_file:
                txt_file.write(r.text)

        with open("temp_data.txt", mode="r") as txt_file:
            all_lines = txt_file.readlines()
            self.video_segment_urls = [("https://embed-cloudfront.wistia.com" + line).strip() for line in all_lines if "deliveries" in line]

        self.total_segments = len(self.video_segment_urls)
        return self.video_segment_urls

    @limit_concurrency
    async def download_video_segment(self, segment_url, session: AsyncSession, total_segs):
        r = await session.get(segment_url)
        seg_number = int(segment_url.split("/")[-1].split(".")[0].split("-")[1])
        seg_bytes = r.content

        seg_data = {
            "segment_number": seg_number,
            "segment_bytes": seg_bytes
        }

        async with lock:
            self.video_data.append(seg_data)
            print(f"Downloaded {len(self.video_data)}/{total_segs} video segments.")

    async def download_video_segments(self, segment_urls: list):
        async with AsyncSession(impersonate="edge", timeout=120000) as session:
            await asyncio.gather(*(self.download_video_segment(url, session, self.total_segments) for url in segment_urls))

    def pack_video(self):
        with open(f"{self.vid_name}.ts", mode="wb") as vid:
            pass

        for seg_num in range(1, self.total_segments + 1):
            segment = [seg for seg in self.video_data if seg["segment_number"] == seg_num][0]

            with open(f"{self.vid_name}.ts", mode="ab") as vid:
                vid.write(segment["segment_bytes"])

    def download_subtitles(self, vid_url):
        r = requests.get(vid_url, impersonate="edge")
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

        self.initialize_scraper()
