from django.urls import path

from dashboard.views import DiagnosisCreateView, DiagnosisListView, InvoiceListView, PatientCreateView, PatientDeleteView, PatientDetailView, PatientListView, StockListView, drug_list, indexView, invoiceCreateView, stockInDrugs

app_name = 'dashboard'

urlpatterns = [
    path('', indexView, name='index'),
    path('drugs/', drug_list, name='drug-list'),
    path('stock/', StockListView.as_view(), name='stock-list'),
    path('stock/in/', stockInDrugs, name='stock-in'),
    path('sale/', invoiceCreateView, name='invoice-create'),
    path('invoicelist/', InvoiceListView.as_view(), name='invoice-list'),
    # patients
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('patients/new/', PatientCreateView.as_view(), name='patient-create'),
    path('patients/delete/<int:pk>/', PatientDeleteView.as_view(), name='patient-delete'),
    path('patients/records/', DiagnosisListView.as_view(), name='diagnosis-list'),
    path('patients/records/new/', DiagnosisCreateView.as_view(), name='diagnosis-create'),
]