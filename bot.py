import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.dispatcher.router import Router
from aiogram.enums import ContentType
from aiogram import F
import asyncio
from ollama_api import ask_ollama


BOT_TOKEN = "your token"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

router = Router()
dp.include_router(router)

@router.message(F.text)
async def echo_handler(message: Message):
    try:
  
        wait_msg = await message.answer("⏳ Подождите, ответ генерируется...")

   
        answer = ask_ollama(message.text, user_id=str(message.from_user.id))

      
        await bot.edit_message_text(
            chat_id=wait_msg.chat.id,
            message_id=wait_msg.message_id,
            text=answer
        )
    except Exception as e:
        logger.exception("Ошибка при обработке сообщения:")
        await message.answer("⚠️ Произошла ошибка при генерации ответа.")

async def main():
    logger.info("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

