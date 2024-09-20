from generate_png import generate_png
from messier_catalog import messier_catalog, brightest_stars
import ephem
from misc_functions import get_messier_above_horizon, get_brightest_stars_above_horizon, deg_to_hours_minutes

# Функция для генерации LaTeX файла
def generate_latex_report(observer_lat, observer_lon, skychart_filename, output_filename="sky_chart_report.tex", number=1, contours=False, messier=None, stars=None):
    # Получаем 10 случайных объектов Мессье
    observer = ephem.Observer()
    observer.lat = str(observer_lat)
    observer.lon = str(observer_lon)
    observer.date = "2024-09-23 23:46:45"
    visible_messier = get_messier_above_horizon(observer, messier_catalog)
    visible_messier_names = [obj['name'] for obj in visible_messier]

    # Получаем 5 случайных ярких звёзд
    visible_stars = get_brightest_stars_above_horizon(observer, brightest_stars)

    if messier:
        visible_messier_names = messier
        visible_stars = stars

    # Преобразуем в часы и минуты
    hours, minutes = deg_to_hours_minutes(observer_lon)

    # Генерация скайчарта
    generate_png(observer_lon, observer_lat, output_filename=skychart_filename, contours=contours, messier_objects=visible_messier_names, stars=visible_stars)

    rule = r'\rule{2cm}{0.4pt}'

    # Генерация содержимого LaTeX
    latex_content = r"""\documentclass{./SAS-class-skygen}
    
    \newcommand{\hwnum}{Сборная Москвы}
	\newcommand{\subject}{№""" + str(number) + r"""}
	\newcommand{\skykey}{"""+ f'{observer_lat:02d} {hours:02d}:{minutes:02d}' +r"""}
    
    \begin{document}
    
	\begin{center}
		\large\textbf{""" +  f"""{'Пользовательский' if not contours else "Ответ на пользовательский"} скайчарт №{number}""" + r"""}
	\end{center}

	\begin{enumerate}
		\item Обозначьте точку зенита символом \boldsans{Z} и стороны света как \boldsans{N}, \boldsans{E}, \boldsans{S}, \boldsans{W}.
		\item Обозначьте полюс мира символом \boldsans{P}.
		\item Обозначьте точку весны символом \Aries. Или же точку осени символом \Libra.
		\item Проведите большие круги небесного экватора и эклиптики.
		\item Рассчитайте звёздное время скайчарта: """ +  f"""{rule if not contours else f'{hours:02d}:{minutes:02d}'}"""
    latex_content += r""".
		\item Определите широту места съёмки: """  +  f"""{rule if not contours else f'{observer_lat:02d}'}"""
    latex_content += r""".
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
    for obj in visible_messier_names:
        if counter % 3 != 0: latex_content += obj + " & "
        else: latex_content += obj + r" \\" + '\n'
        counter += 1

    latex_content += "\n" + r"""\end{tabular}
    \end{table}
	
	\vspace{0.5cm}
    \begin{center}
    \includegraphics[width=\textwidth]{"""
    latex_content += skychart_filename + r"""}
    \end{center}
    
    \end{document}
    """

    # Сохраняем LaTeX файл
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(latex_content)

    return visible_messier_names, visible_stars

    # print(f"LaTeX отчёт сохранён как {output_filename}")


# generate_latex_report(38, 0, 'skychart.png', output_filename="sky_chart_report.tex", number=1, contours=True)