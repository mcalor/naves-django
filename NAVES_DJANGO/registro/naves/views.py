from django.shortcuts import render
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView,UpdateView, DeleteView
from .models import Nave, Certificado
from .forms import NaveForm, CertificadoForm

class NaveLista(ListView):
    model = Nave
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q")
        tipo = self.request.GET.get("tipo")
        activa = self.request.GET.get("activa")
        qs = (Nave.objects.select_related("armador").annotate(cert_vigentes=Count("certificados", 
        filter=Q(certificados__fecha_vencimiento__gte=self.request.today))))
        if q:
            qs = qs.filter(Q(matricula__icontains=q)|Q(nombre__icontains=q)|Q(armador__nombre__icontains=q))
        if tipo:
            qs = qs.filter(tipo=tipo)
        if activa in ("true","false"):
            qs = qs.filter(activa=(activa=="true"))
        return qs.order_by("nombre")
    # pequeña ayuda para usar 'hoy' en annotate sin importar tz
    def dispatch(self, request, *args, **kwargs):
        from django.utils import timezone
        self.request.today = timezone.localdate()
        return super().dispatch(request, *args, **kwargs)
    
class NaveDetalle(DetailView):
    model = Nave
    
    def get_queryset(self):
        return (Nave.objects
            .select_related("armador")
            .prefetch_related("certificados"))
    
class NaveCrear(CreateView):
    model = Nave
    form_class = NaveForm
    success_url = reverse_lazy("naves:nave_list")

class NaveEditar(UpdateView):
    model = Nave
    form_class = NaveForm
    success_url = reverse_lazy("naves:nave_list")

class NaveEliminar(DeleteView):
    model = Nave
    success_url = reverse_lazy("naves:nave_list")

class CertificadoCrear(CreateView):
    model = Certificado
    form_class = CertificadoForm

    def form_valid(self, form):
        form.instance.nave_id = self.kwargs["pk"]
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("naves:nave_detail", kwargs={"pk":self.kwargs["pk"]})
    
class CertificadoEditar(UpdateView):
    model = Certificado
    form_class = CertificadoForm
    def get_success_url(self):
        return reverse_lazy("naves:nave_detail", kwargs={"pk":self.object.nave_id})
    
class CertificadoEliminar(DeleteView):
    model = Certificado

    def get_success_url(self):
        return reverse_lazy("naves:nave_detail", kwargs={"pk":self.object.nave_id})

