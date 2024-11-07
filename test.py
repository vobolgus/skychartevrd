import dash
import pandas as pd
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from skygen_smal import generate_skychart_with_constellations_and_stars

# Каталог Hipparcos
hip_catalog = pd.read_csv("hipparcos_catalog.csv")

#     # Файл с линиями созвездий
# constellationship_file = "constellationship.fab"

    # Параметры наблюдателя
observer_lat = 38 # Пример: широта Москвы
observer_lon = 280 # Пример: долгота Москвы
time_str = "2024-09-23 11:47:00"

fig = generate_skychart_with_constellations_and_stars(hip_catalog, 90, 0, time_str, observer_lon, observer_lat)

fig.update_layout(
    hovermode='closest',  # Наведение на ближайший объект
    hoverdistance=10,  # Расстояние, при котором срабатывает hover
    margin=dict(l=0, r=0, t=0, b=0),
)

# Приложение Dash
app = dash.Dash(__name__)

# Определение макета приложения
app.layout = html.Div([
    dcc.Graph(
        id='scattergeo-plot',
        figure=fig,
        style={'width': '90vw', 'height': '90vh'}  # Настройка ширины и высоты графика
    ),
    html.Div(id='click-data', style={'height': '50px', 'overflow': 'auto'})  # Фиксированная высота для текста
], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'height': '100vh'})

# Колбэк для обработки кликов
@app.callback(
    Output('click-data', 'children'),
    [Input('scattergeo-plot', 'clickData')]
)
def display_click_data(clickData):
    if clickData and 'points' in clickData:
        point_data = clickData['points'][0]
        # Извлекаем информацию из customdata
        return f"{point_data.get('customdata', 'No data')}"
    return "Click on a point to see the details."

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)