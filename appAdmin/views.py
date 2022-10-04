from django.shortcuts import render, redirect
import requests
import xlwt
from django.http import HttpResponse, HttpResponseRedirect

import platform
import subprocess


import ipaddress
import socket
import sys
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from urllib.parse import urlparse
from django.core.paginator import Paginator
import json
from django.contrib import messages
from .forms import AppForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from appAdmin.models import App


Ip_Address = None
Page = 5

def send_alert_mail(site_objl):
    print("mail enter  ", site_objl)
    if site_objl:
        email_list_notif = [obj.email for obj in User.objects.all()]
        print("mail enter  ", email_list_notif)
        message = render_to_string('site_alert_down.html', {
            'site_obj': site_objl
        })
        mail_subject = 'Site Monitor - Alert Down .'
        email = EmailMessage(mail_subject, message, to=email_list_notif)
        email.send(fail_silently=False)





def get_ip(url):
    hostname = socket.gethostbyname(urlparse(url).hostname)
    print('IP: {}'.format(hostname))
    if hostname:
        return ipaddress.IPv4Address(hostname)


def ping(url):
    Ip_Address = get_ip(url)
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', str(Ip_Address)]
    return subprocess.call(command) == 0



def liste_objects(request):
    liste_obj = App.objects.all()
    paginator = Paginator(liste_obj, Page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    actif = App.objects.filter(status=True).count()
    inactif = App.objects.filter(status=False).count()
    total = actif + inactif

    context = {
        'liste_obj':page_obj,
        'nbActif':actif,
        'nbInactif':inactif,
        'total': total
    }

    return render(request, "index.html", context)

def actif_list(request):
    liste_obj = App.objects.filter(status=True)
    paginator = Paginator(liste_obj, Page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    actif = App.objects.filter(status=True).count()
    inactif = App.objects.filter(status=False).count()
    total = actif + inactif
    context = {
        'actif_list':page_obj,#json.loads(serializers.serialize("json", page_obj)),
        'nbActif':actif,
        'nbInactif':inactif,
        'total': total
    }
    print("---------",context)
    #return JsonResponse(data)
    return render(request, "actif_list.html",context)

def non_actif_list(request):
    liste_obj = App.objects.all().filter(status=False)
    paginator = Paginator(liste_obj, Page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    actif = App.objects.filter(status=True).count()
    inactif = App.objects.filter(status=False).count()
    total = actif + inactif
    context = {
        'non_actif_list':page_obj,
        'nbActif':actif,
        'nbInactif':inactif,
        'total': total
        }
    print("---------",context)
    #return JsonResponse(data)
    return render(request, "non_actif_list.html",context)

## search function #########
def search(request):
    search = request.GET['application']
    print("-------", search)
    liste_obj = App.objects.filter(application__icontains=search)

    actif = App.objects.filter(status=True).count()
    inactif = App.objects.filter(status=False).count()
    total = actif + inactif
    context = {
        'liste_obj':liste_obj,
        'nbActif':actif,
        'nbInactif':inactif,
        'total': total
        }
    print("---------",context)
    return render(request, "search.html",context)





def ping_url(request):
    print("---------  ",request.GET.get('id', ''))
    
    id = request.GET.get('id', '')
    url_obj = App.objects.filter(id=int(id),status=False)
    print("----url_obj-----  ", url_obj)
    data = {
        'status':'false',
        }
    if url_obj:
        data = {
        'status':'true',
        }
        send_alert_mail(url_obj[0])
        return JsonResponse(data)
    return JsonResponse(data)

        # try:
        #     r = requests.get(url_obj[0].urls+"?format=json")
        #     if r.status_code == 200:
        #         try:
        #             if ping(url_obj[0].urls):
        #                 url_obj[0].status = True
        #                 url_obj[0].status_serveur = True
        #                 url_obj[0].save()
        #                 data = {
        #                     'time':r.elapsed.total_seconds(),
        #                     'url': url_obj[0].urls,
        #                     'ip': Ip_Address,
        #                     'status_navigateur':'true',
        #                     'status_serveur': 'true',
        #                 }
        #                 return JsonResponse(data)
        #         except:

        #             url_obj[0].status = True
        #             url_obj[0].status_serveur = False
        #             url_obj[0].save()
        #             data = {
        #                 'time':r.elapsed.total_seconds(),
        #                 'url': url_obj[0].urls,
        #                 'ip': Ip_Address,
        #                 'status_navigateur':'true',
        #                 'status_serveur': 'false',
        #             }

        #             return JsonResponse(data)

        #     else:
        #         try:
        #             if ping(url_obj[0].urls):
        #                 url_obj[0].status = False
        #                 url_obj[0].status_serveur = True
        #                 url_obj[0].save()
        #                 data = {
        #                     'time':r.elapsed.total_seconds(),
        #                     'url': url_obj[0].urls,
        #                     'ip': Ip_Address,
        #                     'status_navigateur':'false',
        #                     'status_serveur': 'true',
        #                 }
        #                 return JsonResponse(data)
        #         except:

        #             url_obj[0].status = False
        #             url_obj[0].status_serveur = False
        #             url_obj[0].save()
        #             data = {
        #                 'time ': r.elapsed.total_seconds(),
        #                 'url': url_obj[0].urls,
        #                 'ip': Ip_Address,
        #                 'status_navigateur':'false',
        #                 'status_serveur': 'false',
        #             }

        #             return JsonResponse(data)
        # except:
        #     try:
        #         if ping(url_obj[0].urls):
        #             url_obj[0].status = False
        #             url_obj[0].status_serveur = True
        #             url_obj[0].save()
        #             data = {
        #                 'time ': "undefined",
        #                 'url': url_obj[0].urls,
        #                 'ip': Ip_Address,
        #                 'status_navigateur': 'false',
        #                 'status_serveur': 'true',
        #             }

        #             return JsonResponse(data)
        #     except:
        #         url_obj[0].status = False
        #         url_obj[0].status_serveur = False
        #         url_obj[0].save()
        #         data = {
        #             'time ': "undefined",
        #             'url': url_obj[0].urls,
        #             'ip': Ip_Address,
        #             'status_navigateur': 'false',
        #             'status_serveur': 'false',
        #         }

        #         return JsonResponse(data)
        # return JsonResponse(data)




def download_excel_data(request):
	response = HttpResponse(content_type='application/ms-excel')

	# decide file name
	response['Content-Disposition'] = 'attachment; filename="site web_url.xls"'

	# creating workbook
	wb = xlwt.Workbook(encoding='utf-8')

	# adding sheet
	ws = wb.add_sheet("sheet1")

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	# headers are bold
	font_style.font.bold = True

	# column header names, you can use your own headers here
	columns = ['Application', 'URL','STATUS']

	# write column headers in sheet
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	# get your data, from database or from a text file...
	data = App.objects.all().values_list('application', 'urls', 'status')  # dummy method to fetch data.
	for my_row in data:
		row_num = row_num + 1
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, my_row[col_num], font_style)

	wb.save(response)
	return response

#  class RegisterForm(CreateView):
# def link_form(request):
#     # model = App
#     # fields = ('application', 'urls', 'status', 'status_serveur') 
#     if request.method == 'POST':
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             app = form.save()
#             messages.success(request, "Registration successful." )
#             return redirect("liste_obj/")
#         messages.error(request, "Unsuccessful registration. Invalid information.")   
#     form = NewUserForm()
#     return render(request=request, template_name="link_form.html", context={"form": form})


 
def create_form(request):
    form = AppForm()
    return render(request, "link_form.html", {'form':form})

   