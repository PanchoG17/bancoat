from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.db.models import Q, Value, F
from datetime import date, datetime
from django.utils import timezone
from django.http import HttpResponseRedirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

## Imports models
from apps.persona.models import Persona, Beneficiario, DocumentacionBeneficiario
from apps.electrodependientes.models import Electrodependiente
from apps.inventario.models import DetallePrestamo
from apps.clasificadores.models import TipoParentesco

## Imports forms
from apps.persona.forms import PersonaForm, BeneficiarioForm,DocumentacionFormset, PersonaEditForm
from apps.forms import BajasForm, ResponsableEditForm

# Helpers
from apps.helpers import getRoute

@permission_required('persona.add_persona', raise_exception=True)
def registrarPersona(request):

    persona = PersonaForm(usuario = request.user)

    context = {
        'title' : 'Registrar nueva persona',
        'persona': persona,
        'active': True
    }

    if 'confirmar' in request.POST:

        persona = PersonaForm(request.POST, usuario = request.user)

        if persona.is_valid():
            persona.save()
            return redirect('persona:listado_persona')
        else:
            persona = PersonaForm(request.POST, usuario = request.user)

            for field in persona.errors:
                persona[field].field.widget.attrs['class'] += ' is-invalid'

            context['persona'] = persona
            return render(request,'persona/registrar.html', context)

    return render(request,'persona/registrar.html', context)

@method_decorator(permission_required('persona.view_persona', raise_exception=True), name='dispatch')
class personaListView(ListView):
    paginate_by = 15
    model = Persona
    template_name = 'persona/listado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Crear url con filtros para mantener el paginador
        base_url = self.request.build_absolute_uri('/personas/listado?')
        url = getRoute(self, base_url)

        context["title"] = 'Listado de personas registradas'
        context["url"] = url
        context["segment"] = 'personas listado-personas'
        context["active"] = True
        return context

    def get_queryset(self):

        queryset = Persona.objects.filter(activo = True)

        if 'search' in self.request.GET:
            try:
                queryset = Persona.objects.filter(documento = self.request.GET.get('search'), activo = True)

            except Exception as e:
                queryset = Persona.objects.none()

            return queryset

        return queryset

@method_decorator(permission_required('persona.view_persona', raise_exception=True), name='dispatch')
class personaDetailView(UpdateView):
    model = Persona
    form_class = PersonaEditForm
    template_name = 'persona/detalle.html'

    def get_context_data(self, **kwargs):

        prestamos = DetallePrestamo.objects.filter(
            Q(beneficiario__persona_beneficiaria = self.get_object())|
            Q(electro__persona_electrodependiente = self.get_object())
        ).annotate(restante = F('fecha_devolucion') - Value(date.today())).order_by('regresado', 'restante')

        context = super().get_context_data(**kwargs)
        context["active"] = True
        context["title"] = 'Detalle de persona'
        context["baja_form"] = BajasForm()
        context["prestamos"] = prestamos
        return context

    def form_valid(self, form):
        form.instance.usuario_modificacion = self.request.user.pk
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

@permission_required('persona.edit_persona', raise_exception=True)
def setBajaPersona(request):

    if 'confirmar' in request.POST:
        persona = Persona.objects.get(pk = request.POST.get('id'))
        persona.activo = False
        persona.usuario_baja = request.user.pk
        persona.fecha_baja = datetime.now(tz=timezone.utc)
        persona.save()

        try:
            electro = Electrodependiente.objects.get(persona_electrodependiente = persona)
            electro.activo = False
            electro.usuario_baja = request.user.pk
            electro.fecha_baja = datetime.now(tz=timezone.utc)
            electro.save()
        except Exception as e:
            pass

        try:
            beneficiario = Beneficiario.objects.get(persona_beneficiaria = persona)
            beneficiario.activo = False
            beneficiario.usuario_baja = request.user.pk
            beneficiario.fecha_baja = datetime.now(tz=timezone.utc)
            beneficiario.save()
        except Exception as e:
            pass

    return redirect('persona:listado_persona')


"""
BENEFICIARIOS
"""
@permission_required('persona.add_beneficiario', raise_exception=True)
def registrarBeneficiario(request):

    beneficiario = BeneficiarioForm(usuario = request.user)
    #documentacion = DocumentacionForm()

    context = {
        'title' : 'Registrar beneficiario',
        'beneficiario': beneficiario,
        'active': True,
        #'documentacion': documentacion
    }

    if 'confirmar' in request.POST:

        beneficiario = BeneficiarioForm(request.POST, request.FILES, usuario = request.user)

        #documentacion = DocumentacionForm(request.POST, request.FILES)
        if beneficiario.is_valid(): #and documentacion.is_valid():
            beneficiario = beneficiario.save()
            # documentacion = documentacion.save(commit = False)
            # documentacion.beneficiario = beneficiario
            # documentacion = documentacion.save()

            return redirect('persona:listado_beneficiario')
        else:
            beneficiario = BeneficiarioForm(request.POST, request.FILES, usuario = request.user)
            #documentacion = DocumentacionForm(request.POST, request.FILES)

            for field in beneficiario.errors:
                beneficiario[field].field.widget.attrs['class'] += ' is-invalid'

            # for field in documentacion.errors:
            #     documentacion[field].field.widget.attrs['class'] += ' is-invalid'

            context['beneficiario'] = beneficiario
            #context['documentacion'] = documentacion
            return render(request,'persona/beneficiario/registrar.html', context)

    return render(request,'persona/beneficiario/registrar.html', context)

@permission_required('persona.edit_beneficiario', raise_exception=True)
def editarBeneficiario(request):

    if 'confirmar_responsable' in request.POST:

        beneficiario = Beneficiario.objects.get(pk = request.POST.get('id'))
        beneficiario.persona_responsable = Persona.objects.get(pk = request.POST.get('responsable'))
        beneficiario.vinculo = TipoParentesco.objects.get(pk = request.POST.get('vinculo'))
        beneficiario.save()

    if 'confirmar_documentacion' in request.POST:
        documentacionFormset = DocumentacionFormset(request.POST, request.FILES)
        if documentacionFormset.is_valid():
            beneficiario = Beneficiario.objects.get(pk = request.POST.get('id'))
            documentos = documentacionFormset.save( commit=False )
            for d in documentos:
                d.beneficiario = beneficiario
                d.save()

    return redirect('persona:detalle_beneficiario', pk=request.POST.get('id'))

@method_decorator(permission_required('persona.view_beneficiario', raise_exception=True), name='dispatch')
class beneficiarioListView(ListView):
    paginate_by = 15
    model = Beneficiario
    template_name = 'persona/beneficiario/listado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Crear url con filtros para mantener el paginador
        base_url = self.request.build_absolute_uri('/personas/beneficiario/listado?')
        url = getRoute(self, base_url)

        context["title"] = 'Listado de beneficiarios registrados'
        context["url"] = url
        context["segment"] = 'personas listado-beneficiarios'
        context["active"] = True
        return context

    def get_queryset(self):

        queryset = Beneficiario.objects.filter(activo = True)

        if 'search' in self.request.GET:
            try:
                persona = Persona.objects.get(documento = self.request.GET.get('search'), activo = True)
                queryset = Beneficiario.objects.filter(persona_beneficiaria = persona)

            except Exception as e:
                queryset = Beneficiario.objects.none()

            return queryset

        return queryset

@method_decorator(permission_required('persona.view_beneficiario', raise_exception=True), name='dispatch')
class beneficiarioDetailView(DetailView):
    model = Beneficiario
    template_name = 'persona/beneficiario/detalle.html'

    def get_context_data(self, **kwargs):

        prestamos = DetallePrestamo.objects.filter(
            beneficiario__persona_beneficiaria = self.get_object().persona_beneficiaria
        ).annotate(restante = F('fecha_devolucion') - Value(date.today())).order_by('regresado', 'restante')

        documentacionFormset = DocumentacionFormset()

        documentos = DocumentacionBeneficiario.objects.filter(beneficiario = self.get_object())

        context = super().get_context_data(**kwargs)
        context["active"] = True
        context["title"] = 'Detalle de beneficiario'
        context["documentacionFormset"] = documentacionFormset
        context["documentos"] = documentos
        context["responsable_edit_form"] = ResponsableEditForm()
        context["prestamos"] = prestamos
        return context
