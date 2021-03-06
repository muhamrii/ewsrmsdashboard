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
from rmsdash.forms import RequestHistoricalForm

@login_required(login_url="/login/")
def index(request):
    listdataserverupdate = TbServer.objects.raw('''SELECT * from tb_server, tb_cpu_ram_load where tb_server.servername = tb_cpu_ram_load.servername and timeid in (SELECT MAX(timeid) from tb_cpu_ram_load GROUP BY tb_cpu_ram_load.servername)''')
    #listdataserverupdate = TbServer.objects.all()
    registeredserver = TbServer.objects.all().distinct().count()
    lastupdate = TbCpuRamLoad.objects.order_by('-timeid').values('timeid').distinct()[:1]
    hitungactive = TbCpuRamLoad.objects.order_by().values('servername').filter(timeid__exact=lastupdate, sshstatus__exact="OK").distinct().count()
    hitungunmonitored = registeredserver - hitungactive
    context={
        'listdataserverupdate' : listdataserverupdate,
        'registeredserver' : registeredserver,
        'hitungactive' : hitungactive,
        'hitungunmonitored' : hitungunmonitored,
    }
    html_template = loader.get_template( 'realtime.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def realtime(request):
    listdataserverupdate = TbServer.objects.raw('''SELECT * from tb_server, tb_cpu_ram_load where tb_server.servername = tb_cpu_ram_load.servername and timeid in (SELECT MAX(timeid) from tb_cpu_ram_load GROUP BY tb_cpu_ram_load.servername)''')
    #listdataserverupdate = TbServer.objects.all()
    registeredserver = TbServer.objects.all().distinct().count()
    lastupdate = TbCpuRamLoad.objects.order_by('-timeid').values('timeid').distinct()[:1]
    hitungactive = TbCpuRamLoad.objects.order_by().values('servername').filter(timeid__exact=lastupdate, sshstatus__exact="OK").distinct().count()
    hitungunmonitored = registeredserver - hitungactive
    context={
        'listdataserverupdate' : listdataserverupdate,
        'registeredserver' : registeredserver,
        'hitungactive' : hitungactive,
        'hitungunmonitored' : hitungunmonitored,
    }
    html_template = loader.get_template( 'realtime.html' )
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def realtimedetail(request, servername):
    def plotram(filterserver):
        db_connection = sql.connect(host='localhost', database='db_ewsrmsdash', user='root', password='Last_12321', auth_plugin='mysql_native_password')
        df = pd.read_sql("select timeid, servername, memload,cpuload, sshstatus from tb_cpu_ram_load where timeid > now() - INTERVAL 24 HOUR;", con=db_connection)
        df = df.loc[df['servername'] == filterserver]
        fig = px.line(df, x="timeid", y="memload")
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    
    def plotcpu(filterserver):
        db_connection = sql.connect(host='localhost', database='db_ewsrmsdash', user='root', password='Last_12321', auth_plugin='mysql_native_password')
        df = pd.read_sql("select timeid, servername, memload,cpuload, sshstatus from tb_cpu_ram_load where timeid > now() - INTERVAL 24 HOUR;", con=db_connection)
        df = df.loc[df['servername'] == filterserver]
        fig = px.line(df, x="timeid", y="cpuload")
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    
    def plotdisk(filterserver):
        db_connection = sql.connect(host='localhost', database='db_ewsrmsdash', user='root', password='Last_12321', auth_plugin='mysql_native_password')
        df = pd.read_sql("select timeid, servername, filesystem, size, used, avail, percentageusage, mounted from tb_disk_capacity where timeid > now() - INTERVAL 24 HOUR;", con=db_connection)
        df = df.loc[df['servername'] == filterserver]
        fig = px.line(df, x="timeid", y="percentageusage", color="mounted", title="Disk Usage", hover_data=["size", "used", "avail"])
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    def plotinodes(filterserver):
        db_connection = sql.connect(host='localhost', database='db_ewsrmsdash', user='root', password='Last_12321', auth_plugin='mysql_native_password')
        df = pd.read_sql("select timeid, servername, filesystem, inodestotal, used, inodesfree, percentageiusage, mounted from tb_inodes_usage where timeid > now() - INTERVAL 24 HOUR;", con=db_connection)
        df = df.loc[df['servername'] == filterserver]
        fig = px.line(df, x="timeid", y="percentageiusage", color="mounted", title="Disk Inodes Usage", hover_data=["inodestotal", "used", "inodesfree"])
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    get_servername =  servername
    lastupdate = TbDiskCapacity.objects.order_by('-timeid').values('timeid').filter(servername__exact=get_servername).distinct()[:1]
    listdiskcapacity = TbDiskCapacity.objects.all().filter(timeid__exact=lastupdate).filter(servername__exact=get_servername)
    listinodesusage = TbInodesUsage.objects.all().filter(timeid__exact=lastupdate).filter(servername__exact=get_servername)
    listdataserverupdate = TbCpuRamLoad.objects.all().filter(servername__exact=get_servername).order_by('-timeid')[:1]
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
def requesthistory(request, servername):
    form = RequestHistoricalForm(request.POST or None)
    get_servername =  servername
    if request.method == "POST":
        if form.is_valid():
            startdate = form.cleaned_data.get("startdate")
            enddate = form.cleaned_data.get("enddate")
            startcompare = startdate.strftime("%Y-%m-%d %X")
            endcompare = enddate.strftime("%Y-%m-%d %X")
            def plotram(filterserver):
                db_connection = sql.connect(host='localhost', database='db_ewsrmsdash', user='root', password='Last_12321', auth_plugin='mysql_native_password')
                df = pd.read_sql("select timeid, servername, memload,cpuload, sshstatus from tb_cpu_ram_load;", con=db_connection)
                df = df.loc[df['servername'] == filterserver]
                df = df.loc[((df['timeid'] > startcompare) & (df['timeid'] <= endcompare))]
                fig = px.line(df, x="timeid", y="memload")
                plot_div = plot(fig, output_type='div', include_plotlyjs=False)
                return plot_div
            
            def plotcpu(filterserver):
                db_connection = sql.connect(host='localhost', database='db_ewsrmsdash', user='root', password='Last_12321', auth_plugin='mysql_native_password')
                df = pd.read_sql("select timeid, servername, memload,cpuload, sshstatus from tb_cpu_ram_load;", con=db_connection)
                df = df.loc[df['servername'] == filterserver]
                df = df.loc[((df['timeid'] > startcompare) & (df['timeid'] <= endcompare))]
                fig = px.line(df, x="timeid", y="cpuload")
                plot_div = plot(fig, output_type='div', include_plotlyjs=False)
                return plot_div

            def plotdisk(filterserver):
                db_connection = sql.connect(host='localhost', database='db_ewsrmsdash', user='root', password='Last_12321', auth_plugin='mysql_native_password')
                df = pd.read_sql("select timeid, servername, filesystem, size, used, avail, percentageusage, mounted from tb_disk_capacity;", con=db_connection)
                df = df.loc[df['servername'] == filterserver]
                df = df.loc[((df['timeid'] > startcompare) & (df['timeid'] <= endcompare))]
                fig = px.line(df, x="timeid", y="percentageusage", color="mounted", hover_data=["size", "used", "avail"])
                plot_div = plot(fig, output_type='div', include_plotlyjs=False)
                return plot_div
            
            def plotinodes(filterserver):
                db_connection = sql.connect(host='localhost', database='db_ewsrmsdash', user='root', password='Last_12321', auth_plugin='mysql_native_password')
                df = pd.read_sql("select timeid, servername, filesystem, inodestotal, used, inodesfree, percentageiusage, mounted from tb_inodes_usage;", con=db_connection)
                df = df.loc[df['servername'] == filterserver]
                df = df.loc[((df['timeid'] > startcompare) & (df['timeid'] <= endcompare))]
                fig = px.line(df, x="timeid", y="percentageiusage", color="mounted", hover_data=["inodestotal", "used", "inodesfree"])
                plot_div = plot(fig, output_type='div', include_plotlyjs=False)
                return plot_div
            
            listdataserverupdate = TbCpuRamLoad.objects.all().filter(servername__exact=get_servername).order_by('-timeid')[:1]
            lastupdate = TbDiskCapacity.objects.order_by('-timeid').values('timeid').filter(servername__exact=get_servername).distinct()[:1]
            context1={
                'startdate' : startdate,
                'enddate' : enddate,
                'servername' : get_servername,
                'listdataserverupdate' : listdataserverupdate,
                'plotram' : plotram(get_servername),
                'plotcpu' : plotcpu(get_servername),
                'plotdisk' : plotdisk(get_servername),
                'plotinodes' : plotinodes(get_servername),
            }
            html_template1 = loader.get_template( 'historical-detail.html' )
            return HttpResponse(html_template1.render(context1, request))

    listdataserverupdate = TbCpuRamLoad.objects.all().filter(servername__exact=get_servername).order_by('-timeid')[:1]
    context={
        'servername' : servername,
        'listdataserverupdate' : listdataserverupdate,
        'form' : form,
    }
    html_template = loader.get_template( 'form-historical.html' )
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