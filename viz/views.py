from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
import pandas

from .models import Dct
from .forms import DBControllerForm
from django_pandas.io import read_frame

def db_controller_view(request):

    if request.method == 'POST':

        cell_lines = request.POST.getlist('cell_lines')
        genes = request.POST.getlist('genes')
        treatments = request.POST.getlist('treatments')
        time_points = request.POST.getlist('time_points')
        data = Dct.objects.filter(
            cell_line__in=cell_lines
        ).filter(
            gene__in=genes
        ).filter(
            treatment__in=treatments
        ).filter(
            time__in=time_points
        )
        # df_list = [pandas.DataFrame(i, index=[0]) for i in data]
        # df = pandas.concat(df_list)
        df = read_frame(data)
        json = df.to_json(orient='records')
        context = {
            'data': json,
            'columns': df.columns
        }
        return HttpResponse(df.to_html())
        # return render(request, '.', context)

    else:

        db_controller_form = DBControllerForm()

        return render(request, 'viz/index.html', {
            'db_controller_form': db_controller_form
        })


def data_table_view(request):

    if request.method == 'POST':

        cell_lines = request.POST.getlist('cell_lines')
        genes = request.POST.getlist('genes')
        treatments = request.POST.getlist('treatments')
        time_points = request.POST.getlist('time_points')
        data = Dct.objects.filter(
            cell_line__in=cell_lines
        ).filter(
            gene__in=genes
        ).filter(
            treatment__in=treatments
        ).filter(
            time__in=time_points
        )
        # df_list = [pandas.DataFrame(i, index=[0]) for i in data]
        # df = pandas.concat(df_list)
        df = read_frame(data)
        json = df.to_json(orient='records')
        context = {
            'data': json,
            'columns': df.columns
        }
        return render(request, 'viz/data_table.html', context=context)
        # return HttpResponse(df.to_html())

    else:
        raise NotImplementedError
    #
    #     db_controller_form = DBControllerForm()
    #
    #     return render(request, 'viz/index.html', {
    #         'db_controller_form': db_controller_form
    #     })



def test_view(request):
    hello = 'hello'
    # return HttpResponse(hello)
    return render(request, "viz/test.html", context={'hello': hello})


def inherit_from_test_view(request):
    django = 'Django'
    # return HttpResponse(hello)
    return render(request, "viz/inherit_from_test.html", context={'django': django })
































