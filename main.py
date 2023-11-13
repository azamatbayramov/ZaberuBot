import aiogram
import asyncio
import os


BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

MESSAGE_TO_REPLY = "Возможно заберу. Куда подходить?"
MESSAGE_TO_NOTIFY = "Пользователь написал сообщение:"
KEYWORDS = ["отдам"]

bot = aiogram.Bot(token=BOT_TOKEN)

dp = aiogram.Dispatcher()


@dp.message()
async def handle_new_message(message: aiogram.types.Message):
    if message.text or message.caption:
        text = message.text or message.caption
        for word in KEYWORDS:
            if word in text.lower():
                await message.reply(MESSAGE_TO_REPLY)

                await bot.send_message(
                    ADMIN_ID,
                    MESSAGE_TO_NOTIFY,
                )

                await bot.forward_message(
                    ADMIN_ID,
                    message.chat.id,
                    message.message_id,
                )

                break


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
