API_TOKEN = "6012171080:AAG_JJpDns1tNvMLFm0eE20mImpFOqEWw-8"

#                [0]             [1]                  [2]                        [3]                        [4]                       [5]             [6]          [7]                  [8]
# user_id: [rdyBtnPressed, QuestStartTime, [w1btn, w2btn ... wnbtn], [w1btn, w2btn ... wnbtn], [q1Press, q2Press, lastQPress], "крышка"->Entered, parkPhotoID, selfieSent?, "континенталь"->Entered]
user_database = dict()

quizQA = {"Какой герой мультфильма живёт в ананасе под водой? 🌊🍍": ["Губка Боб", "Камбала", "Немо"],
          "Какую цифру имеет черный шар в американском бильярде? 🧐🤔": ["8", "7", "9"],
          "Что такое вайфаер? 👨‍🦯❓": ["Очки", "Рукавицы", "Шорты"],
          "С помощью какого ингредиента делают шугаринг? 🤨👀": ["Сахар", "Воск", "Мёд"],
          "Какая страна производит больше всего кофе в мире? ☕🌍": ["Бразилия", "Индонезия", "Вьетнам"],
          "Сколько минут, по правилам, может длиться игра в волейбол? ⌛🏐": ["Неограничено", "20", "15"],
          "Какой из этих цветов - НЕ оттенок красного? ❎🔴": ["Айвори", "Марсала", "Терракотовый"],
          "Сколько букв 'W' изображено на логотипе Volkswagen? 🚗ℹ️": ["Одна", "Две", "Три"],
          "Айвори это цвет...": ["Слоновой Кости", "Спелой Алычи", "Пожелтевших Листьев"],
          "Дриблинг делается с помощью...": ["Мяча", "Пилы", "Удочки"]}

parkIMG = ["img//park1.jpg", "img//park2.jpg"]

answers = {
    "starting": "Буна зива! 👋\n\nС днём рождения, Мамочка! 🥳❤️‍🔥\nТебе уже 42 годика, а выглядишь ты на все 25! 😎\n\nХотим пожелать тебе всего самого хорошего!) 💌\nЗдоровья, богатства, удачи, хороших и верных друзей, взаимопонимания в семье, успех в работе и во всех твоих хобби, чтобы удача преследовала тебя по жизни ну и конечно же счастья! 🥰\n\nА чтобы сделать этот день веселее, мы приготовили для тебя квест! 🥷👣 Но перед ним, ты должна подготовиться и одеться по погоде, так как квест будет не дома 🫣",
    "quiz": f"Отлично! Предлагаю разогреться перед квестом и пройти простенькую викторину из {len(quizQA)} вопросов! 🧠💥",
    "house": 'Супер! Ты прошла викторину! 🎉\n\nИ как по мне, самое время уже начать наш квест 👣🥷\n\nТак вот, первая бумажка всё это время лежала в ноуте Саньки!\n\nИ ещё кое-что! Чуть не забыл) 🫣\nУ нас с тобой должно быть секретное слово, его ‼️ВАЖНО‼️ запомнить, оно тебе понадобится!\nНаше секретное слово это:\nℹ️ "cadou" ["кадоу"] ℹ️\n\nА теперь я желаю тебе удачи! Ещё увидимся 😘',
    "lid": "Именно! ✅\n\nКакой бы огромной ни была кастрюля, внутрь никак нельзя поместить её крышку 🥘\n\nТы очень умная! 🧠🔥\nМы тобой гордимся! ❤️❤️❤️",
    "minipark": "Следующая локация очень зелёная, ведь кто не любит зелень и парки? 🙃\n\nСейчас я дам тебе начальную картинку, из которой ты возможно узнаешь место, но если не выйдет с первого раза - не волнуйся, я сделал несколько фото, поэтому ты всегда можешь попросить подсказку нажав на нужную кнопку! 🥰",
    "sending": "Секундочку, отправляю! ⌛",
    "selfie": "Ваууу!! 😍\nКакая же ты красивая 😍❤️",
    "selfie1": "На этот раз, чтобы добраться до локации, я скину тебе её примерную геопозицию и фотографию того, что ты должна найти! 🙃",
    "stairs": "Сейчас быстренько расскажу что тебе нужно делать на этой локации! 😉",
    "stairs1": "Видишь Богдана там внизу? 👀\n\nПервым делом, тебе нужно стать именно на том пролёте 🙃",
    "stairs2": "Молодец, ты нашла это число! 🔥\n\nВстань точно как показано на фото ниже, лицом к числу которое ты только что нашла 😉",
    "continental": "Хммм, континенталь говоришь? 🤔\nДай-ка я гляну что у меня есть... 🧐",
    "continental1": "Я откопал только одну фотку с подсказкой, на ней не особо что-то понятно, но по моим данным после этой локации уже идёт финал. Поэтому нужно постараться! 💯\n\nУдачи!! ❤️"}