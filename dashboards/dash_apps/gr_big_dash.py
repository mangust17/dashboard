from dashboards.models import PricesClean
from .app_graphs import *
from dash import html, dcc, dash_table
from dash.dash_table import FormatTemplate
from dash.dash_table.Format import Format, Scheme
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date, timedelta
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from django.db.models import F, Func
from django.db.models import Window, Avg, Sum, Min
import pandas as pd
import plotly.express as px
import copy
import dash_bootstrap_components as dbc
from dash.dependencies import ALL, MATCH

external_stylesheets = ['/static/css/bootstrap.min.css', '/static/css/style.css']
external_scripts = ['/static/js/bootstrap.min.js']

start_date = date.today() - timedelta(days=21)
end_date = date.today()

app = DjangoDash('BigGraph', external_stylesheets=external_stylesheets, external_scripts=external_scripts)

queryset = PricesClean.objects.filter(date__range=(start_date, end_date)).values('date','model').annotate(price=Avg('price'), quantity = Avg('quantity'))
df = pd.DataFrame.from_records(queryset)

def get_group_from_dataframe(row):
    model = row['model']
    if '13' in model or '14' in model:
        return '13, 14'
    elif '15 PRO' in model or '15 PRO MAX' in model:
        return '15 PRO, 15 PRO MAX'
    elif '15' in model or '15 PLUS' in model:
        return '15, 15 PLUS'
    elif '16 PRO' in model or '16 PRO MAX' in model:
        return '16 PRO, 16 PRO MAX'
    elif '16' in model or '16 PLUS' in model:
        return '16, 16 PLUS'
    else:
        return 'OTHER'
    
df = gf_price_normalize(df)
df['group'] = df.apply(get_group_from_dataframe, axis=1)    

# Таблица нормализация
df_for_tables = pd.DataFrame.from_records(PricesClean.objects.filter(date__gte=start_date).values())
df_for_tables = gf_price_normalize(df_for_tables)
full_df = df_for_tables.copy()

top5 = PricesClean.objects.filter(date__gte=start_date).values('model').annotate(quantity=Sum('quantity')).order_by('-quantity').values_list('model', flat=True)[:5]
top5 = list(top5)

df_for_tables = df_for_tables[df_for_tables['date']==df_for_tables['last_date']][['model','current_price','median_price','date','price','min_price']]

df_for_tables['delta'] = (df_for_tables['current_price']-df_for_tables['median_price'])/df_for_tables['median_price']

# Установка стандартных значения для layout
default_layout = go.Layout(
    margin=dict(l=20, r=0, b=0, t=20),
    plot_bgcolor="#191C24",
    paper_bgcolor="#191C24",
    font=dict(color='white'),
    legend=dict(orientation='h', x=0, y=-0.2),
    template='plotly_dark'
)

def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

modal_body = []
grouped = df.groupby("group")
for group_name, group_df in grouped:
    group_models = group_df["model"].unique().tolist()
    modal_body.append(
        html.Details([
            html.Summary([
                dcc.Checklist(
                    options=[{"label": html.Span("Группа:", style={"color": "white","fontSize": "14px"}), "value": "ALL"}],
                    value=[],
                    id={'type': 'group-select-all', 'index': group_name},
                    inline=True,
                    style={
                        'display': 'inline-block',
                        'marginRight': '10px',
                        'fontSize': '14px',
                        'fontWeight': 'bold'
                    },
                    inputStyle={"marginRight": "5px"},
                ),
                html.Span(group_name, style={
                    "color": "white",
                    "fontSize": "14px",
                    "fontWeight": "bold",
                    "marginLeft": "10px"
                })
            ]),
            dcc.Checklist(
                options=[{"label": m, "value": m} for m in group_models],
                value=[m for m in top5 if m in group_models],
                id={'type': 'model-group-checklist', 'index': group_name},
                className="form-check text-white",
            )
        ], open=True, className="mb-3")
    )

modal_body_columns = split_list(modal_body, 3)
modal_body_layout = dbc.Row(
    [dbc.Col(children=col, width=4) for col in modal_body_columns]
)

app.layout = html.Div([  # Container
    html.Div([  # Row
        html.Div([  # Col
                  html.Div([ #Col-content
                            html.Div([
                                html.Label('Выберите интервал дат'),
                                html.Br(),
                                dcc.DatePickerRange(
                                    id='my-date-picker-range',
                                    min_date_allowed=date(2023, 8, 5),
                                    initial_visible_month=date.today(),
                                    start_date=date.today()-timedelta(days=30),
                                    end_date=date.today(),
                                    className="bg-dark p-0"),
                            ]),
                            html.Div([
                                dcc.Checklist(
                                    id="country-check",
                                    options=['Показывать Китай','Показывать Гонконг','Показывать Другое'],
                                    value=['Показывать Китай','Показывать Гонконг'],
                                    className="form-check"
                                )
                            ], className="d-flex align-items-center mt-4"),
                            html.Div([
                                dcc.RadioItems(
                                id='radio_check',
                                options=['Считаем по минимуму', 'Считаем по среднему'],
                                value='Считаем по среднему',
                                className='form-check'
                                )],className="d-flex align-items-center mt-4"),
                            html.Div([
                                dcc.RadioItems(
                                id='ddp_check',
                                options=['Считаем без наценки', 'Считаем ddp', 'Считаем ddp + НДС'],
                                value='Считаем без наценки',
                                className='form-check'
                                )],className="d-flex align-items-center mt-4"),
                            html.Div([
                                    html.Button(
                                            "Выбрать модели",
                                            id="open-models-modal",
                                            className="btn btn-primary-secondary",
                                            style={
                                                "margin-top": "20px",
                                                "margin-left": "15px",
                                                "width": "130px",
                                                "height": "50px",
                                                "display": "flex",
                                                "justifyContent": "center",
                                                "alignItems": "center",
                                                "borderRadius": "10px",
                                            },
                                        ),
                                        dcc.Store(id='selected-models', data=top5),
                                        dbc.Modal([
                                            dbc.ModalHeader(dbc.ModalTitle("Выберите модели")),
                                            dbc.ModalBody(modal_body_layout),
                                            dbc.ModalFooter(
                                                dbc.Button("Применить", id="apply-models", className="ms-auto")
                                            )
                                        ],
                                            id="models-modal",
                                            is_open=False,
                                            centered=False,
                                            size="xl",
                                            style={"marginTop": "5vh"},
                                            backdrop="static",
                                            scrollable=True
                                        )
                                    ]),

                            # html.Button("DDP", id="ddp-settings-btn", n_clicks=0, className="btn btn-primary-secondary",style={
                            #                                                                                                     "margin-top": "20px",
                            #                                                                                                     "margin-left": "15px",
                            #                                                                                                     "width": "130px",       
                            #                                                                                                     "height": "50px",
                            #                                                                                                     "display": "flex",
                            #                                                                                                     "justifyContent": "center",
                            #                                                                                                     "alignItems": "center",      
                            #                                                                                                     "borderRadius": "10px" 
                            #                                                                                                     },)

                             dbc.Modal(
                                        [
                                            dbc.ModalHeader(dbc.ModalTitle("Настройки коэффициентов DDP")),
                                            dbc.ModalBody([
                                                html.Label("Цена дороги"),
                                                dcc.Input(id="ddp-logistics", type="number", value=5.0, step=0.01, className="form-control mb-2"),
                                                html.Label("Маржа"),
                                                dcc.Input(id="ddp-margin", type="number", value=0.0, step=0.01, className="form-control mb-2"),
                                                html.Label("Пошлина"),
                                                dcc.Input(id="ddp-duty", type="number", value=1.0, step=0.01, className="form-control mb-2"),
                                                html.Label("Ставка перевода"),
                                                dcc.Input(id="ddp-conv", type="number", value=1.5, step=0.01, className="form-control mb-2"),
                                            ]),
                                            dbc.ModalFooter(
                                                dbc.Button("Закрыть", id="ddp-close-btn", className="ms-auto", n_clicks=0)
                                            )
                                        ],
                                        id="ddp-modal",
                                        is_open=False,
                                        centered=False,
                                        size="lg",
                                        style={"marginTop": "5vh"},
                                        backdrop="static",
                                        scrollable=False
                                    )
            ], className="bg-secondary p-4 rounded input-group")
        ], className="col-12"),
        html.Div([
          html.Div([
            html.H5('График цен на модели'),
            dcc.Loading(
                id="loading-price-graph-1",
                type = "default",
                children=[
                    dcc.Graph(id='price-graph-1', animate=True, style={"backgroundColor": "rgba(0,0,0,0)", 'color': '#ffffff', 'height': '390px'}, config= {'displaylogo': False})    
                ])
        	], className="rounded p-4 bg-secondary h-500")]
        , className="col-12 col-xl-6" ),
        html.Div([ 
            html.Div([
                html.H5('Динамика кол-ва предложений'),
                dcc.Loading(
                id="loading-bubble",
                type = "default",
                children=[
                    dcc.Tabs(id="tabs2", value=df['model'].unique()[0], children=[
                        dcc.Tab(label = model, value=model, className="bg-secondary p-1 mb-3") for model in df['model'].unique()[:5]
                    ]),
        
                    dcc.Graph(id='vendor_graph', animate=True, style={"backgroundColor": "rgba(0,0,0,0)", 'color': '#ffffff', 'height': '390px'},config= {'displaylogo': False}),   
                ])             
                ], className="bg-secondary rounded p-4 h-500")
            ], className="col-12 col-xl-6"),
        html.Div([
            html.Div([
                html.H5('График цен на модели по спекам'),
                dcc.Loading(
                    id="loading-price-graph-1",
                    type = "default",
                    children=[
                        dcc.Tabs(id="tabs5", value=df['model'].unique()[0], children=[
                            dcc.Tab(label = model, value=model, className="bg-secondary p-1 mb-3") for model in df['model'].unique()[:5]
                        ]),
                        dcc.Graph(id='price-graph-specs', animate=True, style={"backgroundColor": "rgba(0,0,0,0)", 'color': '#ffffff', 'height': '390px'}, config= {'displaylogo': False})   
                        ])  
                ], className="bg-secondary rounded p-4 h-500")
            ], className="col-12 col-xl-6"),
        html.Div([ #col
            html.Div([
                html.H5('График цен в абсолютных значениях'),
                dcc.Loading(
                    id="loading-price-graph-1",
                    type = "default",
                    children=[
                        dcc.Tabs(id="tabs3", value=df['model'].unique()[0], children=[
                            dcc.Tab(label = model, value=model, className="bg-secondary p-1 mb-3") for model in df['model'].unique()[:5]
                        ]),
                        dcc.Graph(id='double-y-graph', animate=True, style={"backgroundColor": "rgba(0,0,0,0)", 'color': '#ffffff', 'height': '390px'}, config= {'displaylogo': False}) 
                            ])  
            ], className="bg-secondary rounded p-4 h-500")
        ], className="col-12 col-xl-6"),
        html.Div([ #col
            html.Div([
                html.H5('График остатки/Цена'),
                dcc.Loading(
                    id="loading-price-graph-1",
                    type = "default",
                    children=[
                        dcc.Tabs(id="tabs4", value=df['model'].unique()[0], children=[
                            dcc.Tab(label = model, value=model, className="bg-secondary p-1 mb-3") for model in df['model'].unique()[:5]
                            ]),
                        dcc.Graph(id='double-y-new', animate=True, style={"backgroundColor": "rgba(0,0,0,0)", 'color': '#ffffff', 'height': '390px'}, config= {'displaylogo': False})
                    ])                
            ], className="bg-secondary rounded p-4 h-500")
        ], className="col-12 col-xl-6"),
        html.Div([ #col
          html.Div([ #content
            html.H5('Динамика цен по неделям'),
            dcc.Loading(
                id="loading-price-graph-1",
                type = "default",
                children=[
                    dcc.Tabs(id="tabs", value=df['model'].unique()[0], children=[
                        dcc.Tab(label = model, value=model, className="bg-secondary p-1 mb-3") for model in df['model'].unique()[:5]
                    ]),
                    dcc.Graph(id='stocks-graph-1', animate=True, style={"backgroundColor": "rgba(0,0,0,0)", 'color': '#ffffff', 'height': '350px'}, config= {'displaylogo': False})
                ])
            ], className="rounded bg-secondary p-4 h-500")
        ], className="col-12 col-xl-6"),
        html.Div([ #Col
          html.Div([ #Content
            html.H5('Таблица данных падение'),
            dcc.Loading(
                id="loading-price-graph-1",
                type = "default",
                children=[    
                    dash_table.DataTable(
                        id = "data-table-fall",
                        columns=[
                            {'name':'Модель', 'id': 'model'},
                            {'name':'Текущая цена', 'id': 'current_price','type':'numeric','format': Format(precision = 2, scheme=Scheme.fixed)},
                            {'name':'Медиана', 'id': 'median_price','type':'numeric','format': Format(precision = 2, scheme=Scheme.fixed)},
                            {'name':'Дельта', 'id': 'delta','type':'numeric', 'format': FormatTemplate.percentage(2)},
                            ],
                        data=df_for_tables.to_dict("records"),
                        style_header={
                            'backgroundColor': 'rgba(128,0,128,0.5)',
                            'color': 'white',
                            'text-align': 'center'
                        },
                        style_data={
                            'backgroundColor': '#191C24',
                            'color': 'white',
                            'font-size': '13px',
                        },
                        style_data_conditional=(
                            data_bars_diverging(df_for_tables, 'delta')
                        ),
                        style_cell_conditional=[{
                            'if': {'column_id': c},
                            'textAlign': 'left' } for c in ['model']] +
                        [{
                            'if': {'column_id': c},        
                            'textAlign': 'center'} for c in ['current_price','median_price','delta']]
                    ),
                    ]), 

            ], className="bg-secondary rounded p-4 h-500"),
        ], className="col-12 col-xl-4"),
        html.Div([ # col
          html.Div([ # content
            html.H5('Таблица данных рост'),
            dcc.Loading(
                id="loading-price-graph-1",
                type = "default",
                children=[            
                    dash_table.DataTable(
                        id = "data-table-grow",
                        columns=[
                            {'name':'Модель', 'id': 'model'},
                            {'name':'Текущая цена', 'id': 'current_price','type':'numeric','format': Format(precision = 2, scheme=Scheme.fixed)},
                            {'name':'Медиана', 'id': 'median_price','type':'numeric','format': Format(precision = 2, scheme=Scheme.fixed)},
                            {'name':'Дельта', 'id': 'delta','type':'numeric', 'format': FormatTemplate.percentage(2)},
                            ],
                        data=df_for_tables.to_dict("records"),
                        style_header={
                            'backgroundColor': 'rgba(128,0,128,0.5)',
                            'color': 'white',
                            'text-align': 'center'
                        },
                        style_data={
                            'backgroundColor': '#191C24',
                            'color': 'white',
                            'font-size': '13px',
                        },
                        style_data_conditional=(
                            data_bars_diverging(df_for_tables, 'delta')
                        ),
                        style_cell_conditional=[{
                            'if': {'column_id': c},
                            'textAlign': 'left' } for c in ['model']] +
                        [{
                            'if': {'column_id': c},        
                            'textAlign': 'center'} for c in ['current_price','median_price','delta']]
                    ),
                ])
            ], className="bg-secondary rounded p-4 table-responsive h-500")
        ], className="col-12 col-xl-4"), #Col
        html.Div([ #Col
            html.Div([ #Cont
                html.H5('Карта'),
                dcc.Graph(id='trace_map', style={"height":"400px"}, config= {'displaylogo': False})
            ], className="bg-secondary rounded p-4 h-500")
        ], className="col-12 col-xl-4"),
        html.Div([ #Col
            html.Div([ #Cont
                html.H5('Структура остатков'),
                dcc.Loading(
                    id="loading-price-graph-1",
                    type = "default",
                    children=[
                        dcc.Graph(id='stocks-tree-1', animate=True, style={"backgroundColor": "rgba(0,0,0,0)", 'color': '#ffffff', 'height': '430px'}, config= {'displaylogo': False})
                    ])
            ], className="bg-secondary rounded p-4 h-500")
        ], className="col-12 col-xl-4"),
        html.Div([ #Col
            html.Div([ #Cont
                html.H5('Анализ цен на модели'),
                dcc.Loading(
                    id="loading-price-graph-1",
                    type = "default",
                    children=[
                        dcc.Graph(id='trace_box', animate=True, style={"backgroundColor": "rgba(0,0,0,0)", 'color': '#ffffff', 'height': '430px'}, config= {'displaylogo': False})
                    ])                
            ], className="bg-secondary rounded p-4 h-500")
        ], className="col-12 col-xl-8"),                
    ], className="row g-4"), #Row
], className="container-fluid p-4") #Container

@app.callback(
    Output("country-check", "value"),
    Input("country-check", "value")
)
def update_country_check(value):
    if not value:
        return ["Показывать Другое"]
    return value


@app.callback(
    Output("ddp-modal", "is_open"),
    Input("ddp-settings-btn", "n_clicks"),
    Input("ddp-close-btn", "n_clicks"),
    State("ddp-modal", "is_open")
)
def toggle_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("models-modal", "is_open"),
    [Input("open-models-modal", "n_clicks"),
     Input("apply-models", "n_clicks")],
    State("models-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_models_modal(open_click, apply_click, is_open):
    return not is_open

@app.callback(
    Output("selected-models", "data"),
    Input("apply-models", "n_clicks"),
    State({'type': 'model-group-checklist', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def save_selected_models(n_clicks, all_selected_lists):
    all_models = [model for sublist in all_selected_lists if sublist for model in sublist]
    return all_models

@app.callback(
    Output({'type': 'model-group-checklist', 'index': MATCH}, 'value'),
    Input({'type': 'group-select-all', 'index': MATCH}, 'value'),
    State({'type': 'model-group-checklist', 'index': MATCH}, 'options'),
    prevent_initial_call=True
)
def select_all_models(select_all_value, model_options):
    if "ALL" in select_all_value:
        return [opt['value'] for opt in model_options]
    return []




@app.callback(
    [
        Output('price-graph-1', 'figure'),
        Output('stocks-graph-1', 'figure'),
        Output('stocks-tree-1', 'figure'),
        Output('data-table-fall', 'data'),
        Output('data-table-grow', 'data'),
        Output('tabs', 'children'),
        Output('vendor_graph', 'figure'),
        Output('tabs2', 'children'),
        Output('double-y-graph', 'figure'),
        Output('double-y-new', 'figure'),
        Output('trace_map', 'figure'),
        Output('trace_box', 'figure'),
        Output('tabs3', 'children'),
        Output('tabs4', 'children'),
        Output('tabs5', 'children'),
        Output('price-graph-specs', 'figure'),
    ],
    [
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date'),
        Input('selected-models', 'data'), 
        Input('tabs', 'value'),
        Input('tabs2', 'value'),
        Input('country-check', 'value'),
        Input('radio_check', 'value'),
        Input('ddp_check', 'value'),
        Input('tabs3', 'value'),
        Input('tabs4', 'value'),
        Input('tabs5', 'value'),
        Input('ddp-logistics', 'value'),
        Input('ddp-margin', 'value'),
        Input('ddp-duty', 'value'),
        Input('ddp-conv', 'value'),
    ]
)
def update_price_graph_1(
    start_date,
    end_date,
    models,
    tab,
    tab2,
    country_check,
    radio_check,
    ddp_check,
    tab3,
    tab4,
    tab5,
    logistics,
    margin_percent,
    duty_percent,
    conversion_rate
):
    if not models:
        return dash.no_update  # fallback

    tab, tab2, tab3, tab4, tab5 = (models[0] if t not in models else t for t in (tab, tab2, tab3, tab4, tab5))

    all_countries = set(
    PricesClean.objects.filter(
        date__range=(start_date, end_date),
        model__in=models
    ).values_list('country', flat=True).distinct()
)

    included_countries = set()

    if 'Показывать Китай' in country_check:
        included_countries.add('CN')
    if 'Показывать Гонконг' in country_check:
        included_countries.add('HK')
    if 'Показывать Другое' in country_check:
        included_countries.update(all_countries - {'CN', 'HK'})

    excluded_countries = list(all_countries - included_countries)


    queryset = PricesClean.objects.filter(
        date__range=(start_date, end_date),
        model__in=models
    ).exclude(country__in=excluded_countries)
  
    if radio_check=='Считаем по среднему':
        queryset_grouped = queryset.values('date','model').annotate(price=Avg('price'), quantity = Sum('quantity'))
    else:
        queryset_grouped = queryset.values('date','model').annotate(price=Min('price'), quantity = Sum('quantity'))

    df = pd.DataFrame.from_records(queryset_grouped)
    df[['price','quantity']]=df[['price','quantity']].astype(int)
    df = gf_price_normalize(df)

    if ddp_check == 'Считаем ddp':
        dap_price = (df.price + logistics) * (1 + margin_percent / 100)
        price_with_duty = dap_price * (1 + duty_percent / 100)
        ddp_price = price_with_duty * (1 + conversion_rate / 100)
        df.price = ddp_price
    elif ddp_check == 'Считаем ddp + НДС':
        dap_price = (df.price + logistics) * (1 + margin_percent / 100)
        price_with_duty = dap_price * (1 + duty_percent / 100)
        ddp_price = price_with_duty * (1 + conversion_rate / 100)
        df.price = ddp_price * 1.2



    # Динамика цен на модели
    trace1 = []
    for model in models:
        country_data = df[df['model'] == model]
        trace = go.Scatter(
            x=country_data['date'],
            y=country_data['price_normalized'],
            mode='lines+markers',
            line=dict(width=2, shape='spline'),
            marker=dict(size=8),
            name=model,
            hovertemplate="%{y}"
        )
        trace1.append(trace)
        
    # Барплот по неделям
    df_grouped_bar = df.groupby(['week','model'],as_index=False)[['price','quantity']].min()
    df_grouped_bar = df_grouped_bar[df_grouped_bar['model']==tab]
    bar_min = min(df_grouped_bar['price'])*0.95
    bar_max = max(df_grouped_bar['price'])*1.05
        
    trace2 = []
    for week in df_grouped_bar['week'].unique():
        week_data = df_grouped_bar[(df_grouped_bar['week'] == week)&(df_grouped_bar['model'].isin(models) )]
        trace2.append(go.Bar(name = 'week '+str(week), x=week_data['model'], y=week_data['price']))
        
    trace3 = []
    if len(country_check) == 1:
        vendor_qs = PricesClean.objects.filter(date__range=(start_date, end_date),model=tab2).values('date','model','vendor').annotate(price=Avg('price'), quantity = Sum('quantity'))
    else:
        vendor_qs = PricesClean.objects.filter(date__range=(start_date, end_date),model=tab2).exclude(country="CN").values('date','model','vendor').annotate(price=Avg('price'), quantity = Sum('quantity'))   
             
    vendor_df = pd.DataFrame.from_records(vendor_qs).sort_values('quantity', ascending=False).head(10)
    
    vendor_mapping = {}
    for i, vendor in enumerate(vendor_df['vendor'].unique(), 1):
        vendor_mapping[vendor] = f"Поставщик {i}"
    
    for vendor in vendor_df['vendor'].unique():
        vendor_data = vendor_df[(vendor_df['vendor']==vendor)]
        trace3.append(go.Scatter(
            x=vendor_data['date'], 
            y=vendor_data['price'],
            mode="markers", 
            
            marker=dict(
                size = vendor_data['quantity']*0.1,
                sizemode = 'area',
                sizeref=0.1,
            ), 
            text=['Price: {}<br>Quantity: {}'.format(int(price), size) for price, size in zip(vendor_data['price'], vendor_data['quantity'])],
            name = vendor_mapping[vendor]))
    
    
    country_data = df[df['model'] == tab3]
    country_data['smoothed_quantity'] = country_data.groupby('model')['price'].apply(lambda x: x.ewm(alpha=0.2, adjust=False).mean()).reset_index(0, drop=True)
    trace_abs = [go.Scatter(
        x=country_data['date'],
        y=country_data['price'],
        mode='lines',
        line=dict(width=2, shape='spline'),
        marker=dict(size=8),
        name=tab3,
        fill='tozeroy',
        fillcolor='rgba(128,0,128,0.1)',
        hovertemplate="Цена: %{y}"
    )] 
    trace_abs.append(go.Scatter(
        x=country_data['date'],
        y=country_data['smoothed_quantity'],
        mode='lines',
        line=dict(width=2, shape='spline', dash='dash', color='rgb(249, 143, 255)'),        
    ))
    
    
    # График по спекам
    if radio_check=='Считаем по среднему':
        df_clean = pd.DataFrame.from_records(queryset.filter(model = tab5).values('date','model','country_id__spec').annotate(price_avg = Avg('price')))
    else:
        df_clean = pd.DataFrame.from_records(queryset.filter(model = tab5).values('date','model','country_id__spec').annotate(price_avg = Min('price')))
        
    min_axis = df_clean['price_avg'].min()*0.95
    max_axis = df_clean['price_avg'].max()*1.05
    trace_specs = []
    for country in df_clean[(df_clean['model'] == tab5)]['country_id__spec'].unique():
        trace_specs.append(go.Scatter(
            x=df_clean[df_clean['country_id__spec']==country]['date'], 
            y=df_clean[df_clean['country_id__spec']==country]['price_avg'], 
            name = country,
            mode='lines+markers',
            line=dict(width=2, shape='spline')))
    spec_layout = copy.deepcopy(default_layout)
    spec_layout.update(
        yaxis=dict(range = [min_axis,max_axis])
    )
    
    
    

    
    # Двойной график
    trace_double_new = []
    trace_double_new.append(
        go.Scatter(
            name="Цена",
            x=df[df['model']==tab4]['date'],
            y=df[df['model']==tab4]['price'],
            mode='lines+markers',
            line=dict(width=2, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(128,0,128,0.4)'
            )
    )
    trace_double_new.append(
        go.Scatter(
            name="Остатки",
            x=df[df['model']==tab4]['date'],
            y=-df[df['model']==tab4]['quantity'],
            mode='lines+markers',
            line=dict(width=2, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(128,50,128,0.4)'
            
            )
    )

    
    # Boxplot внизу
    model_counts = full_df['model'].value_counts()
    models_with_enough_data = model_counts[model_counts > 15].index.tolist()
    boxplot_df_filtered = full_df[full_df['model'].isin(models_with_enough_data)]
    
    trace_box = [go.Box(
        name='Анализ цен на модели',
        x=boxplot_df_filtered['model'],
        y=boxplot_df_filtered['price_normalized'],
        )]

    df_current = boxplot_df_filtered[boxplot_df_filtered['date']==boxplot_df_filtered['last_date']].groupby('model', as_index=False)['price_normalized'].max()
    trace_box.append(go.Scatter(
        name = 'Текущая цена',
        x=df_current['model'],
        y=df_current['price_normalized'],
        mode='markers'
    ))
    layout_box = copy.deepcopy(default_layout)

    
    
    
    # Дерево
    tree = px.treemap(df,path=["model"],values='quantity')


    # Форматирование для обычных графиков
    
    layout = copy.deepcopy(default_layout)
    layout.update(
        template='plotly_dark',
        xaxis=dict(title='Date'),
        yaxis=dict(title=None),
        hovermode="x"
    )
    
    layout_buble = copy.deepcopy(default_layout)
    layout_buble.update(
        showlegend=False,
    )

    layout_absolute_graph = copy.deepcopy(default_layout)
    abs_min = min(df[df['model']==tab3]['price'])*0.99
    abs_max = max(df[df['model']==tab3]['price'])*1.01
    layout_absolute_graph.update(
        yaxis=dict(title='date', range = [abs_min,abs_max]),
        showlegend=False,
        hovermode="x",
    )
    
    price_max = max(df[df['model']==tab4]['price'])*1.6
    quantity_min = -max(df[df['model']==tab4]['quantity'])*1.01
    layout_double_y = copy.deepcopy(default_layout)
    layout_double_y.update(
        yaxis=dict(title='Цена', side='left', showgrid=True, range = [quantity_min,price_max]),
        barmode='relative', 
        hovermode="x"
    )
    
    layout_bar = go.Layout(
        margin=dict(l=20, r=0, b=0, t=20),
        plot_bgcolor="#191C24",
        paper_bgcolor="#191C24",
        xaxis=dict(title='Date'),
        yaxis=dict(title=None, range = [bar_min,bar_max]),
        font=dict(color='white'),
        legend=dict(orientation='h', x=0, y=-0.2),
        template='plotly_dark',
        barmode='group',
    )
    
    
    
    
    # Форматирование для дерева 
    tree.update_layout(
        plot_bgcolor="#251421",
        paper_bgcolor="#251421",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        xaxis_title="",
        yaxis_title="",
        margin=dict(l=0, r=0, t=0, b=0),   
    )
    x_min = df['date'].min()
    x_max = df['date'].max()
    
    # Определяем минимальное и максимальное значение по оси Y для цены
    y_min_price = df['price'].min()
    y_max_price = df['price'].max()
    
   
    # Устанавливаем масштаб для осей X и Y в макете
    layout['xaxis']['range'] = [x_min, x_max]

    tabs = [
        dcc.Tab(label=model, value=model, className="bg-secondary p-1 mb-3") for model in models
    ]
    
    tabs2 = [
        dcc.Tab(label=model, value=model, className="bg-secondary p-1 mb-3") for model in models
    ]
    
    tabs3 = [
        dcc.Tab(label=model, value=model, className="bg-secondary p-1 mb-3") for model in models
    ]
    
    tabs4 = [
        dcc.Tab(label=model, value=model, className="bg-secondary p-1 mb-3") for model in models
    ]
    
    tabs5 = [
        dcc.Tab(label=model, value=model, className="bg-secondary p-1 mb-3") for model in models
    ]
    
    
    

    
    # Карта   
    map_data = PricesClean.objects.filter(date__range=(start_date, end_date)).values('date', 'country').annotate(
        iso_alpha = F("country_id__iso_alpha"),
        continent = F('country_id__spec'),
        qty = Sum('quantity')
        )
    map_df = pd.DataFrame.from_records(map_data)
    map_df['date'] = pd.to_datetime(map_df['date'])
    map_df['week'] = map_df['date'].dt.isocalendar().week
    map_df = map_df.groupby(['week','iso_alpha','continent','country'], as_index=False)['qty'].sum()
    

    fig_map = px.scatter_geo(map_df, locations="iso_alpha", color="continent",
                        hover_name="country", size="qty",
                        animation_frame="week",
                        projection="natural earth",
                        template='plotly_dark')
    layout_map = copy.deepcopy(default_layout)
    layout_map.update(
        showlegend=False,
        geo=dict(
            bgcolor='#191C24',  # Задаем цвет фона карты
            projection_type="natural earth",
            fitbounds='locations'
            
    )
    )
    fig_map.update_layout(layout_map)
    
    


    return (
        {'data': trace1, 'layout': layout},
        {'data': trace2, 'layout': layout_bar,},
        tree, 
        df_for_tables.sort_values('delta', ascending=True).head(13).to_dict(orient='records'), 
        df_for_tables.sort_values('delta', ascending=False).head(13).to_dict(orient='records'), 
        tabs, 
        {'data': trace3, 'layout': layout_buble}, 
        tabs2, 
        {'data': trace_abs,'layout':layout_absolute_graph}, 
        {'data': trace_double_new,'layout':layout_double_y}, 
        fig_map,
        {'data': trace_box, 'layout': layout_box},
        tabs3,
        tabs4,
        tabs5,
        {'data': trace_specs, 'layout': spec_layout}
        )
        
