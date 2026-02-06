from ...models import PricesClean, AggregatedModel, CurrencyNew
from ._app_graphs import *
from dash import html, dcc
from dash.dependencies import Input, Output
from datetime import date, timedelta
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
from django.db.models import Avg, Sum, OuterRef, Subquery, F, Min
import pandas as pd
from ...utils_classes import GraphManager
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


def get_models_sold_in_year(year):
    # Уникальные модели из базы за указанный год — только то, что реально продавалось.
    today = date.today()
    if year == 2026:
        date_end = min(date(2026, 12, 31), today)
        date_start = date(2026, 1, 1)
    elif year == 2025:
        date_start, date_end = date(2025, 1, 1), date(2025, 12, 31)
    else:
        date_start, date_end = date(2024, 1, 1), date(2024, 12, 31)
    sold = (
        PricesClean.objects.filter(date__range=(date_start, date_end))
        .values_list("model", flat=True)
        .distinct()
        .order_by("model")
    )
    return list(dict.fromkeys(m.strip() for m in sold if pattern.fullmatch(m.strip())))


models_2026 = get_models_sold_in_year(2026)
models_2025 = get_models_sold_in_year(2025)
models_2024 = get_models_sold_in_year(2024)

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
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Модель 2026",
                                                    className="form-label small text-muted mb-1",
                                                ),
                                                dcc.Dropdown(
                                                    id="first-dropdown",
                                                    options=[
                                                        {"label": model, "value": model}
                                                        for model in models_2026
                                                    ],
                                                    value="IPHONE 17 256GB",
                                                    style={"minWidth": "250px"},
                                                    placeholder="Модель 2026",
                                                ),
                                            ],
                                            className="d-inline-block me-3",
                                        ),
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Модель 2025",
                                                    className="form-label small text-muted mb-1",
                                                ),
                                                dcc.Dropdown(
                                                    id="second-dropdown",
                                                    options=[
                                                        {"label": model, "value": model}
                                                        for model in models_2025
                                                    ],
                                                    value="IPHONE 16 128GB",
                                                    style={"minWidth": "250px"},
                                                    placeholder="Модель 2025",
                                                ),
                                            ],
                                            className="d-inline-block mx-2",
                                        ),
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Модель 2024",
                                                    className="form-label small text-muted mb-1",
                                                ),
                                                dcc.Dropdown(
                                                    id="third-dropdown",
                                                    options=[
                                                        {"label": model, "value": model}
                                                        for model in models_2024
                                                    ],
                                                    value="IPHONE 15 128GB",
                                                    style={"minWidth": "250px"},
                                                    placeholder="Модель 2024",
                                                ),
                                            ],
                                            className="d-inline-block",
                                        ),
                                    ],
                                    className="mt-4",
                                ),
                            ],
                            className="bg-secondary p-4 rounded",
                        )
                    ],
                    className="col-12",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("О разделе", className="mb-3"),
                                html.H6(
                                    "Здесь сравниваются цены на iPhone за три года (2024, 2025, 2026) по одному и тому же календарному дню. "
                                    "Выберите три модели — по одной на каждый год — чтобы увидеть динамику цен флагманов.",
                                    className="mb-3",
                                ),
                                html.P("Доступные фильтры:", className="mb-1 fw-bold"),
                                html.Ul(
                                    [
                                        html.Li(
                                            "Тип значений: абсолютные (фактические цены), нормированные (относительно среднего) или минимальные."
                                        ),
                                        html.Li("Валюта: доллары или рубли."),
                                        html.Li(
                                            "Группировка: по дню, неделе или месяцу.(при выборе недели или месяца появится еще 2 графика)"
                                        ),
                                        html.Li(
                                            "Регионы: учёт данных из США и/или Китая."
                                        ),
                                    ],
                                    className="mb-0 text-muted",
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
    today = date.today()
    if year == 2026:
        qs = base_query.filter(
            model=model_name,
            date__range=(date(2026, 1, 1), min(date(2026, 12, 31), today)),
        ).values("date", "model")
    elif year == 2025:
        qs = base_query.filter(
            model=model_name, date__range=(date(2025, 1, 1), date(2025, 12, 31))
        ).values("date", "model")
    else:
        qs = base_query.filter(
            model=model_name, date__range=(date(2024, 1, 1), date(2024, 12, 31))
        ).values("date", "model")

    price_agg = Min("price") if radio == "Минимальные значения" else Avg("price")

    return qs.annotate(
        price=price_agg,
        quantity=Sum("quantity"),
        rub_price=Subquery(currency_subquery) * F("price"),
    )


# Формирование датафрейма
def build_combined_price_dataframe(
    first_model, second_model, third_model, radio, currency_radio, regions
):
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

    qs_2026 = get_price_queryset(
        base_query, first_model, 2026, radio, currency_subquery
    )
    qs_2025 = get_price_queryset(
        base_query, second_model, 2025, radio, currency_subquery
    )
    qs_2024 = get_price_queryset(
        base_query, third_model, 2024, radio, currency_subquery
    )

    df_2026 = pd.DataFrame.from_records(qs_2026)
    df_2025 = pd.DataFrame.from_records(qs_2025)
    df_2024 = pd.DataFrame.from_records(qs_2024)

    if df_2026.empty and df_2025.empty and df_2024.empty:
        return pd.DataFrame()

    if not df_2026.empty:
        df_2026["date"] = pd.to_datetime(df_2026["date"])
        df_2026["common_date"] = df_2026["date"].apply(lambda d: d.replace(year=2000))
        df_2026 = df_2026.rename(
            columns={
                "price": "price_2026",
                "rub_price": "rub_price_2026",
                "quantity": "quantity_2026",
            }
        )

    if not df_2025.empty:
        df_2025["date"] = pd.to_datetime(df_2025["date"])
        df_2025["common_date"] = df_2025["date"].apply(lambda d: d.replace(year=2000))
        df_2025 = df_2025.rename(
            columns={
                "price": "price_2025",
                "rub_price": "rub_price_2025",
                "quantity": "quantity_2025",
            }
        )

    if not df_2024.empty:
        df_2024["date"] = pd.to_datetime(df_2024["date"])
        df_2024["common_date"] = df_2024["date"].apply(lambda d: d.replace(year=2000))
        df_2024 = df_2024.rename(
            columns={
                "price": "price_2024",
                "rub_price": "rub_price_2024",
                "quantity": "quantity_2024",
            }
        )

    # Объединяем по common_date — один и тот же календарный день (15 янв, 20 фев и т.д.) для всех лет
    dfs_to_merge = [
        df[[c for c in df.columns if c not in ("date", "model")]]
        for df in [df_2026, df_2025, df_2024]
        if not df.empty
    ]
    if not dfs_to_merge:
        return pd.DataFrame()
    df_combined = dfs_to_merge[0]
    for df in dfs_to_merge[1:]:
        df_combined = pd.merge(df_combined, df, how="outer", on="common_date")

    df_combined = df_combined.drop_duplicates(subset=["common_date"]).sort_values(
        "common_date"
    )

    return df_combined


# Функция для формирования подсказок при группировке
def format_hovertext(g_values, prices, year, g_type, type):
    if type == "price":
        t = "Cредняя цена:"
    else:
        t = "Общее количество:"
    hover = []
    month_map = {
        1: "Янв",
        2: "Фев",
        3: "Мар",
        4: "Апр",
        5: "Май",
        6: "Июн",
        7: "Июл",
        8: "Авг",
        9: "Сен",
        10: "Окт",
        11: "Ноя",
        12: "Дек",
    }
    for g_val, p in zip(g_values, prices):
        if g_type == "month":
            label = month_map.get(g_val, f"Месяц {g_val}")
        elif g_type == "week":
            label = f"Неделя {g_val}"
        else:
            try:
                label = pd.to_datetime(g_val).strftime("%d %b")
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
        Input("third-dropdown", "value"),
        Input("sort-dropdown", "value"),
        Input("radio-check", "value"),
        Input("currency-check", "value"),
        Input("region-check", "value"),
    ],
)
def update_price_graph_1(
    first_model, second_model, third_model, sort, radio, currency_radio, regions
):
    if not all([first_model, second_model, third_model]):
        return [None, None, None, {"display": "none"}, {"display": "none"}]
    versus_graph = GraphManager()

    df = build_combined_price_dataframe(
        first_model, second_model, third_model, radio, currency_radio, regions
    )
    if df.empty:
        return [None, None, None, {"display": "none"}, {"display": "none"}]

    # Нормирование по годам (с учётом возможного отсутствия данных 2026)
    for year, col in [(2026, "price_2026"), (2025, "price_2025"), (2024, "price_2024")]:
        if col in df.columns and df[col].notna().any():
            df[f"normal_{year}"] = df[col] / df[col].mean()
        else:
            df[f"normal_{year}"] = pd.NA
    df["month"] = df["common_date"].dt.month
    # Неделя по дню года: неделя 1 = янв 1-7, неделя 52 = конец декабря (ISO смешивает янв 1-2 с дек!)
    df["week"] = (df["common_date"].dt.dayofyear - 1) // 7 + 1

    def get_y(col_price, col_rub, col_norm):
        if radio == "Нормированные значения":
            return (
                df[col_norm] if col_norm in df.columns else pd.Series([pd.NA] * len(df))
            )
        return (
            (df[col_price] if currency_radio == "Цены в долларах" else df[col_rub])
            if col_price in df.columns
            else pd.Series([pd.NA] * len(df))
        )

    y1 = get_y("price_2026", "rub_price_2026", "normal_2026")
    y2 = get_y("price_2025", "rub_price_2025", "normal_2025")
    y3 = get_y("price_2024", "rub_price_2024", "normal_2024")

    def make_hover(year, col):
        prices = df[col] if col in df.columns else pd.Series([pd.NA] * len(df))
        return [
            (
                f"{d.strftime('%d %b')}<br>Цена {year}: ${p:.2f}"
                if pd.notna(p)
                else f"{d.strftime('%d %b')}<br>Цена {year}: —"
            )
            for d, p in zip(df["common_date"], prices)
        ]

    hovertext_2026 = make_hover(2026, "price_2026")
    hovertext_2025 = make_hover(2025, "price_2025")
    hovertext_2024 = make_hover(2024, "price_2024")

    if sort == "день":
        fig_line = go.Figure()
        if "price_2026" in df.columns and df["price_2026"].notna().any():
            fig_line.add_trace(
                go.Scatter(
                    x=df["common_date"],
                    y=y1,
                    name="2026",
                    mode="lines",
                    line=dict(width=2, shape="spline", dash="dot"),
                    hoverinfo="text",
                    hovertext=hovertext_2026,
                    showlegend=True,
                )
            )
        if "price_2025" in df.columns and df["price_2025"].notna().any():
            fig_line.add_trace(
                go.Scatter(
                    x=df["common_date"],
                    y=y2,
                    name="2025",
                    mode="lines",
                    line=dict(width=2, shape="spline", dash="dash"),
                    hoverinfo="text",
                    hovertext=hovertext_2025,
                    showlegend=True,
                )
            )
        if "price_2024" in df.columns and df["price_2024"].notna().any():
            fig_line.add_trace(
                go.Scatter(
                    x=df["common_date"],
                    y=y3,
                    name="2024",
                    mode="lines",
                    line=dict(width=2, shape="spline"),
                    hoverinfo="text",
                    hovertext=hovertext_2024,
                    showlegend=True,
                )
            )
        fig_line.update_layout(
            versus_graph.layout,
            xaxis=dict(title="Динамика цен по годам", tickformat="%d %b", tickangle=45),
            yaxis=dict(title="Цена"),
            hoverlabel=dict(align="left"),
            hovermode="x",
        )

        return [
            fig_line,
            go.Figure(),
            go.Figure(),
            {"display": "none"},
            {"display": "none"},
        ]

    # Здесь данные группируются либо по недели либо по месяцу
    else:
        g = (
            "week"
            if sort == "неделя"
            else "month" if sort == "месяц" else "common_date"
        )
        agg_dict = {}
        for col in [
            "price_2026",
            "price_2025",
            "price_2024",
            "rub_price_2026",
            "rub_price_2025",
            "rub_price_2024",
            "normal_2026",
            "normal_2025",
            "normal_2024",
            "quantity_2026",
            "quantity_2025",
            "quantity_2024",
        ]:
            if col in df.columns:
                agg_dict[col] = "mean" if "price" in col or "normal" in col else "sum"
        grouped = df.groupby(g).agg(agg_dict).reset_index()

        def get_grouped_y(col_price, col_rub, col_norm):
            if radio == "Нормированные значения" and col_norm in grouped.columns:
                return grouped[col_norm]
            if currency_radio == "Цены в долларах" and col_price in grouped.columns:
                return grouped[col_price]
            if col_rub in grouped.columns:
                return grouped[col_rub]
            return pd.Series([pd.NA] * len(grouped))

        y1 = get_grouped_y("price_2026", "rub_price_2026", "normal_2026")
        y2 = get_grouped_y("price_2025", "rub_price_2025", "normal_2025")
        y3 = get_grouped_y("price_2024", "rub_price_2024", "normal_2024")

        hovertext_2026 = format_hovertext(
            grouped[g], grouped.get("price_2026", pd.Series()), "2026", g, "price"
        )
        hovertext_2025 = format_hovertext(
            grouped[g], grouped.get("price_2025", pd.Series()), "2025", g, "price"
        )
        hovertext_2024 = format_hovertext(
            grouped[g], grouped.get("price_2024", pd.Series()), "2024", g, "price"
        )

        line_mode = "lines+markers"
        fig_line = go.Figure()
        if "price_2026" in grouped.columns and grouped["price_2026"].notna().any():
            fig_line.add_trace(
                go.Scatter(
                    x=grouped[g],
                    y=y1,
                    name="2026",
                    mode=line_mode,
                    line=dict(width=2, shape="spline", dash="dot"),
                    hoverinfo="text",
                    hovertext=hovertext_2026,
                    showlegend=True,
                )
            )
        if "price_2025" in grouped.columns and grouped["price_2025"].notna().any():
            fig_line.add_trace(
                go.Scatter(
                    x=grouped[g],
                    y=y2,
                    name="2025",
                    mode=line_mode,
                    line=dict(width=2, shape="spline", dash="dash"),
                    hoverinfo="text",
                    hovertext=hovertext_2025,
                    showlegend=True,
                )
            )
        if "price_2024" in grouped.columns and grouped["price_2024"].notna().any():
            fig_line.add_trace(
                go.Scatter(
                    x=grouped[g],
                    y=y3,
                    name="2024",
                    mode=line_mode,
                    line=dict(width=2, shape="spline"),
                    hoverinfo="text",
                    hovertext=hovertext_2024,
                    showlegend=True,
                )
            )
        fig_line.update_layout(
            versus_graph.layout,
            xaxis=dict(title="Динамика цен по годам", tickformat="%d %b", tickangle=45),
            yaxis=dict(title="Цена"),
            hoverlabel=dict(align="left"),
            hovermode="x",
        )

        fig_bar = go.Figure()
        colors = {"2026": "#00c853", "2025": "#6370fc", "2024": "#ed553d"}
        if "price_2026" in grouped.columns and grouped["price_2026"].notna().any():
            fig_bar.add_trace(
                go.Bar(
                    x=grouped[g],
                    y=y1,
                    name="2026",
                    marker_color=colors["2026"],
                    hovertext=hovertext_2026,
                    hoverinfo="text",
                    showlegend=True,
                )
            )
        if "price_2025" in grouped.columns and grouped["price_2025"].notna().any():
            fig_bar.add_trace(
                go.Bar(
                    x=grouped[g],
                    y=y2,
                    name="2025",
                    marker_color=colors["2025"],
                    hovertext=hovertext_2025,
                    hoverinfo="text",
                    showlegend=True,
                )
            )
        if "price_2024" in grouped.columns and grouped["price_2024"].notna().any():
            fig_bar.add_trace(
                go.Bar(
                    x=grouped[g],
                    y=y3,
                    name="2024",
                    marker_color=colors["2024"],
                    hovertext=hovertext_2024,
                    hoverinfo="text",
                    showlegend=True,
                )
            )
        fig_bar.update_layout(
            versus_graph.layout,
            xaxis=dict(title="Динамика цен по годам", tickformat="%d %b", tickangle=45),
            yaxis=dict(title="Цена"),
            hoverlabel=dict(align="left"),
            barmode="group",
            hovermode="x",
        )

        hovertext_q_2026 = format_hovertext(
            grouped[g], grouped.get("quantity_2026", pd.Series()), "2026", g, "q"
        )
        hovertext_q_2025 = format_hovertext(
            grouped[g], grouped.get("quantity_2025", pd.Series()), "2025", g, "q"
        )
        hovertext_q_2024 = format_hovertext(
            grouped[g], grouped.get("quantity_2024", pd.Series()), "2024", g, "q"
        )
        fig_bar_q = go.Figure()
        if (
            "quantity_2026" in grouped.columns
            and grouped["quantity_2026"].notna().any()
        ):
            fig_bar_q.add_trace(
                go.Bar(
                    x=grouped[g],
                    y=grouped["quantity_2026"],
                    name="2026",
                    marker_color=colors["2026"],
                    hovertext=hovertext_q_2026,
                    hoverinfo="text",
                    showlegend=True,
                )
            )
        if (
            "quantity_2025" in grouped.columns
            and grouped["quantity_2025"].notna().any()
        ):
            fig_bar_q.add_trace(
                go.Bar(
                    x=grouped[g],
                    y=grouped["quantity_2025"],
                    name="2025",
                    marker_color=colors["2025"],
                    hovertext=hovertext_q_2025,
                    hoverinfo="text",
                    showlegend=True,
                )
            )
        if (
            "quantity_2024" in grouped.columns
            and grouped["quantity_2024"].notna().any()
        ):
            fig_bar_q.add_trace(
                go.Bar(
                    x=grouped[g],
                    y=grouped["quantity_2024"],
                    name="2024",
                    marker_color=colors["2024"],
                    hovertext=hovertext_q_2024,
                    hoverinfo="text",
                    showlegend=True,
                )
            )
        fig_bar_q.update_layout(
            versus_graph.layout,
            xaxis=dict(
                title="Динамика количества по годам", tickformat="%d %b", tickangle=45
            ),
            yaxis=dict(title="Количество"),
            hoverlabel=dict(align="left"),
            barmode="group",
            hovermode="x",
        )

        return [
            fig_line,
            fig_bar,
            fig_bar_q,
            {"display": "block"},
            {"display": "block"},
        ]
