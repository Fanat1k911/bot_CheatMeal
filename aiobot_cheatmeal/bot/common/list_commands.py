from aiogram.types import BotCommand

cmds = [
    BotCommand(command='start', description='Запуск/перезапуск бота'),
    BotCommand(command='staff', description='Коллектив сегодня'),
    BotCommand(command='status', description='Получить отчет дня'),
    BotCommand(command='about', description='О Нас'),
    BotCommand(command='help', description='Помощь'),
]
