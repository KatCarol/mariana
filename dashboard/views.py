from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Sum
from django.views.generic import ListView

from .models import Drug, Batch, Invoice, Patient, SalesItem, Stock


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
            Batch.objects.create(drug=drug, stock=stock, quantity=quantity, batch_number=batch_number, expiration_date=expiration_date)

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
        
# Invoice create view
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


def patientPrescriptionView(request):
    context = {
        "patients": Patient.objects.all()
    }

    return render(request, 'dashboard/patients/patient-prescribe.html', context)
