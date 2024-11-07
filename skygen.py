import pandas as pd
import plotly.graph_objects as go
from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astropy.time import Time
import astropy.units as u
import pickle
import numpy as np
from messier_catalog import messier_catalog, brightest_stars
from misc_functions import ra_dec_to_degrees

# Функция для получения координат звезды по её номеру
def get_star_coordinates(hip_number, hip_catalog):
    star_data = hip_catalog[hip_catalog['HIP'] == hip_number]
    if not star_data.empty:
        ra = star_data.iloc[0]['_RA.icrs']  # Прямое восхождение
        dec = star_data.iloc[0]['_DE.icrs'] # Склонение
        vmag = star_data.iloc[0]['Vmag'] 
        return ra, dec, vmag # Добавляем звёздную величину
    return None

# Загрузка данных наблюдателя
def get_observer_coordinates(lat, lon, elevation=0):
    return EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=elevation*u.m)

# Преобразование координат звёзд в горизонтальные для наблюдателя
def equatorial_to_horizontal(ra, dec, observer_location, time):
    sky_coord = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')
    altaz = sky_coord.transform_to(AltAz(obstime=time, location=observer_location))
    return altaz.alt.deg, altaz.az.deg
    # return sky_coord.ra.deg, sky_coord.dec.deg

# Загрузка линий созвездий из файла
def load_constellation_lines(filename):
    constellations = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            constellation_name = parts[0]
            stars = list(map(int, parts[2:]))
            if constellation_name not in constellations:
                constellations[constellation_name] = []
            constellations[constellation_name].extend([(stars[i], stars[i + 1]) for i in range(0, len(stars), 2)])
    return constellations

# Преобразование всех линий созвездий в горизонтальные координаты
def constellation_lines_to_horizontal(constellation_lines, hip_catalog, observer_location, time):
    coordinates = {}
    for constellation, star_pairs in constellation_lines.items():
        constellation_coords = []
        for star1, star2 in star_pairs:
            coord1 = get_star_coordinates(star1, hip_catalog)
            coord2 = get_star_coordinates(star2, hip_catalog)
            if coord1 and coord2:
                alt1, az1 = equatorial_to_horizontal(coord1[0], coord1[1], observer_location, time)
                alt2, az2 = equatorial_to_horizontal(coord2[0], coord2[1], observer_location, time)
                constellation_coords.append(((alt1, az1), (alt2, az2)))
        coordinates[constellation] = constellation_coords
    return coordinates

# Функция для вычисления экваториальных координат эклиптики
def ecliptic_to_equatorial(ra_range, tilt=23.5):
    # Преобразуем эклиптические координаты в экваториальные
    # Ра меняется от 0 до 360 градусов, наклон фиксирован
    ecliptic_points = []
    for ra in ra_range:
        dec = tilt * np.sin(np.deg2rad(ra))
        ecliptic_points.append((ra, dec))
    return ecliptic_points

# Создаём данные для небесного экватора
def get_equator_points(ra_range):
    equator_points = []
    for ra in ra_range:
        equator_points.append((ra, 0))
    return equator_points

# Получение всех звёзд для отображения
def get_stars_coordinates(hip_catalog, observer_location, time, mag_limit=7):
    star_coords = []
    for _, star in hip_catalog.iterrows():
        if star['Vmag'] <= mag_limit:  # Фильтруем звёзды по звёздной величине
            ra, dec, mag = star['_RA.icrs'], star['_DE.icrs'], star['Vmag']
            alt, az = equatorial_to_horizontal(ra, dec, observer_location, time)
            star_coords.append((alt, az, mag, star['HIP']))
    return star_coords

# Функция для получения координат объектов Мессье в горизонтальной системе
def get_messier_coordinates(messier_catalog, observer_location, time):
    messier_coords = []
    for obj_name, obj_data in messier_catalog.items():
        ra_str, dec_str = obj_data["ra"], obj_data["dec"]
        ra_deg, dec_deg = ra_dec_to_degrees(ra_str, dec_str)
        alt, az = equatorial_to_horizontal(ra_deg, dec_deg, observer_location, time)
        messier_coords.append((alt, az, obj_name))
    return messier_coords

# Функция для получения координат объектов Мессье в горизонтальной системе
def get_bright_star_coordinates(messier_catalog, observer_location, time):
    bright_star_coordinates = []
    for star in brightest_stars:
        ra_str, dec_str = star["ra"], star["dec"]
        ra_deg, dec_deg = ra_dec_to_degrees(ra_str, dec_str)
        alt, az = equatorial_to_horizontal(ra_deg, dec_deg, observer_location, time)
        bright_star_coordinates.append((alt, az, star["name"]))
    return bright_star_coordinates

def get_great_circle_coordinates(coords, observer_location, time):
    ra_list = []
    dec_list = []
    for ra, dec in coords:
        alt, az = equatorial_to_horizontal(ra, dec, observer_location, time)
        ra_list.append(az)
        dec_list.append(alt)
    return (ra_list, dec_list)

# Функция для отрисовки скайчарта со звёздами и линиями созвездий
def plot_constellations_and_stars_on_skychart(constellation_coordinates, stars, messier, bright_stars, equator_points, ecliptic_points, center_ra, center_dec):
    fig = go.Figure()

    # Отрисовка линий созвездий
    for constellation, lines in constellation_coordinates.items():
        for coord1, coord2 in lines:
            alt1, az1 = coord1
            alt2, az2 = coord2
            fig.add_trace(go.Scattergeo(
                lon=[az1, az2],
                lat=[alt1, alt2],
                mode='lines',
                line=dict(width=0.25, color='black'),
                name=constellation
            ))

    # Отрисовка ярких звёзд
    for alt, az, obj_name in bright_stars:
        fig.add_trace(go.Scattergeo(
            lon=[az],  # Прямое восхождение (долгота)
            lat=[alt],  # Склонение (широта)
            mode='text',
            text=obj_name,
            textposition="top center",
            hoverinfo='text',
            name=obj_name,  # Для идентификации в легенде
            visible='legendonly'  # Скрыть по умолчанию
        ))

    # Отрисовка звёзд
    for alt, az, mag, hip_id  in stars:
        size = 7.01 - mag  # Определяем размер кружка по звёздной величине
        star_info = f"HIP: {hip_id}, Mag: {mag:.2f}"
        fig.add_trace(go.Scattergeo(
            lon=[az],
            lat=[alt],
            mode='markers',
            marker=dict(size=size, color='black', opacity=0.8),
            text=star_info,  # Добавляем информацию о звезде
            hoverinfo='text',  # Отображаем эту информацию при наведении
            showlegend=False
        ))

    # Отрисовка мессье
    for alt, az, obj_name in messier:
        # Добавляем объекты Мессье на график
        fig.add_trace(go.Scattergeo(
            lon=[az],  # Прямое восхождение (долгота)
            lat=[alt],  # Склонение (широта)
            mode='markers+text',
            marker=dict(size=5, color='darkblue', opacity=0.8),
            text=obj_name,
            textposition="top center",
            hoverinfo='text',
            name=obj_name,  # Для идентификации в легенде
            visible='legendonly'  # Скрыть по умолчанию
        ))

    fig.add_trace(go.Scattergeo(
            lon=equator_points[0],
            lat=equator_points[1],
            mode='lines',
            line=dict(width=0.25, color='blue'),
            name='Небесный экватор'
        ))

    fig.add_trace(go.Scattergeo(
            lon=ecliptic_points[0],
            lat=ecliptic_points[1],
            mode='lines',
            line=dict(width=0.25, color='red'),
            name='Эклиптика'
        ))

    fig.add_trace(go.Scattergeo(
            lon=[0, 0],  # Прямое восхождение (долгота)
            lat=[90, -90],  # Склонение (широта)
            mode='markers+text',
            marker=dict(size=5, color='black', opacity=0.8),
            text="P",
            textposition="top center",
            hoverinfo='text',
        ))



    # Настройки графика
    fig.update_geos(projection_type="azimuthal equidistant",
    projection_rotation=dict(lon=center_ra, lat=center_dec),
        showland=False, showcountries=False, showocean=False,
                    showcoastlines=False, showframe=True)
    

    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
    )
    
    with open('skygen_cont.pkl', 'wb') as f:
        pickle.dump(fig, f)

    fig.write_html('contours.html')
    fig.show()

    return fig

# Основная функция для генерации скайчарта
def generate_skychart_with_constellations_and_stars(lat, lon, time_str, hip_catalog, constellationship_file, center_ra, center_dec):
    observer_location = get_observer_coordinates(lat, lon)
    time = Time(time_str)

    local_sidereal_time = time.sidereal_time('mean', longitude=observer_location.lon)

    # Загрузка линий созвездий
    constellation_lines = load_constellation_lines(constellationship_file)

    # Преобразование линий созвездий в горизонтальные координаты
    constellation_coordinates = constellation_lines_to_horizontal(constellation_lines, hip_catalog, observer_location, time)

    # Получение всех объектов
    stars = get_stars_coordinates(hip_catalog, observer_location, time)
    messier = get_messier_coordinates(messier_catalog, observer_location, time)
    bright_stars = get_bright_star_coordinates(brightest_stars, observer_location, time)
    equator_points = get_great_circle_coordinates(get_equator_points(np.linspace(0, 360, 50)), observer_location, time)
    ecliptic_points = get_great_circle_coordinates(ecliptic_to_equatorial(np.linspace(0, 360, 50)), observer_location, time)

    # Отрисовка скайчарта
    return plot_constellations_and_stars_on_skychart(constellation_coordinates, stars, messier, bright_stars, equator_points, ecliptic_points, center_ra, center_dec)

# Пример использования
if __name__ == "__main__":
    # Каталог Hipparcos
    hip_catalog = pd.read_csv("hipparcos_catalog.csv")

    # Файл с линиями созвездий
    constellationship_file = "constellationship.fab"

    # Параметры наблюдателя
    observer_lat = 38 # Пример: широта Москвы
    observer_lon = 280 # Пример: долгота Москвы
    time_str = "2024-09-23 11:47:00"

    # Генерация скайчарта со звёздами и контурами созвездий
    generate_skychart_with_constellations_and_stars(90, 0, time_str, hip_catalog, constellationship_file, observer_lon, observer_lat)