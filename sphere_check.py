import numpy as np
from scipy.spatial import ConvexHull

# Функция для преобразования декартовых координат обратно в экваториальные
def cartesian_to_equatorial(cartesian_coords):
    x, y, z = cartesian_coords
    
    # Склонение
    dec = np.degrees(np.arcsin(z))
    
    # Прямое восхождение
    ra = np.degrees(np.arctan2(y, x))
    if ra < 0:
        ra += 360  # Убедимся, что RA в диапазоне [0, 360]
    
    # Прямое восхождение переводим в часы (360 градусов = 24 часа)
    ra_hours = ra / 15
    
    return ra_hours, dec

# Функция для преобразования экваториальных координат (RA, Dec) в декартовы координаты
def equatorial_to_cartesian(ra, dec):
    ra_rad = np.radians(ra)   # Прямое восхождение в радианы
    dec_rad = np.radians(dec)  # Склонение в радианы
    
    x = np.cos(dec_rad) * np.cos(ra_rad)
    y = np.cos(dec_rad) * np.sin(ra_rad)
    z = np.sin(dec_rad)
    
    return np.array([x, y, z])

# Основная функция для проверки, могут ли звезды лежать в одной полусфере
def check_half_sphere(stars):
    # Преобразуем экваториальные координаты в декартовы координаты
    points = np.array([equatorial_to_cartesian(ra, dec) for ra, dec in stars])
    
    # Строим выпуклую оболочку точек
    hull = ConvexHull(points)
    
    # Для каждой грани выпуклой оболочки проверяем, лежат ли все точки по одну сторону от грани
    for simplex in hull.simplices:
        # Векторы, образующие грань
        p1 = points[simplex[0]]
        p2 = points[simplex[1]]
        p3 = points[simplex[2]]
        
        # Нормаль к грани
        normal = np.cross(p2 - p1, p3 - p1)
        normal = normal / np.linalg.norm(normal)  # Нормируем вектор
        
        # Проверяем, с какой стороны нормали лежат все точки
        signs = np.dot(points, normal)
        if np.all(signs >= 0) or np.all(signs <= 0):
            # Если все точки лежат по одну сторону
            return True, normal
    
    # Если не нашли такую грань, значит, звезды не могут лежать в одной полусфере
    return False, None

# Пример использования:
# Задаем звезды их экваториальными координатами (RA в часах, Dec в градусах)
stars = [
    (19 * 15 + 30 / 4, 28),   # Прямое восхождение 0 часов, склонение 0 градусов
    (19 * 15 + 40 / 4, 3.5),  # Прямое восхождение 6 часов, склонение 45 градусов
    (0 * 15 + 55 / 4, -48.5), # Прямое восхождение 12 часов, склонение -45 градусов
    (19 * 15 + 36 / 4, -65.5),  # Прямое восхождение 18 часов, склонение 30 градусов
    (22 * 15 + 30 / 4, -46),    # Прямое восхождение 1 час, склонение 60 градусов
    (23 * 15 + 46 / 4, -66),
    (5 * 15 + 51 / 4, -35),
    (16 * 15 + 8 / 4, -75),
    (12 * 15 + 26 / 4, -18.5)
]

exists, pole_cartesian = check_half_sphere(stars)
if exists:
    ra_hours, dec = cartesian_to_equatorial(pole_cartesian)
    print(f"Полусфера существует. Полюс: RA = {ra_hours:.2f} часов, Dec = {dec:.2f} градусов.")
else:
    print("Полусферы, содержащей все звезды, не существует.")