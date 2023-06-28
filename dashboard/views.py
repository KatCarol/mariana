from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Sum
from django.views.generic import ListView, CreateView, DetailView

from dashboard.forms import DiagnosisForm, DiagnosisFormFull, DiagnosisFormSet, PatientForm

from .models import Diagnosis, Drug, Batch, Invoice, Patient, SalesItem, Stock


def drug_list(request):
    drugs = Drug.objects.annotate(total_quantity=Sum('batches__quantity'))
    return render(request, 'dashboard/drugs/drug-list.html', {'drugs': drugs})

def indexView(request):
    return render(request, 'dashboard/index.html', {})

# stock create view
def stockInDrugs(request):
    if request.method == 'POST':
        drug_ids = request.POST.getlist('drug')
        quantities = request.POST.getlist('quantity')
        batch_numbers = request.POST.getlist('batch_number')
        expiration_dates = request.POST.getlist('expiration_date')

        stock = Stock.objects.create()

        for drug_id, quantity, batch_number, expiration_date in zip(drug_ids, quantities, batch_numbers, expiration_dates):
            drug = Drug.objects.get(id=drug_id)
            Batch.objects.create(drug=drug, stock=stock, quantity=quantity, batch_number=batch_number, expiration_date=expiration_date, quantity_stocked=quantity)

        return redirect('dashboard:stock-in')

    context = {
        'stocks': Stock.objects.all(),
        'drugs': Drug.objects.all(),
    }
    return render(request, 'dashboard/stocks/stock-create.html', context)


class StockListView(ListView):
    model = Stock
    context_object_name = 'stocks'
    template_name = "dashboard/stocks/stock-list.html"


def pick_from_batch(batch, quantity):
    # case 1: batch quantity >= requested quantity
    # case 2: batch quantity < requested quantity
    if batch.quantity >= quantity:
        batch.quantity -= quantity
        batch.save()
        return 0
    else:
        quantity -= batch.quantity
        batch.quantity = 0
        batch.save()
        return quantity
        
# Invoices ===============================
def invoiceCreateView(request):
    if request.method == 'POST':
        drug_ids = request.POST.getlist('drug')
        quantities = request.POST.getlist('quantity')

        invoice = Invoice.objects.create()

        for drug_id, quantity in zip(drug_ids, quantities):
            if batches := Batch.objects.filter(drug=drug, quantity__gt=0).order_by('expiration_date'):
            
                batch_count = 0
                qtty = quantity

                while qtty != 0:
                    qtty = pick_from_batch(batches[batch_count], qtty)
                    batch_count+=1
            
            # TODO END
            drug = Drug.objects.get(id=drug_id)
            SalesItem.objects.create(invoice=invoice, drug=drug, quantity=quantity)

        return redirect('dashboard:invoice-list')

    context = {}
    return render(request, 'dashboard/invoices/invoice-create.html', context)

class InvoiceListView(ListView):
    model = Invoice
    context_object_name = 'invoices'
    template_name = "dashboard/invoices/invoice-list.html"


# Patients =============================
class PatientListView(ListView):
    model = Patient
    template_name = "dashboard/patients/patient-list.html"


class DiagnosisListView(ListView):
    model = Diagnosis
    template_name = "dashboard/patients/diagnosis-list.html"


class DiagnosisCreateView(CreateView):
    model = Diagnosis
    form_class = DiagnosisFormFull
    template_name = "dashboard/patients/patient-create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existing'] = True
        return context


class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "dashboard/patients/patient-create.html"
    success_url = 'dashboard:patient-list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['diagnosis_formset'] = DiagnosisFormSet(self.request.POST, prefix='diagnosis_formset')
        else:
            context['diagnosis_formset'] = DiagnosisFormSet(prefix='diagnosis_formset')
        context['existing'] = False
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        diagnosis_formset = context['diagnosis_formset']
        # print(diagnosis_formset)
        if diagnosis_formset.is_valid():
            self.object = form.save()
            diagnosis_formset.instance = self.object
            diagnosis_formset.save()
            print(diagnosis_formset)
            return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))


