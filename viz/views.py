from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.forms import ModelForm
import pandas, numpy, os
from functools import reduce

from .models import Dct, Mean, Sem, Std, PcaDct, PcaDctExplainedVar
from .forms import DBControllerForm, PCAForm
from django_pandas.io import read_frame

from bokeh.plotting import figure
from bokeh.models import Legend, Whisker, ColumnDataSource, CustomJS
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, Button
from bokeh.embed import components
import bokeh.palettes as palettes
from itertools import cycle

import plotly.plotly as py
import plotly.offline as pyo
import plotly.graph_objs as go

import plotly.tools as plotly_tools


def base_view(request):
    """
    simply redirect user to index.html
    :param request:
    :return:
    """
    return redirect('index.html')


def form_handler(request):
    if request.method == 'POST':
        cell_lines = request.POST.getlist('cell_lines')
        genes = request.POST.getlist('genes')
        treatments = request.POST.getlist('treatments')
        time_points = request.POST.getlist('time_points')
    else:
        cell_lines = ['A', 'D', 'F']
        genes = ['ACTA2']
        treatments = ['TGFb']
        time_points = [0, 0.5, 1, 2, 4, 8, 12, 24, 48, 72, 96]

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

    print('means', means)

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


def do_plot(request, form_data=None):
    if form_data is None:
        form_data = form_handler(request=request)

    assert form_data is not None

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

    return script, div


def plot_view(request):
    """
    Django view to plot line graph based on post request parameters
    :param request:
    :return:
    """
    print('request type: ', request.method)
    if request.method == 'POST':
        form_data = form_handler(request)
        script, div = do_plot(request=request, form_data=form_data)
        print('post request from plot_view (index)')

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
        script, div = do_plot(request=request)

        return render(request, 'viz/index.html', {
            'db_controller_form': db_controller_form,
            'action': '.',
            'div': div,
            'script': script
        })


def process_form(data):
    means = pandas.DataFrame(data['means'].stack(), columns=['Mean'])
    sems = pandas.DataFrame(data['sems'].stack(), columns=['SEM'])
    df = pandas.concat([means, sems], axis=1).reset_index()

    cell_line_type_vec = []
    for i in df.cell_line:
        if i in ['A', 'B', 'C']:
            cell_line_type_vec.append('Neonatal')
        elif i in ['D', 'E', 'F']:
            cell_line_type_vec.append('Senescent')
        elif i in ['G', 'H', 'I']:
            cell_line_type_vec.append('Adult')
    df['cell_group'] = cell_line_type_vec
    return df


def data_table_view(request):
    if request.method == 'POST':

        form_data = form_handler(request)
        df = process_form(form_data)

        data = ColumnDataSource(df)
        # print(request.GET.get('width'))
        width = int(int(request.GET.get('width', 1000)) / 7)
        # print('new_width = ', width)
        columns = [
            TableColumn(field='cell_group', title='Cell Group', width=width),
            TableColumn(field='cell_line', title='Cell Line', width=int(width * 0.5)),
            TableColumn(field='treatment', title='Treatment', width=int(width * 0.7)),
            TableColumn(field='gene', title='Gene', width=width),
            TableColumn(field='time', title='Time', width=int(width * 0.5)),
            TableColumn(field='Mean', title='Mean', width=width, formatter=NumberFormatter(format='0.0000')),
            TableColumn(field='SEM', title='SEM', width=width, formatter=NumberFormatter(format='0.0000'))
        ]

        table_width = int(float(request.GET.get('width')) - 100)

        data_table = DataTable(
            source=data,
            columns=columns,
            fit_columns=False,
            selectable=True,
            width=table_width,
        )

        script, div = components(data_table)

        callback = CustomJS(code="function() {window.alert('callback mother fucker';};")
        btn = Button(label='Download as csv', button_type='success', callback=callback)

        btn_script, btn_div = components(btn)
        print(btn_script)
        print(btn_div)

        context = {
            'data': data,
            'means': form_data['means'],
            'sems': form_data['sems'],
            'stds': form_data['stds'],
            'db_controller_form': DBControllerForm(initial={
                'cell_lines': form_data['cell_lines'],
                'treatments': form_data['treatments'],
                'genes': form_data['genes'],
                'time_points': form_data['time_points']
            }),
            'action': r'data_table?width={}'.format(request.GET.get('width', 500)),
            'script': script,
            'div': div,
            'btn_script': btn_script,
            'btn_div': btn_div,
        }

        return render(request, 'viz/data_table.html', context)

    else:
        print('get request from data table')
        db_controller_form = DBControllerForm()

        return render(request, 'viz/data_table.html', {
            'db_controller_form': db_controller_form,
            'action': r'data_table?width={}'.format(request.GET.get('width', 500)),
        })


def download_button_view(request):
    form_data = form_handler(request)
    df = process_form(form_data)
    df = df[['cell_group', 'cell_line', 'treatment', 'gene', 'time', 'Mean', 'SEM']]
    print(df)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=data.csv'
    df.to_csv(path_or_buf=response, sep=',', index=False)
    return response


def pca_view(request):
    if request.method == 'POST':
        cell_lines = request.POST.getlist('cell_lines')
        # genes = request.POST.getlist('genes')
        treatments = request.POST.getlist('treatments')
        time_points = request.POST.getlist('time_points')
        replicates = request.POST.getlist('replicates')
        colour_by = request.POST.getlist('colour_by')

    else:
        cell_lines = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        treatments = ['TGFb', 'Control', 'Baseline']
        time_points = [0, 0.5, 1, 2, 4, 8, 12, 24, 48, 72, 96]
        replicates = [1, 2, 3, 4, 5, 6]
        colour_by = ['cell_lines']

    # if request.method == 'POST':
    pca_data = PcaDct.objects.filter(
        cell_id__in=cell_lines
    ).filter(
        replicate__in=replicates
    ).filter(
        treatment__in=treatments
    ).filter(
        time_point__in=time_points
    )

        explained_var = PcaDctExplainedVar.objects.all()
        explained_var = read_frame(explained_var, index_col='index')

        ## patch for bug fix. Make colour_by variables match
        ## the corresponding variables on tha back end for querying
        ## pca_data
        pca_data = read_frame(pca_data, index_col='index')
        for i in range(len(colour_by)):
            print('col by', colour_by[i])
            if colour_by[i] == 'time_points':
                colour_by[i] = 'time_point'

            elif colour_by[i] == 'replicates':
                colour_by[i] = 'replicate'

            elif colour_by[i] == 'treatments':
                colour_by[i] = 'treatment'

            elif colour_by[i] == 'cell_lines':
                colour_by[i] = 'cell_id'

            else:
                raise NotImplemented

        # print(pca_data.head())
        # print(colour_by)
        traces = []

        num_colours_needed = 0
        for label, df in pca_data.groupby(by=colour_by):
            num_colours_needed += 1

        c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in numpy.linspace(0, 350, num_colours_needed)]

        def color_gen():
            for i in c:
                yield i

        col = color_gen()
        for label, df in pca_data.groupby(by=colour_by):
            trace = go.Scatter3d(
                x=numpy.array(df['pc1']),
                y=numpy.array(df['pc2']),
                z=numpy.array(df['pc3']),
                mode='markers',
                marker={
                    'color': col.__next__(),
                    'opacity': 0.75
                },
                name=label if isinstance(label, (str, int, float)) else reduce(lambda x, y: "{}_{}".format(x, y), label)
            )
            traces.append(trace)

        layout = go.Layout(
            margin=dict(l=0, r=0, b=0, t=0),
            height=600,
            xaxis={
                'title': 'PC1 ({}% variance explained)'.format(explained_var.iloc[0]),
            },
            yaxis={'title': 'PC2 ({}% variance explained'.format(explained_var.iloc[1])},
            legend={
                'font': {
                    'size': 20
                },
                'y': 0.95  # Lower legend a little to keep away from modebar
            }
            # zaxis={'title': 'PC3 ({}% variance explained'.format(explained_var.iloc[2])}
        )
        fig = go.Figure(data=traces, layout=layout)

        p = pyo.plot(
            figure_or_data=fig,
            # layout=layout,
            output_type='div',
            # filename=filename,
            auto_open=False,
            config={'displayModeBar': True}
        )

        elif colour_by[i] == 'replicates':
            colour_by[i] = 'replicate'

        elif colour_by[i] == 'treatments':
            colour_by[i] = 'treatment'

        elif colour_by[i] == 'cell_lines':
            colour_by[i] = 'cell_id'

        else:
            raise NotImplemented

    traces = []

    num_colours_needed = 0
    for label, df in pca_data.groupby(by=colour_by):
        num_colours_needed += 1

    c = ['hsl(' + str(h) + ',50%' + ',50%)' for h in numpy.linspace(0, 350, num_colours_needed)]

    def color_gen():
        for i in c:
            yield i

    col = color_gen()
    for label, df in pca_data.groupby(by=colour_by):
        trace = go.Scatter3d(
            x=numpy.array(df['pc1']),
            y=numpy.array(df['pc2']),
            z=numpy.array(df['pc3']),
            mode='markers',
            marker={
                'color': col.__next__(),
                'opacity': 0.75
            },
            name=label if isinstance(label, (str, int, float)) else reduce(lambda x, y: "{}_{}".format(x, y), label)
        )
        traces.append(trace)

    layout = go.Layout(
        margin=dict(l=0, r=0, b=0, t=0),
        height=600,
        scene={
            'camera': {
                'up': {
                    'x': 0,
                    'y': 0,
                    'z': 1
                },
                'center': {
                    'x': 0,
                    'y': 0,
                    'z': 0
                },
                'eye': {
                    'x': 1.25,
                    'y': 1.25,
                    'z': 1.25
                }
            },
            'xaxis': {'title': 'PC1 ({}% variance explained)'.format(
                round(float(explained_var.iloc[0])*100), 2)},
            'yaxis': {'title': 'PC2 ({}% variance explained)'.format(
                round(float(explained_var.iloc[1])*100), 2)},
            'zaxis': {'title': 'PC3 ({}% variance explained)'.format(
                round(float(explained_var.iloc[2])*100), 2)},
        },


        legend={
            'font': {
                'size': 20
            }

        }
        # zaxis={'title': 'PC3 ({}% variance explained'.format(explained_var.iloc[2])}
    )
    fig = go.Figure(data=traces, layout=layout)

    p = pyo.plot(
        figure_or_data=fig,
        # layout=layout,
        output_type='div',
        # filename=filename,
        auto_open=False,
        config={'displayModeBar': False}
    )

    ## patch for bug fix. Swap cell_id for cell_lines
    ## for form on front end
    for i in range(len(colour_by)):
        if colour_by[i] == 'cell_id':
            colour_by[i] = 'cell_lines'

    initial = {
        'cell_lines': cell_lines,
        'treatments': treatments,
        'time_points': time_points,
        'replicates': replicates,
        'colour_by': colour_by
    }
    print(colour_by)
    context = {
        'pca_form': PCAForm(initial=initial),
        'data': p,
    }
    return render(request, 'viz/pca.html', context=context)

    # else:
    #
    #     return render(request, 'viz/pca.html', {
    #         'pca_form': PCAForm(),
    #     })
