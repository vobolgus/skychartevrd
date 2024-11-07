import pickle
import plotly.graph_objects as go
from messier_catalog import messier_catalog
from misc_functions import ra_dec_to_degrees, update_messier_visibility
from rotate_png import rotate_png
import random

# Функция для загрузки сохранённого графика, изменения центра и сохранения PNG
def generate_png(center_ra=0, center_dec=0, output_filename="updated_sky_chart.png", contours=False, messier_objects=None):
    # Загружаем сохранённый объект Figure
    if contours:
        with open('skygen_cont.pkl', 'rb') as f:
            fig = pickle.load(f)
    else:
        with open('skygen.pkl', 'rb') as f:
            fig = pickle.load(f)
    # Изменяем параметры центра проекции (RA и Dec)
    fig.update_geos(
        projection_rotation=dict(lon=360-center_ra, lat=center_dec)  # Центрируем график по новым значениям
    )
    # Если переданы объекты для отображения, показываем только их
    if messier_objects:
        update_messier_visibility(fig, messier_objects)
    # Сохраняем изменённый график как PNG
    fig.write_image(output_filename, format="png", scale=2, width=800, height=800)
    rotate_png(output_filename, random.randint(0, 360))



    # print(f"График с новыми параметрами сохранён как {output_filename}")

# Пример вызова: изменить центр на RA=90 и Dec=45, сохранить как PNG
# generate_png(center_ra=280, center_dec=38, output_filename="skychart.png", contours=False)