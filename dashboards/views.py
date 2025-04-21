from django.shortcuts import render

def dash_graph(request):
    return render(request, "dashboards/graph.html")
