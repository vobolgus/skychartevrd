import numpy as np
import random
import os
import subprocess
import shutil
import plotly.graph_objects as go  # Правильный импорт Plotly
from astroquery.vizier import Vizier
import ephem
from datetime import datetime

messier_catalog = {
    "M1": {"ra": "05 34 31.97", "dec": "22 00 52.1"},
    "M2": {"ra": "21 33 27.02", "dec": "-00 49 23.7"},
    "M3": {"ra": "13 42 11.62", "dec": "28 22 38.2"},
    "M4": {"ra": "16 23 35.22", "dec": "-26 31 32.7"},
    "M5": {"ra": "15 18 33.22", "dec": "02 04 51.7"},
    "M6": {"ra": "17 40 20.5", "dec": "-32 15 12.0"},
    "M7": {"ra": "17 53 51.1", "dec": "-34 47 34.6"},
    "M8": {"ra": "18 03 37.2", "dec": "-24 23 12"},
    "M9": {"ra": "17 19 11.78", "dec": "-18 30 58.5"},
    "M10": {"ra": "16 57 09.05", "dec": "-04 05 58.8"},
    "M11": {"ra": "18 51 05.08", "dec": "-06 16 12.2"},
    "M12": {"ra": "16 47 14.18", "dec": "-01 56 52.7"},
    "M13": {"ra": "16 41 41.24", "dec": "36 27 36.9"},
    "M14": {"ra": "17 37 36.13", "dec": "-03 14 45.3"},
    "M15": {"ra": "21 29 58.33", "dec": "12 10 01.2"},
    "M16": {"ra": "18 18 48.02", "dec": "-13 48 24.3"},
    "M17": {"ra": "18 20 58.54", "dec": "-16 10 45.1"},
    "M18": {"ra": "18 19 58.47", "dec": "-17 06 07"},
    "M19": {"ra": "17 02 37.69", "dec": "-26 16 04.2"},
    "M20": {"ra": "18 02 42.02", "dec": "-22 58 18.5"},
    "M21": {"ra": "18 04 13.0", "dec": "-22 29 24"},
    "M22": {"ra": "18 36 23.94", "dec": "-23 54 17.1"},
    "M23": {"ra": "17 56 54.0", "dec": "-19 00 06"},
    "M24": {"ra": "18 16 54.98", "dec": "-18 29 57"},
    "M25": {"ra": "18 31 47.0", "dec": "-19 07 00"},
    "M26": {"ra": "18 45 18.0", "dec": "-09 23 00"},
    "M27": {"ra": "19 59 36.34", "dec": "22 43 16.1"},
    "M28": {"ra": "18 24 32.89", "dec": "-24 52 11.3"},
    "M29": {"ra": "20 23 56.0", "dec": "38 32 00"},
    "M30": {"ra": "21 40 22.12", "dec": "-23 10 47.5"},
    "M31": {"ra": "00 42 44.31", "dec": "41 16 09.4"},
    "M32": {"ra": "00 42 41.83", "dec": "40 51 55.3"},
    "M33": {"ra": "01 33 50.89", "dec": "30 39 36.8"},
    "M34": {"ra": "02 42 00.0", "dec": "42 45 00"},
    "M35": {"ra": "06 09 06.0", "dec": "24 20 00"},
    "M36": {"ra": "05 36 18.0", "dec": "34 08 24"},
    "M37": {"ra": "05 52 18.0", "dec": "32 33 12"},
    "M38": {"ra": "05 28 42.0", "dec": "35 51 18"},
    "M39": {"ra": "21 31 48.0", "dec": "48 26 00"},
    "M40": {"ra": "12 22 12.5", "dec": "58 04 59"},
    "M41": {"ra": "06 46 00.0", "dec": "-20 45 00"},
    "M42": {"ra": "05 35 17.3", "dec": "-05 23 28"},
    "M43": {"ra": "05 35 31.4", "dec": "-05 16 02"},
    "M44": {"ra": "08 40 24.0", "dec": "19 41 00"},
    "M45": {"ra": "03 47 00.0", "dec": "24 07 00"},
    "M46": {"ra": "07 41 46.0", "dec": "-14 49 00"},
    "M47": {"ra": "07 36 35.0", "dec": "-14 29 00"},
    "M48": {"ra": "08 13 43.0", "dec": "-05 45 00"},
    "M49": {"ra": "12 29 46.76", "dec": "08 00 01"},
    "M50": {"ra": "07 03 48.0", "dec": "-08 20 00"},
    "M51": {"ra": "13 29 52.7", "dec": "47 11 43"},
    "M52": {"ra": "23 24 48.0", "dec": "61 35 06"},
    "M53": {"ra": "13 12 55.25", "dec": "18 10 05.4"},
    "M54": {"ra": "18 55 03.33", "dec": "-30 28 47.5"},
    "M55": {"ra": "19 39 59.71", "dec": "-30 57 53.1"},
    "M56": {"ra": "19 16 35.52", "dec": "30 11 00.7"},
    "M57": {"ra": "18 53 35.08", "dec": "33 01 45.0"},
    "M58": {"ra": "12 37 43.52", "dec": "11 49 05"},
    "M59": {"ra": "12 42 02.29", "dec": "11 38 49"},
    "M60": {"ra": "12 43 40.0", "dec": "11 33 57"},
    "M61": {"ra": "12 21 55.0", "dec": "04 28 25"},
    "M62": {"ra": "17 01 12.88", "dec": "-30 06 49.2"},
    "M63": {"ra": "13 15 49.3", "dec": "42 01 45"},
    "M64": {"ra": "12 56 43.64", "dec": "21 41 00"},
    "M65": {"ra": "11 18 55.98", "dec": "13 05 32.0"},
    "M66": {"ra": "11 20 14.96", "dec": "12 59 30.0"},
    "M67": {"ra": "08 50 12.0", "dec": "11 48 00"},
    "M68": {"ra": "12 39 27.98", "dec": "-26 44 38.6"},
    "M69": {"ra": "18 31 23.27", "dec": "-32 20 54.1"},
    "M70": {"ra": "18 43 12.17", "dec": "-32 17 30.0"},
    "M71": {"ra": "19 53 46.49", "dec": "18 46 45.1"},
    "M72": {"ra": "20 53 27.74", "dec": "-12 32 14.4"},
    "M73": {"ra": "20 58 55.4", "dec": "-12 38 06"},
    "M74": {"ra": "01 36 41.88", "dec": "15 47 00"},
    "M75": {"ra": "20 06 04.78", "dec": "-21 55 17.5"},
    "M76": {"ra": "01 42 19.8", "dec": "51 34 31"},
    "M77": {"ra": "02 42 40.8", "dec": "-00 00 48"},
    "M78": {"ra": "05 46 45.0", "dec": "00 03 24"},
    "M79": {"ra": "05 24 10.6", "dec": "-24 31 30"},
    "M80": {"ra": "16 17 02.41", "dec": "-22 58 30.6"},
    "M81": {"ra": "09 55 33.2", "dec": "69 03 55"},
    "M82": {"ra": "09 55 52.7", "dec": "69 40 47"},
    "M83": {"ra": "13 37 00.96", "dec": "-29 51 56.2"},
    "M84": {"ra": "12 25 03.73", "dec": "12 53 13"},
    "M85": {"ra": "12 25 24.05", "dec": "18 11 26"},
    "M86": {"ra": "12 26 12.17", "dec": "12 56 44"},
    "M87": {"ra": "12 30 49.42", "dec": "12 23 28"},
    "M88": {"ra": "12 32 00.8", "dec": "14 25 05"},
    "M89": {"ra": "12 35 39.8", "dec": "12 33 23"},
    "M90": {"ra": "12 36 49.8", "dec": "13 09 47"},
    "M91": {"ra": "12 35 26.4", "dec": "14 29 47"},
    "M92": {"ra": "17 17 07.39", "dec": "43 08 09.4"},
    "M93": {"ra": "07 44 30.5", "dec": "-23 51 30"},
    "M94": {"ra": "12 50 53.06", "dec": "41 07 11.2"},
    "M95": {"ra": "10 43 57.7", "dec": "11 42 14"},
    "M96": {"ra": "10 46 45.7", "dec": "11 49 11"},
    "M97": {"ra": "11 14 47.7", "dec": "55 01 08"},
    "M98": {"ra": "12 13 48.30", "dec": "14 54 01.2"},
    "M99": {"ra": "12 18 49.6", "dec": "14 25 18"},
    "M100": {"ra": "12 22 54.9", "dec": "15 49 21"},
    "M101": {"ra": "14 03 12.6", "dec": "54 20 53"},
    "M102": {"ra": "15 06 29.5", "dec": "55 45 48"},
    "M103": {"ra": "01 33 23.0", "dec": "60 39 00"},
    "M104": {"ra": "12 39 59.43", "dec": "-11 37 23.0"},
    "M105": {"ra": "10 47 49.6", "dec": "12 34 53"},
    "M106": {"ra": "12 18 57.5", "dec": "47 18 14"},
    "M107": {"ra": "16 32 31.86", "dec": "-13 03 13.6"},
    "M108": {"ra": "11 11 31.2", "dec": "55 40 25"},
    "M109": {"ra": "11 57 36.0", "dec": "53 22 28"},
    "M110": {"ra": "00 40 22.0", "dec": "41 41 07"}
}

brightest_stars = [
    {"name": "Сириус", "ra": "06 45 08.9", "dec": "-16 42 58", "Vmag": -1.46},
    {"name": "Канопус", "ra": "06 23 57.1", "dec": "-52 41 45", "Vmag": -0.74},
    {"name": "Альфа Центавра", "ra": "14 39 35.9", "dec": "-60 50 07", "Vmag": -0.27},
    {"name": "Арктур", "ra": "14 15 39.7", "dec": "+19 10 57", "Vmag": -0.05},
    {"name": "Вега", "ra": "18 36 56.3", "dec": "+38 47 01", "Vmag": 0.03},
    {"name": "Капелла", "ra": "05 16 41.4", "dec": "+45 59 53", "Vmag": 0.08},
    {"name": "Ригель", "ra": "05 14 32.3", "dec": "-08 12 06", "Vmag": 0.12},
    {"name": "Процион", "ra": "07 39 18.1", "dec": "+05 13 30", "Vmag": 0.34},
    {"name": "Ахернар", "ra": "01 37 42.9", "dec": "-57 14 12", "Vmag": 0.46},
    {"name": "Бетельгейзе", "ra": "05 55 10.3", "dec": "+07 24 25", "Vmag": 0.50},
    {"name": "Хадар", "ra": "14 03 49.4", "dec": "-60 22 23", "Vmag": 0.61},
    {"name": "Альтаир", "ra": "19 50 47.0", "dec": "+08 52 00", "Vmag": 0.76},
    {"name": "Акрукс", "ra": "12 26 33.1", "dec": "-63 05 57.7", "Vmag": 0.77},
    {"name": "Альдебаран", "ra": "04 35 55.2", "dec": "+16 30 33", "Vmag": 0.85},
    {"name": "Антарес", "ra": "16 29 24.4", "dec": "-26 25 55", "Vmag": 0.96},
    {"name": "Спика", "ra": "13 25 11.6", "dec": "-11 09 41", "Vmag": 0.98},
    {"name": "Поллукс", "ra": "07 45 19.4", "dec": "+28 01 34", "Vmag": 1.14},
    {"name": "Фомальгаут", "ra": "22 57 39.0", "dec": "-29 37 20", "Vmag": 1.16},
    {"name": "Денеб", "ra": "20 41 25.9", "dec": "+45 16 49", "Vmag": 1.25},
    {"name": "Мимоза", "ra": "12 47 40.8", "dec": "-59 41 21.2", "Vmag": 1.25},
    {"name": "Регул", "ra": "10 08 22.3", "dec": "+11 58 02", "Vmag": 1.35},
    {"name": "Адара", "ra": "06 58 37.0", "dec": "-28 58 04", "Vmag": 1.50},
    {"name": "Кастор", "ra": "07 34 34.7", "dec": "+31 53 12.7", "Vmag": 1.57},
    {"name": "Гакрукс", "ra": "12 31 07.8", "dec": "-57 06 54.1", "Vmag": 1.63},
    {"name": "Шаула", "ra": "17 33 36.5", "dec": "-37 06 13", "Vmag": 1.62},
    {"name": "Алиот", "ra": "12 54 01.7", "dec": "+55 57 35", "Vmag": 1.76},
    {"name": "Мирфак", "ra": "03 24 19.4", "dec": "+49 51 40", "Vmag": 1.79},
    {"name": "Дубхе", "ra": "11 03 43.7", "dec": "+61 45 03", "Vmag": 1.79},
    {"name": "Альциона", "ra": "03 47 29.1", "dec": "+24 06 19", "Vmag": 2.85},
    {"name": "Садалмелик", "ra": "22 05 47.0", "dec": "-00 19 11", "Vmag": 2.96},
    {"name": "Альдерамин", "ra": "21 18 33.8", "dec": "+62 35 08", "Vmag": 2.44},
    {"name": "Меридиана", "ra": "19 06 14.9", "dec": "-37 12 45", "Vmag": 1.85},
    {"name": "Альнаир", "ra": "22 08 13.6", "dec": "-46 57 39", "Vmag": 1.74}
]

# Преобразуем радианы в часы и минуты
def rad_to_hours_minutes(rad):
    hours = rad * 12.0 / ephem.pi  # Преобразуем радианы в часы
    h = int(hours)  # Целая часть - это часы
    m = int((hours - h) * 60)  # Дробная часть преобразуется в минуты
    return h, m

# Функция для вычисления звёздного времени (LST)
def get_local_sidereal_time(observer):
    # Гринвичское звёздное время (GST)
    lst = observer.sidereal_time()
    
    # # Местное звёздное время (LST)
    # lst = gst - observer.lon  # Долгота автоматически учитывается в радианах
    # print(observer.lon, gst, lst)
    return lst

def get_brightest_stars_above_horizon(observer):
    visible_stars = []
    for star in brightest_stars:
        # Создаем объект звезды с указанными координатами
        star_obj = ephem.FixedBody()
        star_obj._ra = ephem.hours(star['ra'])
        star_obj._dec = ephem.degrees(star['dec'])
        star_obj.compute(observer)

        # Если звезда выше горизонта, добавляем её в список
        if star_obj.alt > 0:
            visible_stars.append({
                "name": star['name'],
                "alt": star_obj.alt,
                "az": star_obj.az
            })

    # Если видимых звёзд больше 5, выбираем случайные 5
    if len(visible_stars) > 9:
        visible_stars = random.sample(visible_stars, 9)

    return visible_stars

# Функция для вычисления объектов каталога Мессье над горизонтом
def get_messier_above_horizon(observer):
    visible_messier = []
    for obj_name, coords in messier_catalog.items():
        # Создаем объект Messier с указанными координатами
        messier_obj = ephem.FixedBody()
        messier_obj._ra = ephem.hours(coords['ra'])
        messier_obj._dec = ephem.degrees(coords['dec'])
        messier_obj.compute(observer)
        
        # Если объект выше горизонта, добавляем его в список
        if messier_obj.alt > 0:
            visible_messier.append({
                "name": obj_name,
                "alt": messier_obj.alt,
                "az": messier_obj.az
            })
        
        # Если объектов больше 10, выбираем случайные 10
    if len(visible_messier) > 9:
        visible_messier = random.sample(visible_messier, 9)
    
    return visible_messier

# Функция для преобразования в стереографическую проекцию с сохранением полярных координат
def stereographic_projection_polar(alt):
    r = np.pi / 2 - alt  # Преобразуем высоту в угловое расстояние от зенита
    r_stereo = np.tan(r / 2)  # Преобразование в стереографические координаты
    return r_stereo

# Функция для генерации скайчарта с использованием Plotly
def generate_sky_chart(observer_lat, observer_lon, date_time, output_filename="sky_chart_plotly.html", save_as_png=False, png_filename="sky_chart_stereo_polar.png"):
    # Устанавливаем местоположение наблюдателя
    observer = ephem.Observer()
    observer.lat = str(observer_lat)
    observer.lon = str(observer_lon)
    observer.date = date_time

    # Загрузка звёзд из Bright Star Catalog
    v = Vizier(row_limit=-1)
    print("Запрашиваем каталог V/50 для ярких звёзд...")
    result = v.query_constraints(catalog="V/50", Vmag="<6.0")
    
    # Проверим, вернулись ли результаты
    if len(result) == 0:
        print("Запрос не вернул данных. Проверьте правильность каталога или условий.")
        return
    else:
        stars = result[0]

    # Массивы для хранения данных звезд
    azimuths = []
    altitudes = []
    magnitudes = []

    # Преобразуем координаты звёзд в азимут и высоту
    for star in stars:
        try:
            # Прямое восхождение и склонение
            ra = ephem.hours(star['RAJ2000'])  # Преобразуем в радианы
            dec = ephem.degrees(star['DEJ2000'])  # Преобразуем в радианы
            mag = star['Vmag']
        except (ValueError, KeyError):
            continue  # Пропускаем звезды с некорректными данными

        # Преобразование в альт-аз координаты
        star_coords = ephem.FixedBody()
        star_coords._ra = ra
        star_coords._dec = dec
        star_coords.compute(observer)
        alt = star_coords.alt
        az = star_coords.az
        
        # Если звезда видна на небе (над горизонтом)
        if alt > 0:
            azimuths.append(az)
            altitudes.append(stereographic_projection_polar(alt))
            magnitudes.append(mag)

    # Преобразование значений азимута и высоты в градусы для Plotly


    rotate_angle = random.randint(0, 360)
    azimuths_deg = [(np.degrees(a) + rotate_angle) % 360 for a in azimuths]
    # altitudes_deg = [90 - np.degrees(a) for a in altitudes]  # Инвертируем высоту
    altitudes_deg = altitudes  # Инвертируем высоту

    # Размеры точек на основе звездной величины (чем меньше величина, тем больше точка)
    sizes = [6 - mag for mag in magnitudes]

    # Создаем скайчарт с Plotly
    fig = go.Figure()

    # Добавляем круг для обводки области отрисовки
    # Создаем окружность с максимальным радиусом
    circle_r = [1] * 360  # Радиус окружности
    circle_theta = np.linspace(0, 360, 360)  # Азимут от 0 до 360

    fig.add_trace(go.Scatterpolar(
        r=circle_r,
        theta=circle_theta,
        mode='lines',
        line=dict(color='black', width=2),  # Устанавливаем черную линию для обвода
        showlegend=False  # Убираем отображение легенды
    ))

    fig.add_trace(go.Scatterpolar(
        r=altitudes_deg,
        theta=azimuths_deg,
        mode='markers',
        marker=dict(
            size=sizes,  # Устанавливаем размер на основе величины
            color='black',
            opacity=1,
            line=dict(width=0)
        )
    ))

    # # Получаем 5 случайных видимых звёзд
    # visible_stars = get_brightest_stars_above_horizon(observer)

    # # Выводим названия звёзд
    # for star in visible_stars:
    #     print(star['name'])

    # Добавляем объекты Мессье, которые находятся над горизонтом
    visible_messier = get_messier_above_horizon(observer)
    if visible_messier:
        # random_sample = random.sample(visible_messier, 10)
        # random_sample = sorted(random_sample, key=lambda obj: int(obj['name'][1:]))
        # print(*[obj['name'] for obj in random_sample]) 
        r_messier = []
        theta_messier = []
        for obj in visible_messier:
            r_messier.append(stereographic_projection_polar(obj['alt']))  # Преобразуем высоту в стереографические координаты
            theta_messier.append(np.degrees(obj['az']))  # Азимут в градусах

        # # Добавляем объекты Мессье на график с другим стилем
        # fig.add_trace(go.Scatterpolar(
        #     r=r_messier,
        #     theta=theta_messier,
        #     mode='markers+text',
        #     marker=dict(
        #         size=5,  # Размер маркера для объектов Мессье
        #         color='white',
        #         opacity=1,
        #         symbol='square',
        #         line=dict(width=2, color='red')  # Красная обводка для объектов Мессье
        #     ),
        #     text=[obj['name'] for obj in visible_messier],  # Добавляем имена объектов Мессье
        #     textposition='top center',
        #     showlegend=False
        # ))

    # Настройки графика
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 1]),  # Высота до 90 градусов
            angularaxis=dict(visible=False),
            bgcolor='white'
        ),
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),  # Минимальные отступы
        width=800,  # Устанавливаем ширину
        height=800,  # Устанавливаем высоту
        paper_bgcolor='white',  # Фон всего графика белый
        plot_bgcolor='red',
    )

    # Сохранение в файл
    fig.write_html(output_filename)
    print(f"График сохранён как {output_filename}")

    # Опциональное сохранение в PNG
    if save_as_png:
        fig.write_image(png_filename, format='png', scale=2, width=800, height=800, engine="kaleido")
        print(f"График сохранён как {png_filename} в формате PNG")

# Функция для генерации LaTeX файла
def generate_latex_report(observer_lat, observer_lon, date_time, sky_chart_filename, output_filename="sky_chart_report.tex", number=1):
    # Генерация скайчарта
    generate_sky_chart(observer_lat, observer_lon, date_time, save_as_png=True, png_filename=sky_chart_filename)

    # Получаем 10 случайных объектов Мессье
    observer = ephem.Observer()
    observer.lat = str(observer_lat)
    observer.lon = str(observer_lon)
    observer.date = date_time
    visible_messier = get_messier_above_horizon(observer)

    # Получаем 5 случайных ярких звёзд
    visible_stars = get_brightest_stars_above_horizon(observer)

    # Получаем местное звёздное время
    lst = get_local_sidereal_time(observer)

    # Преобразуем в часы и минуты
    hours, minutes = rad_to_hours_minutes(lst)

    # Генерация содержимого LaTeX
    latex_content = r"""\documentclass{./SAS-class-skygen}
    
    \newcommand{\hwnum}{Сборная Москвы}
	\newcommand{\subject}{№""" + str(number) + r"""}
	\newcommand{\skykey}{""" + str(round(observer_lat, 2)) + ' ' + f"{hours:02d}:{minutes:02d}" + r"""}
    
    \begin{document}
    
	\begin{center}
		\large\textbf{Пользовательский скайчарт №""" + str(number) + r"""}
	\end{center}

	\begin{enumerate}
		\item Обозначьте точку зенита символом \boldsans{Z} и стороны света как \boldsans{N}, \boldsans{E}, \boldsans{S}, \boldsans{W}.
		\item Обозначьте полюс мира символом \boldsans{P}.
		\item Обозначьте точку весны символом \Aries. Или же точку осени символом \Libra.
		\item Проведите большие круги небесного экватора и эклиптики.
		\item Рассчитайте звёздное время скайчарта: \rule{2cm}{0.4pt}
		\item Определите широту места съёмки: \rule{2cm}{0.4pt}
		\item Проведите контуры всех видимых созвездий, а также напишите их обозначения по Байеру.
		\item Отметьте на скайчарте небесные объекты, приведённые в таблице ниже.
	\end{enumerate}
	
    \vspace{0.5cm}

    \begin{table}[h!]
    \centering
    \begin{tabular}{ccc}
    \multicolumn{3}{c}{\textbf{Звёзды}} \\ """ 

    counter = 1
    for star in visible_stars:
        if counter % 3 != 0: latex_content += star["name"] + " & "
        else: latex_content += star["name"] + r" \\" + '\n'
        counter += 1

    latex_content += "\n" + r"""\end{tabular}
    \hfill
    \begin{tabular}{ccc}
    \multicolumn{3}{c}{\textbf{Объекты Мессье}} \\ """

    counter = 1
    for obj in visible_messier:
        if counter % 3 != 0: latex_content += obj["name"] + " & "
        else: latex_content += obj["name"] + r" \\" + '\n'
        counter += 1

    latex_content += "\n" + r"""\end{tabular}
    \end{table}
	
	\vspace{0.5cm}
    \begin{center}
    \includegraphics[width=\textwidth]{"""
    latex_content += sky_chart_filename + r"""}
    \end{center}
    
    \end{document}
    """

    # Сохраняем LaTeX файл
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(latex_content)

    print(f"LaTeX отчёт сохранён как {output_filename}")

# Функция для компиляции LaTeX файла в PDF
def compile_latex_to_pdf(tex_filename, output_directory, pdf_destination):
    try:
        # Проверяем, существует ли папка для выходных файлов, и создаём её, если она не существует
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        if not os.path.exists(pdf_destination):
            os.makedirs(pdf_destination)
        # Вызываем pdflatex для компиляции .tex файла в PDF
        with open(os.devnull, 'w') as FNULL:
            # Компилируем LaTeX файл, указывая папку для выходных файлов, подавляя вывод
            print(f"Компиляция {tex_filename} (сообщения подавлены)...")
            subprocess.run(["pdflatex",f"-output-directory={output_directory}", tex_filename],
                stdout=FNULL, stderr=FNULL, check=True)
            # Определяем базовое имя файла (без расширения)
            base_filename = os.path.splitext(os.path.basename(tex_filename))[0]
            pdf_filename = base_filename + ".pdf"

            # Полный путь к PDF-файлу в папке output
            pdf_filepath = os.path.join(output_directory, pdf_filename)

            # Проверяем, существует ли PDF файл и перемещаем его в папку назначения
            if os.path.exists(pdf_filepath):
                destination_filepath = os.path.join(pdf_destination, pdf_filename)
                shutil.move(pdf_filepath, destination_filepath)
                print(f"PDF файл перемещён в {destination_filepath}")
            else:
                print(f"PDF файл {pdf_filename} не найден в папке {output_directory}")
        print(f"Успешно скомпилирован файл: {tex_filename}")
    except subprocess.CalledProcessError:
        print(f"Ошибка при компиляции {tex_filename}")

def generate_skychart(start, n=1, user_time=False, user_lat=False):
    for i in range(start, n+start):
        if user_time and user_lat:
            observer_lat = user_lat
            user_time = list(map(int, user_time.split(':')))
            observer_lon = user_time[0] * 15 + user_time[1] / 4
        else:
            observer_lat = random.randrange(4000, 5000) / 100
            observer_lon = random.randrange(0, 360)
        date_time = f'2024/09/23 23:47:00'
        sky_chart_filename = f"./pics/skychart{i}.png"
        tex_filename = f"./reports/skychart{i}.tex"
        output_directory = 'trash'
        pdf_destination = 'skycharts'

        generate_latex_report(observer_lat, observer_lon, date_time, sky_chart_filename, tex_filename, i)
        compile_latex_to_pdf(tex_filename, output_directory, pdf_destination)
