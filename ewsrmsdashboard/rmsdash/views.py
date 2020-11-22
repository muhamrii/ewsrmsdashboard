from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from plotly.offline import plot
import plotly.graph_objects as go

@login_required(login_url="/login/")
def index(request):
    def scatter():
        x1 = [1,2,3,4]
        y1 = [30, 35, 25, 45]

        trace = go.Scatter(
            x=x1,
            y = y1
        )
        layout = dict(
            title='Simple Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis = dict(range=[min(y1), max(y1)])
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context = {}
    context['segment'] = 'index'
    context ={
        'plot1': scatter()
    }

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def realtime(request):
    context={}
    html_template = loader.get_template( 'realtime.html' )
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
