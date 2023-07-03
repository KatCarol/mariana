from django.urls import path

from dashboard.views import DiagnosisCreateView, DiagnosisListView, DrugCreateView, DrugDeleteView, DrugDetailView, DrugUpdateView, InvoiceListView, PatientCreateView, PatientDeleteView, PatientDetailView, PatientListView, StockCreateView, StockListView, DrugListView, IndexView, InvoiceCreateView

app_name = 'dashboard'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('drugs/', DrugListView.as_view(), name='drug-list'),
    path('drugs/create', DrugCreateView.as_view(), name='drug-create'),
    path('drugs/update/<int:pk>/', DrugUpdateView.as_view(), name='drug-update'),
    path('drugs/detail/<int:pk>/', DrugDetailView.as_view(), name='drug-detail'),
    path('drugs/delete/<int:pk>/', DrugDeleteView.as_view(), name='drug-delete'),
    path('stock/', StockListView.as_view(), name='stock-list'),
    path('stock/in/', StockCreateView.as_view(), name='stock-in'),
    path('sale/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('invoicelist/', InvoiceListView.as_view(), name='invoice-list'),
    # patients
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('patients/new/', PatientCreateView.as_view(), name='patient-create'),
    path('patients/delete/<int:pk>/', PatientDeleteView.as_view(), name='patient-delete'),
    path('patients/records/', DiagnosisListView.as_view(), name='diagnosis-list'),
    path('patients/records/new/', DiagnosisCreateView.as_view(), name='diagnosis-create'),
]