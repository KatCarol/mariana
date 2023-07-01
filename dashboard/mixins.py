from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class ClinicianRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is a clinician or superuser or admin."""

    def dispatch(self, request, *args, **kwargs):
            
        if (
            not request.user.is_superuser
            and not request.user.is_clinician
            and not request.user.is_admin
        ):
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

class SalesAttendantRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is a sales attendant or superuser or admin."""

    def dispatch(self, request, *args, **kwargs):
        if (
            not request.user.is_superuser
            and not request.user.is_sales_attendant
            and not request.user.is_admin
        ):
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an admin or superuser."""

    def dispatch(self, request, *args, **kwargs):
        if (
            not request.user.is_superuser
            and not request.user.is_admin
        ):
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)