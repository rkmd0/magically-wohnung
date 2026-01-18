from apscheduler.schedulers.asyncio import AsyncIOScheduler
from selectolax.parser import HTMLParser
from functions import *
from config import *
import aiohttp
import asyncio

BASE_URL = "https://www.real-estate.lviv.ua"

last_id = 0

async def parse():
    global last_id
    async with aiohttp.ClientSession() as session:
        async with session.get(ENDPOINT) as r:
            content = await r.content.read()
            tree = HTMLParser(content)
            objects = tree.css(".col-dense-right")

            for obj in objects:
                if "data-name" not in obj.attributes:
                    continue

                if obj.attributes["data-name"] != "object":
                    continue

                obj_id = int(obj.attributes["data-id"])

                if obj_id <= last_id:
                    continue

                obj_lat = float(obj.attributes["data-lat"])
                obj_lng = float(obj.attributes["data-lng"])
                obj_url = BASE_URL + obj.css_first(
                    ".text-under-photo-search-listing"
                ).attributes["href"]

                price_paragraph = obj.css_first(".object-listing-price")
                price = price_paragraph.css_first("span").text().strip()
                price = price.replace(" ", "")
                price = int(price)

                if price < MIN_PRICE:
                    continue

                distance_continue = False
                _name = ""

                for point in points:
                    distance = haversine_distance(
                        point["lat"], point["lng"],
                        obj_lat, obj_lng
                    )

                    if distance < point["dist"]:
                        distance_continue = False
                        _name = point["name"]
                        break

                    distance_continue = True

                if distance_continue:
                    continue

                last_id = obj_id

                message = ""

                message += f"Ціна: {price} грн\n"
                message += f"Район: {_name}\n"
                message += ""
                message += obj_url

                await send_telegram_message(message)
                print(obj_url, price)

def init_scheduler():
    scheduler = AsyncIOScheduler(
        daemon=True, timezone="Europe/Berlin", misfire_grace_time=None
    )

    scheduler.add_job(parse, "interval", minutes=1)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    init_scheduler()
