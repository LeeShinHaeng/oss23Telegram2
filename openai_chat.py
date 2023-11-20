import os
import logging
import asyncio
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI

#TOKEN : token of your chatbot
#API_KEY : token of your OpenAI address
token = "TOKEN"
client = OpenAI(
    api_key="API_KEY"
)

#start 명령어 처리
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

#gpt에게 문의하는 함수
async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = update.message.text + "json"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question}
        ],
        response_format={"type": "json_object"}
    ) 
    choices_text = completion.choices[0].message.content
    await update.message.reply_text(choices_text)

#token을 사용해 app 실행
app = ApplicationBuilder().token(token).build()

#command " /start " 명령어로 start
app.add_handler(CommandHandler("start", start))

#사용자가 보낸 메시지에 대해 gpt에 검색
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gpt))

#Ctrl+C를 입력할때까지 실행
app.run_polling()