from __future__       import absolute_import, unicode_literals
from celery           import shared_task, app
from celery.schedules import crontab

import requests

from django.contrib.auth          import authenticate
from django.core.management.base  import BaseCommand, CommandError
from django.contrib.auth.models   import User
from django.core.mail             import send_mail

from tickers.models               import Ticker, SubsTicker
from tickers_api_v2.settings      import API_KEY, API_URL, EMAIL_HOST_USER


@shared_task
def send_message_max(ticker, max_price, host, email):
    subject = 'WARNING in {}'.format(ticker)
    report  = 'In {} > Max price {}'.format(ticker, max_price)
    send_mail(subject, report, host, [email], fail_silently=False)


@shared_task
def send_message_min(ticker, min_price, host, email):
    subject = 'WARNING in {}'.format(ticker)
    report  = 'In {} < Min price {}'.format(ticker, min_price)
    send_mail(subject, report, host, [email], fail_silently=False)


@shared_task
def get_request(subs_ticker):
    pass


@shared_task
def get_data_from_vapi():
    
    try:
        subs_queryset = SubsTicker.objects.all()

    except Ticker.DoesNotExist:
        raise CommandError('does not exist')
    except SubscribeTicker.DoesNotExist:
        raise CommandError('does not exist')

    for subs_ticker in subs_queryset:

        payload = {
            "function": 'GLOBAL_QUOTE',
            "symbol"  : subs_ticker.ticker,
            "apikey"  : API_KEY,
            }

        try:
            response  = requests.get(API_URL, payload)
            data      = response.json()
            print(data)
        except requests.exceptions.HTTPError as error:
            print(' Requests ERROR:', error)

        try:
            if float(data['Global Quote']['03. high']) > float(subs_ticker.max_price):
                send_message_max(
                    subs_ticker.ticker,
                    subs_ticker.max_price,
                    EMAIL_HOST_USER,
                    subs_ticker.email
                    )                

            if float(data['Global Quote']['04. low']) < float(subs_ticker.min_price):
                send_message_min(
                    subs_ticker.ticker,
                    subs_ticker.min_price,
                    EMAIL_HOST_USER,
                    subs_ticker.email,
                    )

            Ticker.objects.create(
                user        = subs_ticker.user,
                symbol      = data['Global Quote']['01. symbol'],
                high        = data['Global Quote']['03. high'],
                low         = data['Global Quote']['04. low'],
                price       = data['Global Quote']['05. price'],
                trading_day = data['Global Quote']['07. latest trading day'],
                )

        except KeyError:
            print('**Standard API call frequency is 5 calls per minute and 500 calls per day!**')


################
#from datetime import timedelta
#from celery.task import periodic_task
# @periodic_task(run_every=(timedelta(seconds=5)), name='testprint')
# def test_task_1():
#     print('*** my FIRST periodic task ***')
