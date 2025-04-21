import plotly.express as px
import pandas as pd
from .models import *
from django.db.models import Sum
import plotly.graph_objs as go


def gr_black_line(df, x, y, color):
    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        line_shape="linear",
        template="plotly_dark",
    )
    fig.update_traces(
        text=df[y],
        mode="markers+lines",
        textposition="top center",
        textfont_color="pink",
    )
    fig.update_layout(
        legend=dict(
            orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.24
        ),
        plot_bgcolor="#191C24",
        paper_bgcolor="#191C24",
        xaxis_title_font_color="#191C24",  # Цвет заголовка по оси X
        yaxis_title_font_color="#191C24",  # Цвет заголовка по оси Y
        xaxis_tickfont_color="#D840EF",  # Цвет меток по оси X
        yaxis_tickfont_color="#D840EF",  # Цвет меток по оси Y)
        xaxis_title="",
        yaxis_title="",
        margin=dict(l=0, r=20, t=20, b=0),
    )
    return fig


def gr_bar(df, x, y, colors):
    color_order = df[colors].unique()
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=colors,
        template="plotly_dark",
        orientation="v",
        category_orders={x: df[x].unique()},
    )
    fig.update_layout(
        title="Структура остатков",
        title_x=0.5,  # Расположение заголовка по горизонтали (центр)
        title_y=1,  # Расположение заголовка по вертикали (верх)
        legend=dict(
            orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.44
        ),
        plot_bgcolor="#191C24",
        paper_bgcolor="#191C24",
        xaxis_title_font_color="#DC23DC",  # Цвет заголовка по оси X
        yaxis_title_font_color="#D840EF",  # Цвет заголовка по оси Y
        xaxis_tickfont_color="#D840EF",  # Цвет меток по оси X
        yaxis_tickfont_color="#D840EF",  # Цвет меток по оси Y)
        xaxis_title="",
        yaxis_title="",
        margin=dict(l=0, r=40, t=20, b=10),
    )

    return fig


def gr_anim(df, x, y, date, model, quantity):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        animation_frame=date,
        animation_group=model,
        size=quantity,
        color=model,
    )
    fig.update_layout(
        legend=dict(
            orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.44
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title_font_color="#DC23DC",  # Цвет заголовка по оси X
        yaxis_title_font_color="#D840EF",  # Цвет заголовка по оси Y
        xaxis_tickfont_color="#D840EF",  # Цвет меток по оси X
        yaxis_tickfont_color="#D840EF",  # Цвет меток по оси Y)
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        xaxis_title="",
        yaxis_title="",
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        width=900,
        height=400,
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [
                            None,
                            {
                                "frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True,
                            },
                        ],
                        "label": "Play",
                        "method": "animate",
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.5,  # Положение бегунка по горизонтали
                "xanchor": "center",
                "y": 2.2,  # Положение бегунка по вертикали
                "yanchor": "top",
            }
        ],
    )
    return fig


def gr_tree(df, values, color):
    fig = px.treemap(df, path=["model"], values=values, color=color)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        xaxis_title="",
        yaxis_title="",
        margin=dict(l=0, r=0, t=0, b=0),
        height=270,
    )
    return fig


def gr_bar_normalized(df, x, y, color):
    df = df.groupby([x, color], as_index=False)["quantity"].sum()
    fig = px.bar(df, x=x, y=y, color=color)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        xaxis_title="",
        yaxis_title="",
        margin=dict(l=0, r=0, t=0, b=0),
        height=280,
        template="plotly_dark",
    )
    return fig


def gr_invoice_status():
    queryset_balance = CleanReportsBuy.objects.filter(quantity__gt=0)
    df = pd.DataFrame.from_records(queryset_balance.values())
    df = df.groupby(["invoice_id", "model_id_ns", "status"], as_index=False)[
        "quantity"
    ].sum()

    invoice_total = InvoiceContent.objects.values("invoice", "model_id").annotate(
        quantity=Sum("quantity")
    )
    df_invoices = pd.DataFrame.from_records(invoice_total)
    df_invoices["invoice"] = df_invoices["invoice"].astype(int)

    df_merged = (
        pd.merge(
            df_invoices,
            df,
            how="outer",
            left_on=["invoice", "model_id"],
            right_on=["invoice_id", "model_id_ns"],
            left_index=False,
        )
        .drop(["model_id_ns", "invoice_id"], axis=1)
        .fillna(0)
    )
    fig = px.bar(df_merged, "invoice", "quantity_x", color="status")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, zeroline=True),
        yaxis=dict(showgrid=False, zeroline=False),
        xaxis_title="",
        yaxis_title="",
        margin=dict(l=0, r=0, t=0, b=0),
        height=250,
        template="plotly_dark",
        legend=dict(
            orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.44
        ),
    )
    return fig


def gr_timeline(df, name_start, name_finish, y):
    fig = px.timeline(df, x_start=name_start, x_end=name_finish, y=y)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, zeroline=True),
        yaxis=dict(showgrid=False, zeroline=False),
        xaxis_title="",
        yaxis_title="",
        margin=dict(l=0, r=0, t=0, b=0),
        template="plotly_dark",
        height=160,
        showlegend=False,
    )
    return fig


class GrapghAttrs:
    brand_colors = {
        'rtk': "magenta",
        'itentive': "pink",
        'dihouse': "darkturquoise",
        'restore': "paleturquoise"
    }
    @staticmethod
    def get_default_layout():
        default_layout = go.Layout(
            margin=dict(l=20, r=0, b=0, t=20),
            plot_bgcolor="#191C24",
            paper_bgcolor="#191C24",
            font=dict(color="white"),
            legend=dict(orientation="h", x=0, y=-0.2),
            template="plotly_dark",
        )
        return default_layout
