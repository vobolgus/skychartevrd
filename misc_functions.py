import ephem
import random

# Функция для преобразования RA, Dec в градусы
def ra_dec_to_degrees(ra_str, dec_str):
    # Преобразуем RA
    ra_parts = list(map(float, ra_str.split()))
    ra_degrees = (ra_parts[0] + ra_parts[1] / 60 + ra_parts[2] / 3600) * 15  # RA в часах, переводим в градусы

    # Преобразуем Dec
    dec_parts = list(map(float, dec_str.split()))
    sign = -1 if '-' in dec_str else 1
    dec_degrees = sign * (abs(dec_parts[0]) + dec_parts[1] / 60 + dec_parts[2] / 3600)  # Dec уже в градусах

    return ra_degrees, dec_degrees

# Функция для изменения видимости объектов Мессье по запросу
def update_messier_visibility(fig, messier_objects_to_show):
    for trace in fig.data:
        if trace.name in messier_objects_to_show:
            trace.visible = True  # Показать

# Преобразуем радианы в часы и минуты
def deg_to_hours_minutes(rad):
    hours = rad * 12.0 / 180  # Преобразуем радианы в часы
    h = int(hours)  # Целая часть - это часы
    m = int((hours - h) * 60)  # Дробная часть преобразуется в минуты
    return h, m

def get_brightest_stars_above_horizon(observer, brightest_stars_catalog):
    visible_stars = []
    for star in brightest_stars_catalog:
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
def get_messier_above_horizon(observer, messier_catalog):
    visible_messier = []
    for obj_name, coords in messier_catalog.items():
        # Создаем объект Messier с указанными координатами
        messier_obj = ephem.FixedBody()
        messier_obj._ra = ephem.hours(coords['ra'])
        messier_obj._dec = ephem.degrees(coords['dec'])
        messier_obj.compute(observer)
        
        # Если объект выше горизонта, добавляем его в список
        if messier_obj.alt > 1/57.3:
            visible_messier.append({
                "name": obj_name,
                "alt": messier_obj.alt,
                "az": messier_obj.az
            })
        
        # Если объектов больше 10, выбираем случайные 10
    if len(visible_messier) > 9:
        visible_messier = random.sample(visible_messier, 9)

    return visible_messier