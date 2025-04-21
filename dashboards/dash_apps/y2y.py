from dashboards.models import PricesClean, AggregatedModel, CurrencyNew
from dashboards.utils_classes import GraphManager
from .app_graphs import *
from dash import html, dcc
from dash.dependencies import Input, Output
from datetime import date, timedelta
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
from django.db.models import Avg, Sum, OuterRef, Subquery, F, Min
import pandas as pd
import re

external_stylesheets = ['/static/css/bootstrap.min.css', '/static/css/style.css']
external_scripts = ['/static/js/bootstrap.min.js']

start_date = date.today() - timedelta(days=21)
end_date = date.today()

app = DjangoDash('y2y-app', external_stylesheets=external_stylesheets, external_scripts=external_scripts)

models = AggregatedModel.objects.filter(model__contains = "IPHONE").distinct().values_list('model', flat=True).order_by('model')
models = list(dict.fromkeys(model.strip() for model in models))
pattern = re.compile(r'IPHONE\s\d+\s(?:PRO|PLUS|PRO\sMAX)?\s?\d+(?:GB|TB)')

filtered_models = [model for model in models if pattern.fullmatch(model.strip())]
old_models = [model for model in filtered_models if not re.search(r'\b16\b', model)]

app.layout = html.Div([  # Container
    html.Div([ # Row
        html.Div([ #Col
            html.Div([
                html.H5("Статистика год к году по аналогичным моделям"),
                html.Div([
                    dcc.Dropdown(
                        id="first-dropdown",
                        options = [{'label': model, 'value': model} for model in filtered_models],
                        value="IPHONE 16 128GB", 
                        style={'minWidth':'300px', 'height': '30px'},
                        placeholder="Выбери модель 2024"),
                    
                    dcc.Dropdown(
                        id="second-dropdown",
                        options = [{'label': model, 'value': model} for model in old_models],
                        value="IPHONE 15 128GB", 
                        style={'minWidth':'300px'},
                        className="mx-4",
                        placeholder="Выбери модель 2023"
                        ),
                ], className="input-group mt-4")
            ], className="bg-secondary p-4 rounded")
        ], className="col-12"),
        html.Div([  # Col
    html.Div([  # bg
        html.H5("Динамика предложений по спекам"),
            html.Div([
                # Обертка для радиоэлементов
                html.Div([
                    # Первый RadioItems
                    html.Div([
                        dcc.RadioItems(
                            id='radio-check',
                            options=['Абсолютные значения', 'Нормированные значения','Минимальные значения'],
                            value='Абсолютные значения',
                            className='form-check'
                        )
                    ], className="d-flex align-items-center mt-4"),
                    
                    # Второй RadioItems
                    html.Div([
                        dcc.RadioItems(
                            id='currency-check',
                            options=['Цены в долларах', 'Цены в рублях'],
                            value='Цены в долларах',
                            className='form-check'
                        )
                    ], className="d-flex align-items-center mt-4"),
                    
                    # Checklist
                    html.Div([
                        dcc.Checklist(
                            id='region-check',
                            options=[
                                {'label': 'Учитывать Америку', 'value': 'usa'},
                                {'label': 'Учитывать Китай', 'value': 'china'}
                            ],
                            value=['usa', 'china'],
                            className='form-check'
                        )
                    ], className="d-flex align-items-center mt-4"),
                    
                ], className="d-flex mb-4"),  # Flex column для вертикального размещения

                # График с загрузчиком
                dcc.Loading(
                    id="price-graph-versus-loader",
                    type="default",
                    children=[
                        dcc.Graph(
                            id='price-graph-versus', 
                            animate=False, 
                            config={'displaylogo': False}, 
                            style={"height": "350px"}, 
                            className="mt-4"
                        )
                    ]
                )
            ], className="d-flex flex-column")  # Flex column для размещения всех элементов вертикально
        ], className="bg-secondary p-4 rounded")
    ], className="col-12"),
    ], className="row g-4") #Row
], className="container-fluid p-4") #Container

@app.callback(
    [Output('price-graph-versus', 'figure'),
     ],
    [
      Input('first-dropdown', 'value'),
      Input('second-dropdown', 'value'),
      Input('radio-check', 'value'),
      Input('currency-check', 'value'),
      Input('region-check', 'value'), 
    ])
def update_price_graph_1(first_model, second_model, radio, currency_radio, regions):
    # График сравнений
    versus_graph = GraphManager()
    currency_subquery = CurrencyNew.objects.filter(datetime__date = OuterRef('date'), code = "USD").values('value')
  
    # Базовый запрос
    base_query = PricesClean.objects
    
    exclude_specs = []
    if 'usa' not in regions:
        exclude_specs.extend(['USA', 'USA OTHER'])
    if 'china' not in regions:
        exclude_specs.append('CHINA')
    
    if exclude_specs:
        base_query = base_query.exclude(
            country_id__spec__in=exclude_specs
        )
        if 'usa' not in regions:
            base_query = base_query.exclude(country_id__spec__icontains='US')
    
    total_before = PricesClean.objects.count()
    total_after = base_query.count()
    print(f"Выбранные регионы: {regions}")
    print(f"Записей до фильтрации: {total_before}")
    print(f"Записей после фильтрации: {total_after}")
    print(f"Исключено записей: {total_before - total_after}")

    # Первый df
    first_qs = base_query.filter(model = first_model, date__gte = date(2025,1,1)).values('date','model')
    
    if radio == "Минимальные значения":
        first_qs = first_qs.annotate(
            price=Min('price'),
            quantity=Sum('quantity'),
            rub_price=Subquery(currency_subquery)*F('price')
        )
    else:
        first_qs = first_qs.annotate(
            price=Avg('price'),
            quantity=Sum('quantity'),
            rub_price=Subquery(currency_subquery)*F('price')
        )
    
    df = pd.DataFrame.from_records(first_qs)
    df['second_axe'] = df['date']-timedelta(days=362)
    
    # Второй df
    second_qs = base_query.filter(
        model=second_model, 
        date__range=(date(2024,1,1), date.today()-timedelta(days=365))
    ).values('date','model')
    
    if radio == "Минимальные значения":
        second_qs = second_qs.annotate(
            price=Min('price'),
            quantity=Sum('quantity'),
            rub_price=Subquery(currency_subquery)*F('price')
        )
    else:
        second_qs = second_qs.annotate(
            price=Avg('price'),
            quantity=Sum('quantity'),
            rub_price=Subquery(currency_subquery)*F('price')
        )

    second_df = pd.DataFrame.from_records(second_qs)
    
    # Объединение
    df = df.sort_values("second_axe")
    second_df = second_df.sort_values("date")

    # 🔧 Конвертация в datetime
    df['second_axe'] = pd.to_datetime(df['second_axe'])
    second_df['date'] = pd.to_datetime(second_df['date'])

    merged_df = pd.merge_asof(
        df,
        second_df,
        left_on="second_axe",
        right_on="date",
        direction="nearest",
        tolerance=pd.Timedelta(days=3)
    )

    merged_df = merged_df.dropna(subset=["price_x", "price_y"])

    print(merged_df)
    merged_df['normal_1'] = merged_df['price_x']/merged_df['price_x'].mean()
    merged_df['normal_2'] = merged_df['price_y']/merged_df['price_y'].mean()
    
    if radio == "Нормированные значения":
        y1 = merged_df['normal_1']
        y2 = merged_df['normal_2']
    else:  
        if currency_radio == "Цены в долларах":
            y1 = merged_df['price_x']
            y2 = merged_df['price_y']
        else:
            y1 = merged_df['rub_price_x']
            y2 = merged_df['rub_price_y']
    
    fig = go.Figure()

    fig.add_trace(
      go.Scatter(
        x = merged_df['date_y'],
        y = y2,
        name = 2023,
        xaxis="x2",
        yaxis="y1",
        line=dict(width=2, shape='spline', dash="dash"),
      )
    )

    fig.add_trace(
      go.Scatter(
        x = merged_df['date_x'],
        y = y1,
        name = 2024,
        yaxis="y1",
        line=dict(width=2, shape='spline'),
      )
    )

    fig.update_layout(versus_graph.layout)
    fig.update_layout(
        xaxis=dict(
            title='Primary X Axis',
            titlefont=dict(size=12),
            position=0,
            tickangle=45,
        ),
        xaxis2=dict(
            title='Secondary X Axis',
            overlaying='x',  # Накладываем на первую ось
            side='bottom',   # Расположение второй оси X
            position=0,
            tickangle=45 
        ),
        yaxis=dict(title='Цена'),
        title=None,
        
    )

    return [fig]