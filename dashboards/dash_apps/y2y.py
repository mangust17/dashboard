from dashboards.models import PricesClean, AggregatedModel, CurrencyNew
from dashboards.utils_classes import GraphManager
from .app_graphs import *
from dash import html, dcc
from dash.dependencies import Input, Output
from datetime import date, timedelta
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
from django.db.models import Avg, Sum, OuterRef, Subquery, F, Min, Value, ExpressionWrapper, FloatField
import pandas as pd
import re

external_stylesheets = ["/static/css/bootstrap.min.css", "/static/css/style.css"]
external_scripts = ["/static/js/bootstrap.min.js"]

start_date = date.today() - timedelta(days=21)
end_date = date.today()

app = DjangoDash(
    "y2y-app",
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
)

models = (
    AggregatedModel.objects.filter(model__contains="IPHONE")
    .distinct()
    .values_list("model", flat=True)
    .order_by("model")
)
models = list(dict.fromkeys(model.strip() for model in models))
pattern = re.compile(r"IPHONE\s\d+\s(?:PRO|PLUS|PRO\sMAX)?\s?\d+(?:GB|TB)")

filtered_models = [model for model in models if pattern.fullmatch(model.strip())]
old_models = [model for model in filtered_models if not re.search(r"\b16\b", model)]

app.layout = html.Div(
    [  # Container
        html.Div(
            [  # Row
                html.Div(
                    [  # Col
                        html.Div(
                            [
                                html.H5("Статистика год к году по аналогичным моделям"),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="first-dropdown",
                                            options=[
                                                {"label": model, "value": model}
                                                for model in filtered_models
                                            ],
                                            value="IPHONE 16 128GB",
                                            style={
                                                "minWidth": "300px",
                                                "height": "30px",
                                            },
                                            placeholder="Выбери модель 2024",
                                        ),
                                        dcc.Dropdown(
                                            id="second-dropdown",
                                            options=[
                                                {"label": model, "value": model}
                                                for model in old_models
                                            ],
                                            value="IPHONE 15 128GB",
                                            style={"minWidth": "300px"},
                                            className="mx-4",
                                            placeholder="Выбери модель 2023",
                                        ),
                                    ],
                                    className="input-group mt-4",
                                ),
                            ],
                            className="bg-secondary p-4 rounded",
                        )
                    ],
                    className="col-12",
                ),
                html.Div(
                    [  # Col
                        html.Div(
                            [  # bg
                                html.H5("Динамика цен предложений по спекам"),
                                html.Div(
                                    [
                                        # Обертка для радиоэлементов
                                        html.Div(
                                            [
                                                # Первый RadioItems
                                                html.Div(
                                                    [
                                                        dcc.RadioItems(
                                                            id="radio-check",
                                                            options=[
                                                                "Абсолютные значения",
                                                                "Нормированные значения",
                                                                "Минимальные значения",
                                                            ],
                                                            value="Абсолютные значения",
                                                            className="form-check",
                                                        )
                                                    ],
                                                    className="d-flex align-items-center mt-4",
                                                ),
                                                # Второй RadioItems
                                                html.Div(
                                                    [
                                                        dcc.RadioItems(
                                                            id="currency-check",
                                                            options=[
                                                                "Цены в долларах",
                                                                "Цены в рублях",
                                                            ],
                                                            value="Цены в долларах",
                                                            className="form-check",
                                                        )
                                                    ],
                                                    className="d-flex align-items-center mt-4",
                                                ),
                                                html.Div(
                                                    [
                                                        dcc.RadioItems(
                                                            id="sort-dropdown",
                                                            options=[
                                                                "день",
                                                                "неделя",
                                                                "месяц",
                                                            ],
                                                            value="день",
                                                            className="form-check",
                                                        )
                                                    ],
                                                    className="d-flex align-items-center mt-4",
                                                ),
                                                # Checklist
                                                html.Div(
                                                    [
                                                        dcc.Checklist(
                                                            id="region-check",
                                                            options=[
                                                                {
                                                                    "label": "Учитывать Америку",
                                                                    "value": "usa",
                                                                },
                                                                {
                                                                    "label": "Учитывать Китай",
                                                                    "value": "china",
                                                                },
                                                            ],
                                                            value=["usa", "china"],
                                                            className="form-check",
                                                        )
                                                    ],
                                                    className="d-flex align-items-center mt-4",
                                                ),
                                            ],
                                            className="d-flex mb-4",
                                        ),  # Flex column для вертикального размещения
                                        # График с загрузчиком
                                        dcc.Loading(
                                            id="price-graph-versus-loader",
                                            type="default",
                                            children=[
                                                dcc.Graph(
                                                    id="price-graph-versus",
                                                    animate=False,
                                                    config={"displaylogo": False},
                                                    style={"height": "350px"},
                                                    className="mt-4",
                                                )
                                            ],
                                        ),
                                    ],
                                    className="d-flex flex-column",
                                ),  # Flex column для размещения всех элементов вертикально
                            ],
                            className="bg-secondary p-4 rounded",
                        )
                    ],
                    className="col-12",
                ),
                html.Div(
                    [  # Col
                        html.Div(
                            [  # bg
                                html.H5("Динамика цен предложений по спекам"),
                                html.Div(
                                    [
                                        dcc.Loading(
                                            id="price-graph-versus-bar-loader",
                                            type="default",
                                            children=[
                                                dcc.Graph(
                                                    id="price-graph-versus-bar",
                                                    animate=False,
                                                    config={"displaylogo": False},
                                                    style={"height": "350px"},
                                                    className="mt-4",
                                                )
                                            ],
                                        ),
                                    ],
                                    className="d-flex flex-column",
                                ),  # Flex column для размещения всех элементов вертикально
                            ],
                            className="bg-secondary p-4 rounded",
                        )
                    ],
                    className="col-12",
                    id="bar-graph-div",
                    style={},
                ),
                html.Div(
                    [  # Col
                        html.Div(
                            [  # bg
                                html.H5("Динамика количества по спекам"),
                                html.Div(
                                    [
                                        dcc.Loading(
                                            id="price-graph-versus-bar-quant-loader",
                                            type="default",
                                            children=[
                                                dcc.Graph(
                                                    id="price-graph-versus-bar-quant",
                                                    animate=False,
                                                    config={"displaylogo": False},
                                                    style={"height": "350px"},
                                                    className="mt-4",
                                                )
                                            ],
                                        ),
                                    ],
                                    className="d-flex flex-column",
                                ),  # Flex column для размещения всех элементов вертикально
                            ],
                            className="bg-secondary p-4 rounded",
                        )
                    ],
                    className="col-12",
                    id="bar-quant-graph-div",
                    style={},
                ),
            ],
            className="row g-4",
        )  # Row
    ],
    className="container-fluid p-4",
)  # Container

# Формирование запроса
def get_price_queryset(base_query, model_name, year, radio, currency_subquery):
    if year == 2025:
        qs = base_query.filter(model=model_name, date__gte=date(2025, 1, 1)).values("date", "model")
    else:
        qs = base_query.filter(model=model_name, date__range=(date(2024, 1, 1), date(2025, 1, 1))).values("date", "model")

    price_agg = Min("price") if radio == "Минимальные значения" else Avg("price")

    return qs.annotate(
        price=price_agg,
        quantity=Sum("quantity"),
        currency=Subquery(currency_subquery),
    )

# Формирование датафрейма
def build_combined_price_dataframe(first_model, second_model, radio, currency_radio, regions):
    currency_subquery = CurrencyNew.objects.filter(
        datetime__date=OuterRef("date"), code="USD"
    ).values("value")

    base_query = PricesClean.objects

    exclude_specs = []
    if "usa" not in regions:
        exclude_specs.extend(["USA", "USA OTHER"])
    if "china" not in regions:
        exclude_specs.append("CHINA")

    if exclude_specs:
        base_query = base_query.exclude(country_id__spec__in=exclude_specs)


    qs_2025 = get_price_queryset(base_query, first_model, 2025, radio, currency_subquery)
    qs_2024 = get_price_queryset(base_query, second_model, 2024, radio, currency_subquery)

    df_2025 = pd.DataFrame.from_records(qs_2025)
    df_2024 = pd.DataFrame.from_records(qs_2024)

    if df_2025.empty and df_2024.empty:
        return pd.DataFrame()

    if not df_2025.empty:
        df_2025["date"] = pd.to_datetime(df_2025["date"])
        df_2025 = df_2025.rename(columns={
            "price": "price_2025",
            "currency": "currency_2025",
            "quantity": "quantity_2025",
        })

    if not df_2024.empty:
        df_2024["date"] = pd.to_datetime(df_2024["date"])
        df_2024 = df_2024.rename(columns={
            "price": "price_2024",
            "currency": "currency_2024",
            "quantity": "quantity_2024",
        })

    df_combined = pd.merge(
        df_2025,
        df_2024,
        how="outer",
        on="date",
        suffixes=("_2025", "_2024")
    )

    df_combined = df_combined.sort_values("date")

    df_combined["common_date"] = df_combined["date"].apply(lambda d: d.replace(year=2000))

    return df_combined

#Функция для формирования подсказок при группировке
def format_hovertext(g_values, prices, year, g_type, type):
    if type == "price":
        t = "Cредняя цена:"
    else:
        t = "Общее количество:"
    hover = []
    month_map = {
    1: "Янв", 2: "Фев", 3: "Мар", 4: "Апр", 5: "Май", 6: "Июн",
    7: "Июл", 8: "Авг", 9: "Сен", 10: "Окт", 11: "Ноя", 12: "Дек"
    }
    for g_val, p in zip(g_values, prices):
        if g_type == "month":
            label = month_map.get(g_val, f"Месяц {g_val}")
        elif g_type == "week":
            label = f"Неделя {g_val}"
        else:
            try:
                label = pd.to_datetime(g_val).strftime('%d %b')
            except Exception:
                label = str(g_val)
        if pd.notna(p):
            hover.append(f"{label}<br>{t} {year}: ${p:.2f}")
        else:
            hover.append(f"{label}<br>{t} {year}: —")
    return hover


@app.callback(
    [
        Output("price-graph-versus", "figure"),
        Output("price-graph-versus-bar", "figure"),
        Output("price-graph-versus-bar-quant", "figure"),
        Output("bar-graph-div", "style"),
        Output("bar-quant-graph-div", "style"),
    ],
    [
        Input("first-dropdown", "value"),
        Input("second-dropdown", "value"),
        Input("sort-dropdown", "value"),
        Input("radio-check", "value"),
        Input("currency-check", "value"),
        Input("region-check", "value"),
    ],
)
def update_price_graph_1(first_model, second_model, sort, radio, currency_radio, regions):
    versus_graph = GraphManager()

    df = build_combined_price_dataframe(first_model, second_model, radio, currency_radio, regions)
    if df.empty:
        return [None, None, None, {"display": "none"}, {"display": "none"}]

    df["normal_1"] = df["price_2025"] / df["price_2025"].mean()
    df["normal_2"] = df["price_2024"] / df["price_2024"].mean()
    df["month"] = df["date"].dt.month
    df["week"] = df["date"].dt.isocalendar().week
    df["price_2025"] = ((((df["price_2025"] + 3 ) * (1 + 2.5 / 100)) * (1 + 1.5 / 100)) * (1 + 1 / 100)) * 1.2
    df["rub_price_2025"] = df["price_2025"] * df["currency_2025"]
    df["price_2024"] = ((((df["price_2024"] + 3 ) * (1 + 2.5 / 100)) * (1 + 1.5 / 100)) * (1 + 1 / 100)) * 1.2
    df["rub_price_2024"] = df["price_2024"] * df["currency_2024"]
    if radio == "Нормированные значения":
        y1 = df["normal_1"]
        y2 = df["normal_2"]
    else:
        if currency_radio == "Цены в долларах":
            y1 = df["price_2025"]
            y2 = df["price_2024"]
        else:
            y1 = df["rub_price_2025"]
            y2 = df["rub_price_2024"]

    #  Scatter: цены 2024 и 2025
    fig_line = go.Figure()
    hovertext_2025 = [
        f"{date.strftime('%d %b')}<br>Цена 2025: ${p:.2f}" if not pd.isna(p) else f"{date.strftime('%d %b')}<br>Цена 2025: —"
        for date, p in zip(df["common_date"], df["price_2025"])
    ]
    hovertext_2024 = [
        f"{date.strftime('%d %b')}<br>Цена 2024: ${p:.2f}" if not pd.isna(p) else f"{date.strftime('%d %b')}<br>Цена 2024: —"
        for date, p in zip(df["common_date"], df["price_2024"])
    ]

    if sort == "день":
        # Строю по обычной coomon_date что бы графики остались целыми
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df["common_date"],
            y=y1,
            name="2025",
            mode='lines', line=dict(width=2, shape="spline", dash="dash"),
            hoverinfo="text", 
            hovertext=hovertext_2025, 
            showlegend=True
        ))
        fig_line.add_trace(go.Scatter(
            x=df["common_date"],
            y=y2,
            name="2024",
            mode='lines', line=dict(width=2, shape="spline"),
            hoverinfo="text",
            hovertext=hovertext_2024, 
            showlegend=True
        ))
        fig_line.update_layout(
            versus_graph.layout,
            xaxis=dict(title="Динамика цен по годам", tickformat="%d %b", tickangle=45),
            yaxis=dict(title="Цена"),
            hoverlabel=dict(align="left"),
            hovermode="x"
        )

        return [fig_line, go.Figure(), go.Figure(), {"display": "none"}, {"display": "none"}]

    # Здесь данные группируются либо по недели либо по месяцу
    else:
        g = "week" if sort == "неделя" else "month" if sort == "месяц" else "common_date"
        grouped = df.groupby(g).agg({
            "price_2025": "mean",
            "price_2024": "mean",
            "rub_price_2025": "mean",
            "rub_price_2024": "mean",
            "normal_1": "mean",
            "normal_2": "mean",
            "quantity_2025": "sum",
            "quantity_2024": "sum"
        }).reset_index()

        if radio == "Нормированные значения":
            y1 = grouped["normal_1"]
            y2 = grouped["normal_2"]
        else:
            if currency_radio == "Цены в долларах":
                y1 = grouped["price_2025"]
                y2 = grouped["price_2024"]
            else:
                y1 = grouped["rub_price_2025"]
                y2 = grouped["rub_price_2024"]

        hovertext_2025 = format_hovertext(grouped[g], grouped["price_2025"], "2025", g,"price")
        hovertext_2024 = format_hovertext(grouped[g], grouped["price_2024"], "2024", g,"price")


        line_mode = 'lines+markers'
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=grouped[g], 
            y=y1, 
            name="2025",
            mode=line_mode, 
            line=dict(width=2, shape="spline", dash="dash"),
            hoverinfo="text", 
            hovertext=hovertext_2025, 
            showlegend=True
        ))
        fig_line.add_trace(go.Scatter(
            x=grouped[g], 
            y=y2, 
            name="2024",
            mode=line_mode, 
            line=dict(width=2, shape="spline"),
            hoverinfo="text", 
            hovertext=hovertext_2024, 
            showlegend=True
        ))
        fig_line.update_layout(
            versus_graph.layout,
            xaxis=dict(title="Динамика цен по годам", tickformat="%d %b", tickangle=45),
            yaxis=dict(title="Цена"),
            hoverlabel=dict(align="left"),
            hovermode="x"
        )

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=grouped[g], 
            y=y1, 
            name="2025",
            marker_color="#6370fc", 
            hovertext=hovertext_2025, 
            hoverinfo="text", 
            showlegend=True
        ))
        fig_bar.add_trace(go.Bar(
            x=grouped[g], 
            y=y2, 
            name="2024",
            marker_color="#ed553d", 
            hovertext=hovertext_2024, 
            hoverinfo="text", 
            showlegend=True
        ))
        fig_bar.update_layout(
            versus_graph.layout,
            xaxis=dict(title="Динамика цен по годам", tickformat="%d %b", tickangle=45),
            yaxis=dict(title="Цена"),
            hoverlabel=dict(align="left"),
            barmode='group',
            hovermode="x"
        )

        hovertext_2025 = format_hovertext(grouped[g], grouped["quantity_2025"], "2025", g,"q")
        hovertext_2024 = format_hovertext(grouped[g], grouped["quantity_2024"], "2024", g,"q") 
        fig_bar_q = go.Figure()
        fig_bar_q.add_trace(go.Bar(
            x=grouped[g], 
            y=grouped["quantity_2025"],
            name="2025", 
            marker_color="#6370fc",
            hovertext=hovertext_2025, 
            hoverinfo="text", 
            showlegend=True
        ))
        fig_bar_q.add_trace(go.Bar(
            x=grouped[g], 
            y=grouped["quantity_2024"],
            name="2024", 
            marker_color="#ed553d",
            hovertext=hovertext_2024, 
            hoverinfo="text", 
            showlegend=True
        ))
        fig_bar_q.update_layout(
            versus_graph.layout,
            xaxis=dict(title="Динамика количества по годам", tickformat="%d %b", tickangle=45),
            yaxis=dict(title="Количество"),
            hoverlabel=dict(align="left"),
            barmode='group',
            hovermode="x"
        )

        return [fig_line, fig_bar, fig_bar_q, {"display": "block"}, {"display": "block"}]