import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("TOKEN")

async def survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ YES, I'm interested", callback_data="yes")],
        [InlineKeyboardButton("❌ NO, I'm not interested", callback_data="no")]
    ]

    await update.message.reply_text(
        "📢 *ThinkPad Unlock Tool*\n\n"
        "Are you interested in buying the ThinkPad Unlock Tool?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "yes":
        await query.edit_message_text(
            "✅ Thank you for your interest!"
        )

    elif query.data == "no":
        await query.edit_message_text(
            "❌ You chose not to continue.\nYou will now be removed from the group."
        )

        await context.bot.ban_chat_member(
            chat_id=query.message.chat.id,
            user_id=query.from_user.id,
        )

        await context.bot.unban_chat_member(
            chat_id=query.message.chat.id,
            user_id=query.from_user.id,
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("survey", survey))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
