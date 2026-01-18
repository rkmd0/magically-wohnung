from config import *
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance in kilometers between two latitude/longitude points using the Haversine formula.

    Arguments: lat1 -- Latitude of the first point in degrees.
    lon1 -- Longitude of the first point in degrees.
    lat2 -- Latitude of the second point in degrees.
    lon2 -- Longitude of the second point in degrees.

    Returns:
    Distance in kilometers between the two points.
    """
    # Convert latitude/longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Earth's radius in kilometers
    radius = 6371

    # Calculate the distance
    distance = radius * c
    return distance

from telegram import Bot

async def send_telegram_message(message):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_ID, text=message)
