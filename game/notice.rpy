# -*- coding: utf-8 -*-
# In-game notice (unofficial fan patch)

label about_notice:
    scene black
    if persistent._language == "chinese":
        jump about_notice_zh
    jump about_notice_ru

label about_notice_zh:
    "本作品为《Welcome to Omsk》（2012）的非官方粉丝补丁。"
    "原作版权归 Связной и Семён（Svjaznoj i Semjon）所有。"
    "本补丁仅供非商业学习与欣赏。"
    "禁止出售或冒充官方。权利人要求下架将予配合。"
    "详细说明见项目根目录 NOTICE.md。"
    "（按继续返回）"
    return

label about_notice_ru:
    "Это неофициальный фан-патч к игре «Добро пожаловать в Омск» / Welcome to Omsk (2012)."
    "Авторские права на оригинал принадлежат Связному и Семёну (Svjaznoj i Semjon)."
    "Патч предназначен только для некоммерческого ознакомления."
    "Запрещается продажа и выдача патча за официальный релиз. По требованию правообладателей распространение будет прекращено."
    "Подробности - в файле NOTICE.md в корне проекта."
    "(Нажмите, чтобы вернуться)"
    return
