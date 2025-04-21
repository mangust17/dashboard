import pandas as pd
from django.utils import timezone
import random

# Функция для рассчета квантиля по модели для DF
def calculate_quantiles(group):
    if len(group.unique()) == 1:  # Если все значения одинаковые
        return 'Q1'
    quantiles = group.quantile([0.33, 0.66, 1.0])  # Вычисляем квантили
    quantiles_list = quantiles.tolist()
    # Добавляем малое значение к каждой границе бина, чтобы сделать их уникальными
    quantiles_list = [q + 0.000001 * i for i, q in enumerate(quantiles_list)]
    return pd.cut(group, bins=[float('-inf')] + quantiles_list, labels=['Q1', 'Q2', 'Q3'])

# Расчетная функция, которая добавляет дополнительные столбцы в модели
def gf_price_normalize(df):

    df=pd.DataFrame(df)
    try:
        df = df.groupby(['model','date'], as_index=False)[['price','quantity']].agg({'price':'mean','quantity':'sum'})
        df['model_sum'] = df.groupby(['model'], as_index=False)['price'].transform('mean')
        df['min_price'] = df.groupby(['model'], as_index=False)['price'].transform('min')
        df['median_price'] = df.groupby(['model'], as_index=False)['price'].transform('median')
        df['last_date'] = df.groupby(['model'], as_index = False)['date'].transform('max')
        df['current_price'] = df[df['date'] == df['last_date']]['price'] 
        df['price_normalized'] = df['price']/df['median_price']
        df['quantile'] = df.groupby('model')['price'].transform(calculate_quantiles)
        df['date'] = pd.to_datetime(df['date'])
        df['week']=df['date'].dt.isocalendar().week
        #   df.to_excel(f'C:/Users/atropinskiy/Desktop/excel/df{(random.randint(1,100))}.xlsx')
        # for index, row in df.iterrows():
        #     if not 0.95 <= row['price_normalized'] <= 1.05:
        #         df.at[index, 'price_normalized'] = 1
    except:
        df=pd.DataFrame()
    return df


# Дата бары с условным форматированием https://dash.plotly.com/datatable/conditional-formatting
def data_bars(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #0074D9 0%,
                    #0074D9 {max_bound_percentage}%,
                    #191C24 {max_bound_percentage}%,
                    #191C24 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'paddingBottom': 2,
            'paddingTop': 2
        })

    return styles


def data_bars_diverging(df, column, color_above='#3D9970', color_below='#FF4136'):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    col_max = df[column].max()
    col_min = df[column].min()
    ranges = [
        ((col_max - col_min) * i) + col_min
        for i in bounds
    ]
    midpoint = (col_max + col_min) / 2.

    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        min_bound_percentage = bounds[i - 1] * 100
        max_bound_percentage = bounds[i] * 100

        style = {
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'paddingBottom': 2,
            'paddingTop': 2
        }
        if max_bound > midpoint:
            background = (
                """
                    linear-gradient(90deg,
                    #191C24 0%,
                    #191C24 50%,
                    {color_above} 50%,
                    {color_above} {max_bound_percentage}%,
                    #191C24 {max_bound_percentage}%,
                    #191C24 100%)
                """.format(
                    max_bound_percentage=max_bound_percentage,
                    color_above=color_above
                )
            )
        else:
            background = (
                """
                    linear-gradient(90deg,
                    #191C24 0%,
                    #191C24 {min_bound_percentage}%,
                    {color_below} {min_bound_percentage}%,
                    {color_below} 50%,
                    #191C24 50%,
                    #191C24 100%)
                """.format(
                    min_bound_percentage=min_bound_percentage,
                    color_below=color_below
                )
            )
        style['background'] = background
        styles.append(style)

    return styles