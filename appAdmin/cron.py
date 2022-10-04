import requests
import time
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import requests
import ipaddress
import requests
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


# methode executée toutes les 
def check_automatique_url():
    
    # recuperation de tous les site actif
    for url_obj in App.objects.filter(is_activate=True):
        time.sleep(5)
        if url_obj:
            print("-------------r------------  ", url_obj.urls)
            # on essai d'atteindre l'url du site grace à r = requests.get(url_obj.urls)
            try:
                r = requests.get(url_obj.urls)
                # si le site passe
                if r.status_code == 200:
                    # on essai de faire le ping grace à ping(url_obj.urls)
                    try:
                        if ping(url_obj.urls):
                            url_obj.status = True
                            url_obj.status_serveur = True
                            url_obj.save()
                    # on met à jour le status du site en BD si le ping ne passe pas
                    except:
                        url_obj.status = True
                        url_obj.status_serveur = False
                        url_obj.save()
                # si le site ne passe pas
                else:
                    # on essai de faire le ping grace à ping(url_obj.urls)
                    try:
                        if ping(url_obj.urls):
                            url_obj.status = False
                            url_obj.status_serveur = True
                            url_obj.save()
                            send_alert_mail(url_obj)
                    # on met à jour le status du site en BD si le ping ne passe pas et on alert
                    except:
                        url_obj.status = False
                        url_obj.status_serveur = False
                        url_obj.save()
                        send_alert_mail(url_obj)
                        print(url_obj, "Site Currently down - alert sent2")
            # si l'on n'arrive pas à accéder grace à r = requests.get(url_obj.urls) on fait le ping sur le serveur
            except:
                # on essai de faire le ping grace à ping(url_obj.urls)
                try:
                    if ping(url_obj.urls):
                        url_obj.status = False
                        url_obj.status_serveur = True
                        url_obj.save()
                        send_alert_mail(url_obj)
                # on met à jour le status du site en BD si le ping ne passe pas et on alert
                except:
                    url_obj.status = False
                    url_obj.status_serveur = False
                    url_obj.save()
                    send_alert_mail(url_obj)
                    print(url_obj, "Site Currently down - alert sent4")












