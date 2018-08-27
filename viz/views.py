from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.forms import ModelForm
import pandas

from .models import Dct, Mean, Sem, Std
from .forms import DBControllerForm
from django_pandas.io import read_frame

from bokeh.plotting import figure
from bokeh.models import Legend, Whisker, ColumnDataSource
from bokeh.embed import components
import bokeh.palettes as palettes
from itertools import cycle


def plot_view(request):
    if request.method == 'POST':

        cell_lines = request.POST.getlist('cell_lines')
        genes = request.POST.getlist('genes')
        treatments = request.POST.getlist('treatments')
        time_points = request.POST.getlist('time_points')

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
        for cl in sorted(list(set(means.index.get_level_values(0)))):
            for tr in sorted(list(set(means.index.get_level_values(1)))):
                for g in sorted(list(set(means.index.get_level_values(2)))):
                    num_colours_needed += 1

        if num_colours_needed <= 2:
            colours = palettes.Plasma[3]
        else:
            colours = palettes.Plasma[num_colours_needed]

        def colour_gen():
            for c in cycle(colours):
                yield c

        cols = colour_gen()
        legend_items = []
        err_data = {}
        for cl in sorted(list(set(means.index.get_level_values(0)))):
            for tr in sorted(list(set(means.index.get_level_values(1)))):
                for g in sorted(list(set(means.index.get_level_values(2)))):

                    col = cols.__next__()
                    plot_data = means.loc[cl, tr, g]
                    err_data = sems.loc[cl, tr, g]

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
            'means': means,
            'sems': sems,
            'stds': stds,
            'db_controller_form': DBControllerForm(initial={
                'cell_lines': cell_lines,
                'treatments': treatments,
                'genes': genes,
                'time_points': time_points
            }),
            'script': script,
            'div': div
        }

        return render(request, 'viz/index.html', context=context)

    else:

        db_controller_form = DBControllerForm()

        return render(request, 'viz/index.html', {
            'db_controller_form': db_controller_form
        })

#
# def plot_view(request):
#     if request.method == 'POST':
#
#         cell_lines = request.POST.getlist('cell_lines')
#         genes = request.POST.getlist('genes')
#         treatments = request.POST.getlist('treatments')
#         time_points = request.POST.getlist('time_points')
#         data = Dct.objects.filter(
#             cell_line__in=cell_lines
#         ).filter(
#             gene__in=genes
#         ).filter(
#             treatment__in=treatments
#         ).filter(
#             time__in=time_points
#         )
#         df = read_frame(data)
#         json = df.to_json(orient='records')
#
#         x = [1, 3, 5, 7, 9, 11, 13]
#         y = [1, 2, 3, 4, 5, 6, 7]
#         title = 'y = f(x)'
#
#         plot = figure(title=title,
#                       x_axis_label='X-Axis',
#                       y_axis_label='Y-Axis',
#                       plot_width=400,
#                       plot_height=400)
#
#         plot.line(x, y, legend='f(x)', line_width=2)
#         # Store components
#         script, div = components(plot)
#
#         db_controller_form = DBControllerForm()
#
#         context = {
#             'data': df.to_html(),
#             'json': json,
#             'columns': df.columns,
#             'db_controller_form': db_controller_form,
#             'script': script,
#             'div': div,
#         }
#         return render(request, 'viz/index.html', context=context)
#         # return render(request, '.', context)
#
#     else:
#
#         db_controller_form = DBControllerForm()
#
#         return render(request, 'viz/index.html', {
#             'db_controller_form': db_controller_form
#         })
