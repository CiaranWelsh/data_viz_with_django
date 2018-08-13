from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm

from .models import Dct
from .forms import NewForm, DctModelForm
# Create your views here.







def sql_builder(request, **kwargs):
    sql = "SELECT * from dct WHERE cell_type='A'"



def get_all(request, **kwargs):
    # dct = get_object_or_404(Dct)
    objs = Dct.objects.all()
    return HttpResponse('get_all return value')





# def get_name(request):
#     if request.method == 'POST':
#         form = NewForm(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('thanks')
#
#     else:
#         form = NewForm()
#
#     return render(request, 'viz/index.html', {'form': form})






def control_panel(request):
    # if request.method == 'POST':
    #     form = DctModelForm(request.POST)
    #     if form.is_valid():
    #         return HttpResponseRedirect('thanks')
    #
    # else:
    form = DctModelForm()

    return render(request, 'viz/index.html', {'form': form})





