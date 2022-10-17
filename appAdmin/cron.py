import requests
import time
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import ipaddress
import socket
from .models import *
import platform
import subprocess

from urllib.parse import urlparse


Ip_Address = None


# methode pour  recuperer l'ip en fonction de l'url du site
def get_ip(url):
    hostname = socket.gethostbyname(urlparse(url).hostname)
    print('IP: {}'.format(hostname))
    if hostname:
        return ipaddress.IPv4Address(hostname)

# methode pour le ping
def ping(url):
    Ip_Address = get_ip(url)
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', str(Ip_Address)]
    return subprocess.call(command) == 0



# methode d'envoie de mail
# def send_alert_mail(site_objl):
#     print("mail enter  ", site_objl)
#     if site_objl:
#         email_list_notif = [obj.email for obj in User.objects.all()]
#         print("mail enter  ", email_list_notif)
#         message = render_to_string('site_alert_down.html', {
#             'site_obj': site_objl
#         })
#         mail_subject = 'Site Monitor - Alert Down .'
#         email = EmailMessage(mail_subject, message, to=email_list_notif)
#         email.send(fail_silently=False)


# methode executée toutes les 
def check_automatique_url():
    
    # recuperation de tous les sites actifs
    for url_obj in App.objects.filter(is_activate=True):
        # time.sleep(15)
        if url_obj:
            print("-------------r------------  ", url_obj.urls)
            # on essai d'atteindre l'url du site grace à r = requests.get(url_obj.urls)
            try:
                r = requests.get(url_obj.urls)
                # si le site passe
                if r.status_code == 200:
                    url_obj.status = True
                    url_obj.save()
                    Print("test")
                # si le site ne passe pas
                else:
                    url_obj.status = False
                    url_obj.save()
                    send_alert_mail(url_obj)
                    print(url_obj, "Site Currently down - alert sent2")

# scheduler = BackgroundScheduler()
# scheduler.start()
# scheduler.add_job(
#     func=check_automatique_url,
#     trigger=IntervalTrigger(seconds=2),
#     id='printing_time_job',
#     name='Print time every 2 seconds',
#     replace_existing=True)                    


           











