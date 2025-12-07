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

    url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?query={query}"

    try:
        data = requests.get(url).json()

        products = data.get("data", {}).get("products", [])
        if not products:
            await update.message.reply_text("По твоему запросу ничего не найдено 😔")
            return

        reply = ""
        for item in products[:20]:  # максимум 20 товаров
            name = item.get("name")
            price = item.get("salePriceU", 0) // 100
            old_price = item.get("priceU", 0) // 100
            discount = item.get("sale", 0)
            link = f"https://www.wildberries.ru/catalog/{item.get('id')}/detail.aspx"

            reply += (
                f"🛍 {name}\n"
                f"💰 Цена: {price} ₽\n"
                f"❌ Старая цена: {old_price} ₽\n"
                f"🔻 Скидка: {discount}%\n"
                f"{link}\n\n"
            )

        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("Ошибка при получении данных 😔")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("find", find))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

