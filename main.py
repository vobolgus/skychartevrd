from generate_report import generate_latex_report
from compile_report import compile_latex_to_pdf
import random

def generate_skychart(start, n=1, user_time=False, user_lat=False):
    for i in range(start, n+start):
        if user_time and user_lat:
            observer_lat = user_lat
            user_time = list(map(int, user_time.split(':')))
            observer_lon = user_time[0] * 15 + user_time[1] / 4
        else:
            observer_lat = random.randrange(-900, 900) / 10
            observer_lon = random.randrange(0, 360)
        date_time = f'2024/09/23 23:47:00'
        skychart_filename = f"./pics/skychart{i}.png"
        tex_filename = f"./reports/skychart{i}.tex"
        output_directory = 'trash'
        pdf_destination = 'skycharts'

        generate_latex_report(observer_lat, observer_lon, skychart_filename, output_filename=tex_filename, number=i, contours=False)
        compile_latex_to_pdf(tex_filename, output_directory, pdf_destination)

generate_skychart(41, 20)
