from django.urls import path
from . import views


app_name = "naves"


urlpatterns = [
    path("", views.NaveLista.as_view(), name="nave_list"),
    path("nave/<int:pk>/", views.NaveDetalle.as_view(), name="nave_detail"),
    path("nave/nueva/", views.NaveCrear.as_view(), name="nave_create"),
    path("nave/<int:pk>/editar/", views.NaveEditar.as_view(), name="nave_update"),
    path("nave/<int:pk>/eliminar/", views.NaveEliminar.as_view(), name="nave_delete"),
    path("nave/<int:pk>/certificado/nuevo/", views.CertificadoCrear.as_view(), name="cert_create"),
    path("certificado/<int:pk>/editar/", views.CertificadoEditar.as_view(), name="cert_update"),
    path("certificado/<int:pk>/eliminar/", views.CertificadoEliminar.as_view(), name="cert_delete"),
]
