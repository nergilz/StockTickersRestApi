from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from tickers.models import Ticker 
from tickers.serializers import TickerDetailSerializer, TickerListSerializer
from tickers.permissions import IsOwnerOrReadOnly
#from rest_framework.authentication import TokenAuthentication, SessionAuthentication


class TickerCreateView(generics.CreateAPIView):
    serializer_class    = TickerDetailSerializer
    permissions_classes = (IsAuthenticated, )


class TickerListView(generics.ListAPIView):
    serializer_class    = TickerListSerializer
    queryset            = Ticker.objects.all()
    permissions_classes = (IsAdminUser, )


class TickerRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class    = TickerDetailSerializer
    permissions_classes = (IsOwnerOrReadOnly, )
    #authentication_classes = (TokenAuthentication, SessionAuthentication, )

    def get_queryset(self):
        queryset = Ticker.objects.filter(user=self.request.user)
        return queryset
