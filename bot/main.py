import json

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config


class App:
    def __init__(self):
        self.app = ApplicationBuilder().token(config('BotKey')).build()
        self.chat_id = None
        self._register_handlers()

    def _register_handlers(self):
        self.app.add_handler(MessageHandler(filters=filters.StatusUpdate.WEB_APP_DATA, callback=self.web_app_handler))
        self.app.add_handler(MessageHandler(filters=filters.ALL, callback=self.message_handler))
    def web_app_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(update.effective_message.web_app_data.data)
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.chat_id = update.effective_chat.id
        web_url = f'https://ee3158ac6659.ngrok-free.app/todos/' + str(self.chat_id)

        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton('اجرای todo', web_app=WebAppInfo(url=web_url))]])
        await update.message.reply_text('لطفا برای اجرای وب اپ روی دکمه اجرا بزنید', reply_markup=keyboard)

    def run(self):
        print('bot start...')
        self.app.run_polling()


if __name__ == '__main__':
    app = App()
    app.run()
