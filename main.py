import logging, asyncio, time, random, datetime

from data import API_TOKEN, answers, user_database, quizQA, parkIMG
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

## Старт ##
@dp.message_handler(commands=['start'])
async def welcomingFunc(message: types.Message):
    ## Приветствие ##
    await bot.send_chat_action(message.chat.id, 'typing')
    await asyncio.sleep(2.5)
    await message.answer(answers.get("starting"))

    ## Добавление кнопки "Готова" ##
    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    btnReady = types.InlineKeyboardButton("Готова!", callback_data='rdyBtn')
    inline_keyboard.add(btnReady)

    await asyncio.sleep(15)
    await message.answer("Ты готова? (Нажми когда оденешься!) 🤗", reply_markup=inline_keyboard)
    
    ## Ставим rdyBtnPressed на False для пользователя [0] ##
    user_id = message.from_user.id
    if user_id in user_database:
        del user_database[user_id]

    user_database[user_id] = [False]


## Викторина ##
@dp.callback_query_handler(lambda query: query.data == "rdyBtn")
async def rdyBtnHandler(query: types.CallbackQuery):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    if not user_database[user_id][0]:
        user_database[user_id][0] = True

        ## Добавляем стартовое время пользователя [1] ##
        user_database[user_id].append(time.time())

        ## Простенькая викторина ##
        await asyncio.sleep(0.2)
        await bot.send_message(chat_id, answers.get("quiz"))
        
        quiz_keyboard = types.InlineKeyboardMarkup(row_width=1)
        user_database[user_id].append([f"w{i}" for i in range(len(quizQA)*2)]) # wBtnList - [2]
        user_database[user_id].append(user_database[user_id][2].copy()) # wBtnListEditable - [3]

        wBtnList = user_database[user_id][3]

        for question, possible_answers in quizQA.items():
            rans, wans1, wans2 = possible_answers
            
            rkbutton = types.InlineKeyboardButton(rans, callback_data="Q1RightOPT")
            wkbutton1 = types.InlineKeyboardButton(wans1, callback_data=wBtnList[0])
            wBtnList.pop(0)
            wkbutton2 = types.InlineKeyboardButton(wans2, callback_data=wBtnList[0])
            wBtnList.pop(0)
            btnList = [rkbutton, wkbutton1, wkbutton2]
            random.shuffle(btnList)
            quiz_keyboard.add(*btnList)
            break

        await asyncio.sleep(3)
        await bot.send_message(chat_id, f"[1/{len(quizQA)}] {question}", reply_markup=quiz_keyboard)
        user_database[user_id].append([False]) # Q1 button - False [4][0]

@dp.callback_query_handler(lambda query: query.data in user_database[query.from_user.id][2])
async def wrongQuizAnswer(query: types.CallbackQuery):
    await query.answer("Не-а! ❌ Попробуй ещё 🔄")

@dp.callback_query_handler(lambda query: query.data in [f"Q{i}RightOPT" for i in range(1, len(quizQA)+1)])
async def rightQuizAnswer(query: types.CallbackQuery):
    quiz_keyboard = types.InlineKeyboardMarkup(row_width=1)
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    quizLen = len(quizQA)
    wBtnList = user_database[user_id][3]

    for ind, data in enumerate(quizQA.items()):
        if ind == 0:
            continue

        if query.data == f"Q{quizLen}RightOPT" and not user_database[user_id][4][quizLen-1]:
            user_database[user_id][4][quizLen-1] = True
            await asyncio.sleep(0.2)
            await bot.send_message(chat_id, answers.get("house"))
            user_database[user_id].append(False)
            break

        if query.data == f"Q{ind}RightOPT" and not user_database[user_id][4][ind-1]:
            user_database[user_id][4][ind-1] = True
            question, possible_answers = data
            rans, wans1, wans2 = possible_answers

            rkbutton = types.InlineKeyboardButton(rans, callback_data=f"Q{ind+1}RightOPT")
            wkbutton1 = types.InlineKeyboardButton(wans1, callback_data=wBtnList[0])
            wBtnList.pop(0)
            wkbutton2 = types.InlineKeyboardButton(wans2, callback_data=wBtnList[0])
            wBtnList.pop(0)
            btnList = [rkbutton, wkbutton1, wkbutton2]
            random.shuffle(btnList)
            quiz_keyboard.add(*btnList)

            await asyncio.sleep(0.6)
            await bot.send_message(chat_id, f"[{ind+1}/{quizLen}] {question}", reply_markup=quiz_keyboard)
            user_database[user_id][4].append(False)
            break


## Реакция на ответ на загадку ##
@dp.message_handler()
async def answerMessages(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id not in user_database:
        return
    
    if message.text.lower() == "крышка" and not user_database[user_id][5]:
        user_database[user_id][5] = True
        await message.reply(answers.get("lid"))

        await bot.send_chat_action(chat_id, 'typing')
        await asyncio.sleep(5)
        await message.answer(answers.get("minipark"))
        await asyncio.sleep(10)
        await message.answer(answers.get("sending"))

        support_keyboard = types.InlineKeyboardMarkup(row_width=1)
        support_keyboard.add(types.InlineKeyboardButton("🗝️ ПОДСКАЗКА 🗝️", callback_data="SupportBtn"))
        
        await bot.send_chat_action(chat_id, 'upload_photo')
        with open("img//park.jpg", "rb") as picPark1:
            await message.answer_photo(picPark1, caption="Поняла сразу? Или нужна подсказка?", reply_markup=support_keyboard)

        user_database[user_id].append(1) # PhotoIndex [6]
        user_database[user_id].append(False) # SelfieSent? [7]

    elif (message.text.lower() == "континенталь" or message.text.lower() == "continental") and not user_database[user_id][8]:
        user_database[user_id][8] = True
        await message.reply(answers.get("continental"))
        await bot.send_chat_action(chat_id, "upload_photo")
        await asyncio.sleep(2.25)
        with open("img//continental.jpg", "rb") as picContinental1:
            await message.answer_photo(picContinental1, caption=answers.get("continental1"))

    elif message.text.lower() == "20 пицца":
        start = user_database[user_id][1]
        end = time.time()
        final_time = int(end - start)
        final_time_readable = datetime.timedelta(seconds=final_time)
        await asyncio.sleep(0.4)
        await message.reply(f"Именно так! 💯💯💯\n\nТы справилась с нашим квестом и в очередной раз доказала, какая же ты у нас умная! 🧠🔥\n\nМы очень сильно тебя любим! ❤️❤️❤️❤️❤️❤️❤️\nС днём рождения, Мамочка 🥳\n\nСейчас я скину тебе локацию пиццерии, куда мы отправимся дальше 🥰\n\nНе забудь сказать наше секретное слово когда придёшь в пиццерию! 🤫\n\nВремя, за которое ты прошла квест: {final_time_readable} 🤯\n\nНад твоим днём рождения трудились:\n• Ромчик, любимый сын\n• Серёжа, любимый жум\n• Катя, любимая сестра\n• Богдан, друг Ромки")
        await asyncio.sleep(10)
        await bot.send_chat_action(chat_id, "find_location")
        await asyncio.sleep(6)
        await message.answer_location(latitude=45.789202, longitude=24.142178)

@dp.callback_query_handler(lambda query: query.data == "SupportBtn")
async def sendSupportPictures(query: types.CallbackQuery):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    picID = user_database[user_id][6]
    user_database[user_id][6] += 1

    if len(parkIMG) < picID:
        await bot.send_message(chat_id, "К сожалению, у меня больше нет фото ❌🖼️")
    else:
        await bot.send_message(chat_id, "Конечно! Лови фотку! 😜")
        await bot.send_chat_action(chat_id, 'upload_photo')
        picPath = f"img//park{picID}.jpg"
        with open(picPath, "rb") as picParkSupport:
            await bot.send_photo(chat_id, picParkSupport)


## Реакция на селфи от мамы ##
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def answerToPhoto(message: types.Message):
    user_id = message.from_user.id
    if not user_database[user_id][7]:
        user_database[user_id][7] = True
        
        await asyncio.sleep(0.75)
        await message.reply(answers.get("selfie"))
        await asyncio.sleep(0.8)
        await message.answer(answers.get("selfie1"))
        await bot.send_chat_action(message.chat.id, "find_location")
        await asyncio.sleep(4)
        await message.answer_location(latitude=45.7982, longitude=24.151611)

        continue_keyboard = types.InlineKeyboardMarkup(row_width=1)
        continue_keyboard.add(types.InlineKeyboardButton("Нашла!", callback_data="FindBtn"))
        await bot.send_chat_action(message.chat.id, 'upload_photo')
        await asyncio.sleep(2)
        with open("img//stairs.jpg", "rb") as picStairs1:
            await message.answer_photo(picStairs1, caption="Нажмёшь кнопку 'нашла', когда станешь на место на фото!", reply_markup=continue_keyboard)
        user_database[user_id].append(False) # [8]

@dp.callback_query_handler(lambda query: query.data in ["FindBtn", "foundNumBtn"])
async def sendContinuePicture(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    if query.data == "FindBtn":
        await asyncio.sleep(0.2)
        await bot.send_message(chat_id, answers.get("stairs"))
        await bot.send_chat_action(chat_id, 'upload_photo')
        await asyncio.sleep(1.5)
        with open("img//stairs1.jpg", "rb") as picStairs2:
            await bot.send_photo(chat_id, picStairs2, caption=answers.get("stairs1"))
        foundNumber_keyboard = types.InlineKeyboardMarkup(row_width=1)
        foundNumber_keyboard.add(types.InlineKeyboardButton("Вижу число!", callback_data="foundNumBtn"))
        await asyncio.sleep(3)
        await bot.send_message(chat_id, 'Стоя там, ты должна оглянуться по сторонам и найти число "1868" 🔍🧐', reply_markup=foundNumber_keyboard)

    elif query.data == "foundNumBtn":
        await asyncio.sleep(0.2)
        await bot.send_message(chat_id, answers.get("stairs2"))
        await asyncio.sleep(2.25)
        with open("img//stairs2.jpg", "rb") as picStairs3:
            await bot.send_photo(chat_id, picStairs3, caption="Стоя так, как на фото, поверни голову на 90° влево, в той области и лежит следующая бумажка! 🎉")
        


def main():
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()