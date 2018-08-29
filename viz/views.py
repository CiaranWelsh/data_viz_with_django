from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.forms import ModelForm
import pandas

from .models import Dct, Mean, Sem, Std
from .forms import DBControllerForm
from django_pandas.io import read_frame

from bokeh.plotting import figure
from bokeh.models import Legend, Whisker, ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.embed import components
import bokeh.palettes as palettes
from itertools import cycle


def base_view(request):
    """
    simply redirect user to index.html
    :param request:
    :return:
    """
    return redirect('index.html')


def form_handler(request):
    cell_lines = request.POST.getlist('cell_lines')
    genes = request.POST.getlist('genes')
    treatments = request.POST.getlist('treatments')
    time_points = request.POST.getlist('time_points')

    # print('genes', genes)
    # print('cell_linres', cell_lines)
    # print('treatments', treatments)
    # print('time', time_points)

    # for i in [cell_lines, genes, treatments, time_points]:
    #     print(i, i==[])
    #     if i == []:
    #         db_controller_form = DBControllerForm()
    #
    #         return render(request, 'viz/base.html', {
    #             'db_controller_form': db_controller_form
    #         })

    means = Mean.objects.filter(
        cell_line__in=cell_lines
    ).filter(
        gene__in=genes
    ).filter(
        treatment__in=treatments
    ).filter(
        time__in=time_points
    )

    sems = Sem.objects.filter(
        cell_line__in=cell_lines
    ).filter(
        gene__in=genes
    ).filter(
        treatment__in=treatments
    ).filter(
        time__in=time_points
    )

    stds = Std.objects.filter(
        cell_line__in=cell_lines
    ).filter(
        gene__in=genes
    ).filter(
        treatment__in=treatments
    ).filter(
        time__in=time_points
    )

    means = read_frame(means, index_col='index')
    sems = read_frame(sems, index_col='index')
    stds = read_frame(stds, index_col='index')

    means = means.pivot_table(
        values='value',
        index=['cell_line', 'treatment', 'gene'],
        columns='time',
    )
    sems = sems.pivot_table(
        values='value',
        index=['cell_line', 'treatment', 'gene'],
        columns='time',
    )
    stds = stds.pivot_table(
        values='value',
        index=['cell_line', 'treatment', 'gene'],
        columns='time',
    )
    return {'means': means,
            'sems': sems,
            'stds': stds,
            'genes': genes,
            'cell_lines': cell_lines,
            'treatments': treatments,
            'time_points': time_points}


def plot_view(request):
    """
    Django view to plot line graph based on post request parameters
    :param request:
    :return:
    """
    print('request type: ', request.method)
    if request.method == 'POST':

        print('post request from plot_view (index)')

        form_data = form_handler(request)

        TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

        plot = figure(
            sizing_mode='stretch_both',
            x_axis_label='Time (h)',
            y_axis_label='Normalised Cycle Threshold',
            tools=TOOLS,
            toolbar_location='above'
        )
        plot.xaxis.axis_label_text_font_size = '20pt'
        plot.yaxis.axis_label_text_font_size = '20pt'

        plot.xaxis.major_label_text_font_size = '18pt'
        plot.yaxis.major_label_text_font_size = '18pt'

        plot.xgrid.visible = False
        plot.ygrid.visible = False

        num_colours_needed = 0
        for cl in sorted(list(set(form_data['means'].index.get_level_values(0)))):
            for tr in sorted(list(set(form_data['means'].index.get_level_values(1)))):
                for g in sorted(list(set(form_data['means'].index.get_level_values(2)))):
                    num_colours_needed += 1

        if num_colours_needed <= 2:
            colours = palettes.Plasma[3]
        else:
            colours = palettes.Plasma[num_colours_needed]

        def colour_gen():
            for c in cycle(colours):
                yield c

        cols = colour_gen()
        for cl in sorted(list(set(form_data['means'].index.get_level_values(0)))):
            for tr in sorted(list(set(form_data['means'].index.get_level_values(1)))):
                for g in sorted(list(set(form_data['means'].index.get_level_values(2)))):

                    col = cols.__next__()
                    plot_data = form_data['means'].loc[cl, tr, g]
                    err_data = form_data['sems'].loc[cl, tr, g]

                    legend_label = '{}_{}_{}'.format(g, cl, tr),

                    err_xs = []
                    err_ys = []

                    for x, y, err in zip(list(plot_data.index), plot_data.values, err_data.values):
                        err_xs.append((x, x))
                        err_ys.append((y - err, y + err))

                    lin = plot.line(
                        list(plot_data.index),
                        plot_data.values,
                        color=col,
                        line_width=5,
                        legend=legend_label[0],
                        alpha=0.75
                    )

                    circ = plot.circle(
                        list(plot_data.index),
                        plot_data.values,
                        color=col,
                        size=15,
                        legend=legend_label[0],
                        alpha=0.5
                    )

                    ##plot errors
                    errs = plot.multi_line(
                        err_xs, err_ys,
                        line_width=4,
                        color=col,
                        alpha=0.5,
                        legend=legend_label[0]
                    )

        plot.legend.label_text_font_size = '20pt'
        plot.legend.location = 'top_left'
        plot.legend.click_policy = 'hide'

        script, div = components(plot)

        context = {
            'means': form_data['means'],
            'sems': form_data['sems'],
            'stds': form_data['stds'],
            'db_controller_form': DBControllerForm(initial={
                'cell_lines': form_data['cell_lines'],
                'treatments': form_data['treatments'],
                'genes': form_data['genes'],
                'time_points': form_data['time_points']
            }),
            'action': '.',
            'script': script,
            'div': div
        }

        return render(request, 'viz/index.html', context=context)

    else:
        print('get request from plot_view (index)')
        db_controller_form = DBControllerForm()

        return render(request, 'viz/index.html', {
            'db_controller_form': db_controller_form,
            'action': '.',
        })


def data_table_view(request):
    if request.method == 'POST':

        form_data = form_handler(request)

        # print(form_data)

        data = dict(
            mean=form_data['means'],
            SEM=form_data['sems']
        )
        source = ColumnDataSource(data)

        columns = [
            TableColumn(field='means', title='means'),
            TableColumn(field='sems', title='sems'),
        ]
        data_table = DataTable(source=source, columns=columns)

        script, div = components(data_table)

        context = {
            'means': form_data['means'],
            'sems': form_data['sems'],
            'stds': form_data['stds'],
            'db_controller_form': DBControllerForm(initial={
                'cell_lines': form_data['cell_lines'],
                'treatments': form_data['treatments'],
                'genes': form_data['genes'],
                'time_points': form_data['time_points']
            }),
            'action': r'data_table.html',
            'script': script,
            'div': div
        }

        return render(request, 'viz/data_table.html', context)

    else:
        print('get request from data table')
        db_controller_form = DBControllerForm()

        return render(request, 'viz/data_table.html', {
            'db_controller_form': db_controller_form,
            'action': 'data_table.html',
        })


def pca_view(request):
    if request.method == 'POST':
        return HttpResponse('pca')

    else:
        print('get request from plot_view (index)')
        db_controller_form = DBControllerForm()

        return render(request, 'viz/pca.html', {
            'db_controller_form': db_controller_form,
            'action': 'viz/index.html',

        })