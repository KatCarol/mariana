from rest_framework import serializers

from dashboard.models import Drug, Stock

# search about addind a field to a serializer
class DrugSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField('get_quantity')

    def get_quantity(self, drug):
        return drug.get_quantity()

    class Meta:
        model = Drug
        fields = ['name','description','manufacturer','selling_price','quantity']

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'