import os, pptx
from io import BytesIO
from django.conf import settings
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from .graphs import GrapghAttrs
import plotly.graph_objects as go
import plotly.express as px
import copy
import pandas as pd

class GraphManager:
    def __init__(self):
        self.brand_colors = GrapghAttrs.brand_colors
        self.layout = GrapghAttrs.get_default_layout()

    def cm_to_pixels(self, cm, ppi=96):
        return cm / 2.54 * ppi

    def cm_to_inches(self, cm):
        return cm / 2.54

    def create_linear_plot(
        self, df, x_column, y_column, color_col=None, width=435, height=240, label=None
    ):
        traces = []
        if color_col is not None:
            for model in df[color_col].unique():
                data = df[df[color_col] == model]
                trace = go.Scatter(
                    x=data[x_column],
                    y=data[y_column],
                    mode="lines",
                    line=dict(width=2, shape="spline"),
                    name=model,
                )
                traces.append(trace)
        else:
            trace = go.Scatter(
                x=df[x_column],
                y=df[y_column],
                mode="lines",
                line=dict(width=2, shape="spline"),
                name="Общая линия",
            )
            traces.append(trace)

        layout = copy.deepcopy(self.layout)

        layout.update(
            width=width, 
            height=height, 
            title=label,
            margin=dict(t=60, b=10, l=10, r=10)
            )

        return go.Figure(traces, layout)

    def create_tree_plot(self, df, labels, values):
        print(labels, values)
        fig = px.treemap(df, path=[labels], values=values)
        fig.update_layout(
            plot_bgcolor="#251421",
            paper_bgcolor="#251421",
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            xaxis_title="",
            yaxis_title="",
            margin=dict(l=0, r=0, t=0, b=0),
            width=width,
            height=height
        )

        return fig

    def create_bar_plot(self, df, x_column, y_column, color_col=None, width=435, height=240, label = None, type = "stack"):
        traces = []
        colors = px.colors.qualitative.Bold

        if color_col is not None:
            for i, category in enumerate(df[color_col].unique()):
                data = df[df[color_col] == category]
                trace = go.Bar(
                    x=data[x_column],
                    y=data[y_column],
                    name=category,
                    marker_color=colors[i % len(colors)],
                )
                traces.append(trace)
        else:
            trace = go.Bar(
                x=df[x_column],
                y=df[y_column],
                name=color_col,
                marker_color=colors[0],
            )
            traces.append(trace)

        layout = copy.deepcopy(self.layout)
                
        layout.update(
            width=width,
            height=height,
            barmode=type,
            title=label,
            showlegend=True,
            legend=dict(orientation='h', x=0, y=-0.2),
            margin=dict(t=60, b=10, l=10, r=10)
        )

        return go.Figure(traces, layout)
    
    def create_bar_plot_2_axes(self, df, x_column, y1_column, y2_column, width=435, height=240, label = None, type = "group"):
        traces = []
        trace = go.Bar(
            x=df[x_column],
            y=df[y1_column],
            name=y1_column,
        )
        traces.append(trace)
        trace = go.Bar(
        x=df[x_column],
        y=df[y2_column],
        name=y2_column,
        )
        traces.append(trace)
        layout = copy.deepcopy(self.layout)    
        layout.update(
            width=width,
            height=height,
            barmode=type,
            title=label,
            showlegend=True,
            legend=dict(orientation='h', x=0, y=-0.2),
            margin=dict(t=60, b=10, l=10, r=10)
        )

        return go.Figure(traces, layout)
