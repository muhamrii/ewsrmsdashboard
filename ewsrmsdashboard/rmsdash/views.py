from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import mysql.connector as sql
from rmsdash.models import TbServer,TbCpuRamLoad,TbDiskCapacity,TbInodesUsage

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
    listdataserverupdate = TbServer.objects.raw('''SELECT * from tb_server, tb_cpu_ram_load where tb_server.servername = tb_cpu_ram_load.servername and timeid=(select timeid from tb_cpu_ram_load order by timeid desc limit 1)''')
    context={
        'listdataserverupdate' : listdataserverupdate,
    }
    html_template = loader.get_template( 'realtime.html' )
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def realtimedetail(request, servername):
    def plotram(filterserver):
        db_connection = sql.connect(host='localhost', database='db_ewsrmsdash', user='root', password='Last_12321', auth_plugin='mysql_native_password')
        df = pd.read_sql("select timeid, servername, memload,cpuload, sshstatus from tb_cpu_ram_load where timeid > now() - INTERVAL 24 HOUR;", con=db_connection)
        df = df.loc[df['servername'] == filterserver]
        fig = px.line(df, x="timeid", y="memload", title="RAM LOAD")
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    
    def plotcpu(filterserver):
        db_connection = sql.connect(host='localhost', database='db_ewsrmsdash', user='root', password='Last_12321', auth_plugin='mysql_native_password')
        df = pd.read_sql("select timeid, servername, memload,cpuload, sshstatus from tb_cpu_ram_load where timeid > now() - INTERVAL 24 HOUR;", con=db_connection)
        df = df.loc[df['servername'] == filterserver]
        fig = px.line(df, x="timeid", y="cpuload", title="CPU LOAD")
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    
    def plotdisk(filterserver):
        db_connection = sql.connect(host='localhost', database='db_ewsrmsdash', user='root', password='Last_12321', auth_plugin='mysql_native_password')
        df = pd.read_sql("select timeid, servername, filesystem, size, used, avail, percentageusage, mounted from tb_disk_capacity where timeid > now() - INTERVAL 24 HOUR;", con=db_connection)
        df = df.loc[df['servername'] == filterserver]
        fig = px.line(df, x="timeid", y="percentageusage", color="mounted", title="Disk Usage")
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    def plotinodes(filterserver):
        db_connection = sql.connect(host='localhost', database='db_ewsrmsdash', user='root', password='Last_12321', auth_plugin='mysql_native_password')
        df = pd.read_sql("select timeid, servername, filesystem, inodestotal, used, inodesfree, percentageiusage, mounted from tb_inodes_usage where timeid > now() - INTERVAL 24 HOUR;", con=db_connection)
        df = df.loc[df['servername'] == filterserver]
        fig = px.line(df, x="timeid", y="percentageiusage", color="mounted", title="Disk Inodes Usage")
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    lastupdate = TbDiskCapacity.objects.order_by('-timeid').values('timeid').distinct()[:1]
    get_servername =  servername
    listdiskcapacity = TbDiskCapacity.objects.all().filter(timeid__exact=lastupdate).filter(servername__exact=get_servername)
    listinodesusage = TbInodesUsage.objects.all().filter(timeid__exact=lastupdate).filter(servername__exact=get_servername)
    listdataserverupdate = TbServer.objects.raw('''SELECT * from tb_server, tb_cpu_ram_load where tb_server.servername = tb_cpu_ram_load.servername and timeid=(select timeid from tb_cpu_ram_load order by timeid desc limit 1)''')
    context={
        'servername' : servername,
        'plotram' : plotram(servername),
        'plotcpu' : plotcpu(servername),
        'plotdisk' : plotdisk(servername),
        'plotinodes' : plotinodes(servername),
        'listdiskcapacity' : listdiskcapacity,
        'listinodesusage' : listinodesusage,
        'listdataserverupdate' : listdataserverupdate,
    }
    html_template = loader.get_template( 'realtime-detail.html' )
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
