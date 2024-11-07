import asyncio
from telegram import Bot
from datetime import datetime
import os
import re
import glob

async def main():
    # Настройки бота
    bot_token = '7591199768:AAHMBhIS-_OqciDPN8jk4WFn3dhN-1SyAME'  # Замените на ваш токен
    channel_id = '@skygenevrd'     # Замените на юзернейм вашего канала
    bot = Bot(token=bot_token)

    # Путь к папке с файлами
    folder_name = 'skycharts'  # Название папки с файлами
    folder_path = os.path.join(os.getcwd(), folder_name)

    # Проверяем, существует ли папка
    if not os.path.exists(folder_path):
        print(f'Папка {folder_name} не существует.')
        return

    # Шаблон для файлов, которые мы хотим отправлять
    file_pattern = os.path.join(folder_path, 'skychart*.pdf')

    # Получаем список файлов, соответствующих шаблону, и сортируем их
    file_paths = sorted(glob.glob(file_pattern))

    # Проверяем, есть ли файлы в папке
    if not file_paths:
        print(f'В папке {folder_name} нет файлов, соответствующих шаблону.')
        return

    # Файл для хранения последнего отправленного файла
    last_sent_file = 'last_sent.txt'

    # Получаем имена файлов из путей
    file_names = [os.path.basename(path) for path in file_paths]

    # Определяем индекс следующего файла для отправки
    if os.path.exists(last_sent_file):
        with open(last_sent_file, 'r') as f:
            last_sent = f.read().strip()
        try:
            last_index = file_names.index(last_sent)
            next_index = last_index + 1
        except ValueError:
            next_index = 0
    else:
        next_index = 0

    # Проверяем, есть ли следующий файл
    if next_index < len(file_names):
        next_file_name = file_names[next_index]
        next_file_path = file_paths[next_index]
    else:
        print('Все файлы были отправлены.')
        return

    # Извлекаем номер из имени файла
    match = re.search(r'\d+', next_file_name)
    if match:
        number = match.group()
    else:
        number = 'неизвестный номер'

    # Генерируем подпись
    today = datetime.today().strftime('%d.%m.%y')
    caption = f'Скайчарт №{number} от {today}'

    # Отправляем файл
    try:
        with open(next_file_path, 'rb') as f:
            await bot.send_document(chat_id=channel_id, document=f, caption=caption)
        print(f'Файл {next_file_name} успешно отправлен.')
    except Exception as e:
        print(f'Ошибка при отправке файла {next_file_name}: {e}')
        return

    # Обновляем информацию о последнем отправленном файле
    with open(last_sent_file, 'w') as f:
        f.write(next_file_name)


# Запускаем асинхронную функцию
if __name__ == '__main__':
    asyncio.run(main())
    