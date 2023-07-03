from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.db.models import Sum
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView

from dashboard.forms import DiagnosisForm, DiagnosisFormFull, DiagnosisFormSet, DrugForm, PatientForm
from dashboard.mixins import ClinicianRequiredMixin, SalesAttendantRequiredMixin

from .models import Diagnosis, Drug, Batch, Invoice, Patient, SalesItem, Stock
from datetime import date
from django.contrib.auth import get_user_model

User = get_user_model()


# drugs ===========================================
class DrugListView(LoginRequiredMixin, ListView):
    model = Drug
    context_object_name = 'drugs'
    template_name = "dashboard/drugs/drug-list.html"

    def get_queryset(self) -> QuerySet[Any]:
        # the default queryset returns all the Drug objects so we are adding the quanitty to each of them
        return super().get_queryset().annotate(total_quantity=Sum('batches__quantity'))


class DrugDetailView(DetailView):
    model = Drug
    context_object_name = 'drug'
    template_name = "dashboard/drugs/drug-detail.html"

    def get_queryset(self) -> QuerySet[Any]:
        # the default queryset returns all the Drug objects so we are adding the quanitty to each of them
        return super().get_queryset().annotate(total_quantity=Sum('batches__quantity'))


class DrugCreateView(CreateView):
    model = Drug
    form_class = DrugForm
    context_object_name = 'drug'
    template_name = "dashboard/drugs/drug-create.html"
    success_url = "dashboard:drug-list"


class DrugUpdateView(UpdateView):
    model = Drug
    form_class = DrugForm
    context_object_name = 'drug'
    template_name = "dashboard/drugs/drug-update.html"
    success_url = reverse_lazy("dashboard:drug-list")


class DrugDeleteView(DeleteView):
    model = Drug
    context_object_name = 'drug'
    template_name = "dashboard/drugs/drug-delete.html"
    success_url = "dashboard:drug-list"






# dashboard =======================================
class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        batches = Batch.objects.filter(quantity__gt=0)
        expiring_soon = []
        for batch in batches:
            days = batch.daysToExpiry()
            if days < 31:
                expiring_soon.append(batch)
                
        count = len(expiring_soon)
        context = {
            'expiring': expiring_soon,
            'exp_count': count,
            'users': User.objects.all(),
        }
        return render(request, 'dashboard/index.html', context)

# stock create view

class StockCreateView(SalesAttendantRequiredMixin, View):
    def get(self, request):
        context = {
            'stocks': Stock.objects.all(),
            'drugs': Drug.objects.all(),
        }
        return render(request, 'dashboard/stocks/stock-create.html', context)
    
    def post(self, request):
        drug_ids = request.POST.getlist('drug')
        quantities = request.POST.getlist('quantity')
        batch_numbers = request.POST.getlist('batch_number')
        expiration_dates = request.POST.getlist('expiration_date')

        stock = Stock.objects.create()

        for drug_id, quantity, batch_number, expiration_date in zip(drug_ids, quantities, batch_numbers, expiration_dates):
            drug = Drug.objects.get(id=drug_id)
            Batch.objects.create(drug=drug, stock=stock, quantity=quantity, batch_number=batch_number, expiration_date=expiration_date, quantity_stocked=quantity)

        return redirect('dashboard:stock-list')

class StockListView(SalesAttendantRequiredMixin, ListView):
    model = Stock
    context_object_name = 'stocks'
    template_name = "dashboard/stocks/stock-list.html"

    def get_queryset(self):
        queryset = super(StockListView, self).get_queryset()
        queryset = queryset.order_by('-date')
        return queryset

# Invoices ===============================

# function to pick sold products from a batch
def pick_from_batch(batch, quantity):
    # case 1: batch quantity >= requested quantity
    # case 2: batch quantity < requested quantity
    quantity=int(quantity)
    if batch.quantity >= quantity:
        batch.quantity -= quantity
        batch.save()
        return 0
    else:
        quantity -= batch.quantity
        batch.quantity = 0
        batch.save()
        return quantity

class InvoiceCreateView(SalesAttendantRequiredMixin, View):
    def get(self, request):
        context = {
            'drugs': Drug.objects.all(),
        }
        return render(request, 'dashboard/invoices/invoice-create.html', context)

    def post(self, request):
        drug_ids = request.POST.getlist('drug')
        quantities = request.POST.getlist('quantity')

        invoice = Invoice.objects.create()

        for drug_id, quantity in zip(drug_ids, quantities): # loop through both lists of drug_ids and quantities

            drug = Drug.objects.get(id=drug_id)
            if batches := Batch.objects.filter(drug=drug, quantity__gt=0).order_by('expiration_date'):
            
                batch_count = 0
                qtty = quantity

                while qtty != 0:
                    qtty = pick_from_batch(batches[batch_count], qtty)
                    batch_count+=1
            
            # TODO END
            SalesItem.objects.create(invoice=invoice, drug=drug, quantity=quantity)

        return redirect('dashboard:invoice-list')

class InvoiceListView(SalesAttendantRequiredMixin, ListView):
    model = Invoice
    context_object_name = 'invoices'
    template_name = "dashboard/invoices/invoice-list.html"

# Patients =============================
class PatientListView(ClinicianRequiredMixin, ListView):
    model = Patient
    template_name = "dashboard/patients/patient-list.html"

class DiagnosisListView(ClinicianRequiredMixin, ListView):
    model = Diagnosis
    template_name = "dashboard/patients/diagnosis-list.html"

class DiagnosisCreateView(ClinicianRequiredMixin, CreateView):
    model = Diagnosis
    form_class = DiagnosisFormFull
    template_name = "dashboard/patients/patient-create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existing'] = True
        return context

class PatientCreateView(ClinicianRequiredMixin, CreateView):
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

class PatientDeleteView(ClinicianRequiredMixin, DeleteView):
    model = Patient
    template_name = "dashboard/patients/patient-delete.html"
    success_url = reverse_lazy('dashboard:patient-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object
        return context

class PatientDetailView(ClinicianRequiredMixin, DetailView):
    model = Patient
    context_object_name = 'patient'
    template_name = "dashboard/patients/patient-detail.html"

