from genetate_skychart import generate_skychart
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os
import subprocess
import json
import shutil
import logging
import random
from PyPDF2 import PdfMerger

# Логирование для отладки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего бота
TOKEN = '6970617362:AAHzG9nFVb1SAq2u_3d6tmip-Gl5N81qAv4'  # Укажите реальный токен

# Путь для хранения информации о сгенерированных скайчартах и текущем номере
CHARTS_DIR = "./generated_charts"
CURRENT_NUMBER_FILE = os.path.join(CHARTS_DIR, "current_number.json")

# Создание директории для хранения скайчартов, если её ещё нет
if not os.path.exists(CHARTS_DIR):
    os.makedirs(CHARTS_DIR)

# Инициализация или загрузка текущего номера скайчарта
def get_current_number():
    # Проверяем наличие файла
    if os.path.exists(CURRENT_NUMBER_FILE):
        with open(CURRENT_NUMBER_FILE, 'r') as f:
            try:
                data = json.load(f)
                return data.get("current_number", 0)
            except json.JSONDecodeError:
                # Если файл пуст или повреждён, инициализируем его значением 0
                return 0
    else:
        return 0

# Сохранение обновленного номера скайчарта
def save_current_number(current_number):
    with open(CURRENT_NUMBER_FILE, 'w') as f:
        json.dump({"current_number": current_number}, f)

# Загрузка параметров скайчарта по номеру
def load_skychart_params(number):
    try:
        with open(os.path.join(CHARTS_DIR, f"sky_chart_{number}.json"), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


# Сохранение параметров скайчарта в файл с собственным номером
def save_skychart_params(number, observer_lat, observer_lon, visible_messier_names, visible_stars):
    chart_params = {
        "observer_lat": observer_lat,
        "observer_lon": observer_lon,
        "messier": visible_messier_names,
        "stars": visible_stars
    }
    
    with open(os.path.join(CHARTS_DIR, f"sky_chart_{number}.json"), 'w') as f:
        json.dump(chart_params, f)


# Функция для объединения нескольких PDF-файлов
def merge_pdfs(pdf_list, output_pdf):
    merger = PdfMerger()

    for pdf in pdf_list:
        merger.append(pdf)

    # Записываем объединённый файл
    with open(output_pdf, 'wb') as f:
        merger.write(f)

# Основная функция для отправки сгенерированных скайчартов
async def send_skychart(update: Update, context: CallbackContext, observer_lat_list, observer_lon_list, ansnum=None):
    chat_id = update.message.chat_id

    # Параметры для отчёта
    output_directory = f"./reports_{chat_id}"
    pdf_filenames = []  # Список для хранения путей к PDF файлам

    # Создаём директорию заранее, если она не существует
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if ansnum:
        try:
            chart_params = load_skychart_params(ansnum)

            if chart_params:
                await update.message.reply_text(f"Скайчарт с номером {ansnum} загружается...")
                
                observer_lat = chart_params["observer_lat"]
                observer_lon = chart_params["observer_lon"]
                messier = chart_params["messier"]
                stars = chart_params["stars"]

                generate_skychart(observer_lat, observer_lon, f'{output_directory}/skychart{ansnum}ans.png', f'{output_directory}/skychart{ansnum}ans.tex', output_directory, ansnum, True, messier, stars)
                pdf_filename = f"{output_directory}/skychart{ansnum}ans.pdf"
            
                if os.path.exists(pdf_filename):
                    await context.bot.send_document(chat_id=chat_id, document=open(pdf_filename, 'rb'))
                else:
                    await update.message.reply_text("Ошибка: объединённый PDF не найден.")

                # Очистка файлов
                return

            else:
                await update.message.reply_text(f"Ошибка: скайчарт с номером {chart_number} не найден.")
                return
        except ValueError:
            await update.message.reply_text("Ошибка: Номер скайчарта должен быть целым числом.")
            return

    sent_message = await update.message.reply_text(f"Начало компиляции {len(observer_lat_list)} скайчартa(ов)")

    # Генерация нескольких PDF-файлов
    for i, (observer_lat, observer_lon) in enumerate(zip(observer_lat_list, observer_lon_list)):
        tex_filename = f"{output_directory}/sky_chart_report_{chat_id}_{i}.tex"
        pdf_filename = f"{output_directory}/sky_chart_report_{chat_id}_{i}.pdf"
        skychart_filename = f"{output_directory}/sky_chart_{chat_id}_{i}.png"
        pdf_filenames.append(pdf_filename)

        # Получение текущего номера скайчарта и его инкремент
        current_number = get_current_number() + 1
        save_current_number(current_number)
        visible_messier_names, visible_stars = generate_skychart(observer_lat, observer_lon, skychart_filename, tex_filename, output_directory, current_number, False)
        save_skychart_params(current_number, observer_lat, observer_lon, visible_messier_names, visible_stars)
        
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=sent_message.message_id)
        sent_message = await update.message.reply_text(f"Готово {i+1} из {len(observer_lat_list)}")

    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=sent_message.message_id)
    # Объединение всех сгенерированных PDF в один файл
    combined_pdf_filename = f"{output_directory}/skychartevrd.pdf"
    merge_pdfs(pdf_filenames, combined_pdf_filename)

    # Отправка объединённого PDF-файла пользователю
    if os.path.exists(combined_pdf_filename):
        await context.bot.send_document(chat_id=chat_id, document=open(combined_pdf_filename, 'rb'))
    else:
        await update.message.reply_text("Ошибка: объединённый PDF не найден.")

    # Очистка файлов
    shutil.rmtree(output_directory)

async def generate_init(update: Update, context: CallbackContext) -> None:
    args = list(context.args)
    rep_factor = 1

    if len(args) == 0:
        await generate_random_skychart_pdf(update, context)
        return

    if args[0] == 'multi':
        try:
            rep_factor = int(args[1])
            if rep_factor >= 5:
                await update.message.reply_text("Извините, на время запуса бота количество генерируемых скайчартов в режиме multi ограничено 4.")
                return
            args = args[2:]
        except:
            await update.message.reply_text("Извините, в режиме multi требуется указать целое число желаемых скайчартов.\nПример: /generate multi 5")
            return

    # Проверка на наличие аргументов
    if len(args) == 0:
        await generate_random_skychart_pdf(update, context, rep_factor)
        return
    if args[0] == 'ans':
        if len(args) != 2:
            await update.message.reply_text("Извините, опция coords требует ровно два аргумента.\nПример: /generate coords 55.7558 12:00")
            return
        else:
            if rep_factor != 1:
                await update.message.reply_text("Предупреждение, режим multi не работает для опции ans. Будет сгенерирован один скайчарт.")
            await generate_skychart_solution(update, context, args[1])
            return
    if args[0] == 'coords':
        if len(args) != 3:
            await update.message.reply_text("Извините, опция coords требует ровно два аргумента.\nПример: /generate coords 55.7558 12:00")
            return
        else:
            if rep_factor != 1:
                await update.message.reply_text("Предупреждение, режим multi не работает для опции coords. Будет сгенерирован один скайчарт.")
            await generate_skychart_with_args(update, context, args[1], args[2])
            return
    if args[0] == 'in_range':
        if len(args) != 3:
            await update.message.reply_text("Извините, опция in_range требует ровно два аргумента.\nПример: /generate in_range -30 50")
            return
        else:
            await generate_random_skychart_in_range(update, context, args[1], args[2], rep_factor)
            return
    return
    
async def generate_random_skychart_pdf(update: Update, context: CallbackContext, rep=1) -> None:
    # Параметры для отчёта
    observer_lat = [random.randrange(-90,90) for i in range(rep)]
    observer_lon = [random.randrange(0,360) for i in range(rep)]

    await send_skychart(update, context, observer_lat, observer_lon)

async def generate_skychart_with_args(update: Update, context: CallbackContext, user_lat, user_time) -> None:
    try:
        # Проверка валидности широты (она должна быть числом)
        observer_lat = [float(user_lat)]

        # Проверка валидности времени (формат HH:MM)
        user_time = list(map(int, user_time.split(':')))
        if len(user_time) != 2 or user_time[0] < 0 or user_time[0] > 23 or user_time[1] < 0 or user_time[1] > 59:
            await update.message.reply_text("Неправильный формат времени. Пожалуйста, используйте формат HH:MM.")
            return
        
        # Рассчитываем долготу на основе времени (15 градусов на час)
        observer_lon = [user_time[0] * 15 + user_time[1] / 4]

        await send_skychart(update, context, observer_lat, observer_lon)  
    except ValueError:
        await update.message.reply_text("Ошибка: Широта или время заданы неверно. Пример: /generate 55.7558 12:00")

async def generate_random_skychart_in_range(update: Update, context: CallbackContext, dec_min, dec_max, rep) -> None:
    try:
        # Параметры для отчёта
        observer_lat = [random.randrange(int(dec_min),int(dec_max)) for i in range(rep)]
        observer_lon = [random.randrange(0,360) for i in range(rep)]

        await send_skychart(update, context, observer_lat, observer_lon)
    except ValueError:
        await update.message.reply_text("Ошибка: границы заданы неверно. Пример: /generate in_range -30 50")

async def generate_skychart_solution(update: Update, context: CallbackContext, number) -> None:
    try:
        await send_skychart(update, context, 0, 0, number)
    except ValueError:
        await update.message.reply_text("Ошибка: некорректный номер")


# Функция для команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Я бот для генерации скайчартов. Используй команду /help чтобы узнать что я умею.")

async def help_list(update: Update, context: CallbackContext) -> None: 
    await update.message.reply_text("""Список доступных команд:
    1. /start
    2. /help
    3. /generate

Команада /generate поддерживает несколько опций:
1. Случайный скайчарт. Не требуется никаких дополнительных аргументов.
Пример:
    /generate
2. Случайный скайчарт в некотором промежутке широт.
Пример:
    /generate in_range -40 60
3. Скайчарт по конкретной широте и звёздному времени
Пример:
    /generate coords 38.78 18:37

Дополнительно доступен режим multi. Для перехода в этот режим перед выбором опции напишите multi и количество желаемых скайчартов.
Пример:
    /generate multi 3 in_range -40 60
    """)


# Основная функция для запуска бота
def main():
    # Создаем экземпляр приложения
    application = Application.builder().token(TOKEN).build()

    # Регистрируем команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_list))
    application.add_handler(CommandHandler("generate", generate_init))

    # Запуск бота с polling
    application.run_polling()

if __name__ == '__main__':
    main()