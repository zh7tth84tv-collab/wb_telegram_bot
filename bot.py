import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

TOKEN = "8569033661:AAFaEy3EKKam2y7SF59eey34e9_qklVPkY4"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я найду товары по скидке на Wildberries.\n\n"
        "Формат запроса:\n"
        "/find nike\n"
        "/find куртка\n"
        "/find детские ботинки"
    )


async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши запрос. Например: /find adidas")
        return

    query = " ".join(context.args)

    url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?query={qu
