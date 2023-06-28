from django.urls import path

from dashboard.views import InvoiceListView, StockListView, drug_list, indexView, invoiceCreateView, stockInDrugs

app_name = 'dashboard'

urlpatterns = [
    path('', indexView, name='index'),
    path('drugs/', drug_list, name='drug-list'),
    path('stock/', StockListView.as_view(), name='stock-list'),
    path('stock/in/', stockInDrugs, name='stock-in'),
    path('sale/', invoiceCreateView, name='invoice-create'),
    path('invoicelist/', InvoiceListView.as_view(), name='invoice-list'),
]