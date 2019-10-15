from __future__ import absolute_import, unicode_literals
from celery     import shared_task
from django.core.management.base  import CommandError
from django.core.mail             import send_mail
from tickers.models               import Ticker
from tickers_api_v2.settings      import API_KEY, API_URL, EMAIL_HOST_USER
import requests


@shared_task
def send_message(symbol, price, email, ident):
    subject = 'WARNING in {}'.format(symbol)
    report  = 'In Ticker: {} {} {}'.format(symbol, ident, price)
    send_mail(subject, report, EMAIL_HOST_USER, [email], fail_silently=False)


@shared_task
def get_response(ticker):

    symbol = ticker.symbol
    payload = {
        "function": 'GLOBAL_QUOTE',
        "symbol"  : symbol.upper(),
        "apikey"  : API_KEY,
        }
    response = requests.get(API_URL, payload)
    return response.json()


@shared_task
def get_data_from_vapi():
    
    try:
        queryset = Ticker.objects.all()

    except Ticker.DoesNotExist:
        raise CommandError('does not exist')

    for ticker in queryset:
        try:
            data = get_response(ticker)
            print(data)

        except requests.exceptions.HTTPError as err:
            print(' Requests ERROR:', err)

        try:
            if float(data['Global Quote']['03. high']) > float(ticker.max_price):
                send_message(
                    ticker.symbol,
                    ticker.max_price,
                    ticker.email,
                    '>_Maximum_price'
                    )
            if float(data['Global Quote']['04. low']) < float(ticker.min_price):
                send_message(
                    ticker.symbol,
                    ticker.min_price,
                    ticker.email,
                    '<_Minimum_price'
                    )
        except KeyError:
            print('**Standard API call frequency is 5 calls per minute and 500 calls per day!**')
