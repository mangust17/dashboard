from django.shortcuts import render

def dash_graph(request):
    return render(request, "dashboards/graph.html")


def plotly_dash(request):
    context = {}
    return render(request, "dashboards/plotly_dash.html", context)