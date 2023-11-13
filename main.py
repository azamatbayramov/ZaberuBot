import aiogram
import asyncio
import os


BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

MESSAGE_TO_REPLY = "Необычное предложение. Где вы находитесь?"
MESSAGE_TO_NOTIFY = "Пользователь написал сообщение:"
KEYWORDS = ["otdam"]

bot = aiogram.Bot(token=BOT_TOKEN)

dp = aiogram.Dispatcher()


def to_english_letters(s: str) -> str:
    # Replace non-English letters with their closest English equivalents
    s = s.translate(
        str.maketrans(
            {
                "а": "a",
                "б": "b",
                "в": "v",
                "г": "g",
                "д": "d",
                "е": "e",
                "ё": "e",
                "ж": "zh",
                "з": "z",
                "и": "i",
                "й": "y",
                "к": "k",
                "л": "l",
                "м": "m",
                "н": "n",
                "о": "o",
                "п": "p",
                "р": "r",
                "с": "s",
                "т": "t",
                "у": "u",
                "ф": "f",
                "х": "kh",
                "ц": "ts",
                "ч": "ch",
                "ш": "sh",
                "щ": "shch",
                "ъ": "",
                "ы": "y",
                "ь": "",
                "э": "e",
                "ю": "yu",
                "я": "ya",
                "0": "o",
            }
        )
    )

    return s


def is_text_with_keywords(text: str) -> bool:
    text = text.lower()
    text = text.replace(" ", "")
    text = to_english_letters(text)

    for word in KEYWORDS:
        if word in text:
            return True

    return False


@dp.message()
async def handle_new_message(message: aiogram.types.Message):
    if message.text or message.caption:
        text = message.text or message.caption

        if is_text_with_keywords(text):
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


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
