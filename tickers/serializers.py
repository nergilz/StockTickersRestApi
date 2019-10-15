from rest_framework import serializers
from tickers.models import Ticker


class TickerDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticker
        fields = '__all__'


class TickerListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Ticker
        fields = ('id', 'user', 'symbol')

    def get_queryset(self):
        return Ticker.objects.filter(pk=self.request.user.profile.id)
