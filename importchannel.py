from telegram import Bot
from telegram.error import TelegramError
from telegram import InputMediaPhoto
import json
import asyncio

TOKEN = "5756745551:AAEUDIn5AnqGzmmxx068pGtzoYpukooyKY8"
bot = Bot(token=TOKEN)


async def send_message_with_photo(chat_id, text, photo_path):
    try:
        with open(photo_path, "rb") as photo_file:
            await bot.send_photo(chat_id=chat_id, photo=photo_file, caption=text)
    except TelegramError as e:
        print(f"Error sending message: {e}")


async def send_plain_message(chat_id, text):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except TelegramError as e:
        print(f"Error sending message: {e}")


async def main():
    with open("result.json", "r", encoding="utf-8") as json_file:
        channel_history = json.load(json_file)

    channel_username = "@tochka_zakupa"
    for message_data in channel_history["messages"]:
        try:
            text_entities = message_data["text_entities"]
            text = "".join(
                item.get("text", str(item)) if isinstance(item, dict) else str(item) for item in text_entities)
            photo = message_data.get("photo", None)

            if photo:
                await send_message_with_photo(chat_id=channel_username, text=text, photo_path=photo)
            else:
                await send_plain_message(chat_id=channel_username, text=text)

            # Introduce a delay between messages
            await asyncio.sleep(5)  # Adjust the delay duration as needed
        except TelegramError as e:
            print(f"Error sending message: {e}")

    print("Message sending completed.")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
