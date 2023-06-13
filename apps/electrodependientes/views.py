from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.db.models import Value, F
from datetime import date

## Imports models
from apps.persona.models import Persona
from apps.inventario.models import DetallePrestamo
from apps.clasificadores.models import TipoParentesco, Empresa
from apps.electrodependientes.models import Electrodependiente,DocumentacionElectro ,Medico, TitularDeSuministro, Diagnostico

## Imports forms
from apps.electrodependientes.forms import ElectroForm, DocumentacionForm, MedicoForm, TitularSuministroFormSet, DiagnosticoFormSet
from apps.forms import TitularEditForm

# Helpers
from apps.helpers import getRoute

@permission_required('electrodependientes.add_electrodependiente', raise_exception=True)
def registrarElectro(request):

    electro = ElectroForm(usuario = request.user)
    documentacion = DocumentacionForm()
    titular = TitularSuministroFormSet(form_kwargs={'usuario': request.user})
    diagnostico = DiagnosticoFormSet()

    context = {
        'title' : 'Inscripcion al Registro de Electrodependientes por Cuestiones de Salud (RECS)',
        'electro': electro,
        'documentacion':documentacion,
        'titular': titular,
        'diagnostico': diagnostico,
        'segment': 'electro',
        'active': True
    }

    if 'confirmar' in request.POST:
        electro = ElectroForm(request.POST, request.FILES, usuario = request.user)
        titular = TitularSuministroFormSet(request.POST, form_kwargs={'usuario': request.user})
        diagnostico = DiagnosticoFormSet(request.POST)

        if len(request.FILES.getlist('documentacion')) > 5:
            electro.add_error('documentacion', "La cantidad de archivos supera el máximo permitido")

        if electro.is_valid() and titular.is_valid() and diagnostico.is_valid():

            print('Guardando instancias..')
            electro = electro.save()

            if len(request.FILES.getlist('documentacion')) > 0:
                for d in request.FILES.getlist('documentacion'):
                    doc = DocumentacionElectro(electrodependiente=electro, documentacion=d)
                    doc.save()

            if 'formulario' in request.FILES:
                formulario = DocumentacionElectro(electrodependiente=electro, formulario=request.FILES['formulario'])
                formulario.save()

            titular = titular.save(commit=False)
            for t in titular:
                t.electrodependiente = electro
                t.save()

            diagnostico = diagnostico.save(commit=False)
            for d in diagnostico:
                d.electrodependiente = electro
                d.save()

            return redirect('electrodependientes:listado_electro')

        else:
            context['electro'] = electro
            context['titular'] = titular
            context['diagnostico'] = diagnostico
            return render(request,'electro/registrar.html', context)

    return render(request,'electro/registrar.html', context)

@permission_required('electrodependientes.edit_electrodependiente', raise_exception=True)
def editarElectro(request):

    if 'confirmar_titular' in request.POST:

        electro = Electrodependiente.objects.get(pk = request.POST.get('id'))

        anterior_titular = TitularDeSuministro.objects.filter(electrodependiente = electro).last()
        anterior_titular.activo = False
        anterior_titular.usuario_modificacion = request.user.pk
        anterior_titular.save()

        nuevo_titular = TitularDeSuministro(
            electrodependiente = electro,
            titularServicio = Persona.objects.get(pk = request.POST.get('titular_servicio')),
            proveedor_suministro = Empresa.objects.get(pk = request.POST.get('proveedor_suministro')),
            vinculo = TipoParentesco.objects.get(pk = request.POST.get('vinculo')),
            numero_cliente = request.POST.get('nro_cliente'),
            usuario_creador = request.user
        )
        nuevo_titular.save()

    return redirect('electrodependientes:detalle_electro', pk=request.POST.get('id'))

@method_decorator(permission_required('electrodependientes.view_electrodependiente', raise_exception=True), name='dispatch')
class electroListView(ListView):
    paginate_by = 15
    model = Electrodependiente
    template_name = 'electro/listado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Crear url con filtros para mantener el paginador
        base_url = self.request.build_absolute_uri('/electro/listado?')
        url = getRoute(self, base_url)

        context["active"] = True
        context["url"] = url
        context["segment"] = 'electro listado-electro'
        context["title"] = 'Listado de electrodependientess registrados'
        return context

    def get_queryset(self):
        queryset = Electrodependiente.objects.filter(activo = True)

        if 'search' in self.request.GET:
            try:
                persona = Persona.objects.get(documento = self.request.GET.get('search'))
                queryset = Electrodependiente.objects.filter(persona_electrodependiente=persona, activo = True)

            except Exception as e:
                print(e)
                queryset = Electrodependiente.objects.none()

            return queryset

        return queryset

@method_decorator(permission_required('electrodependientes.view_electrodependiente', raise_exception=True), name='dispatch')
class electroDetailView(DetailView):
    model = Electrodependiente
    template_name = 'electro/detalle.html'

    def get_context_data(self, **kwargs):

        prestamos = DetallePrestamo.objects.filter(
            electro__persona_electrodependiente = self.get_object().persona_electrodependiente
        ).annotate(restante = F('fecha_devolucion') - Value(date.today())).order_by('regresado', 'restante')

        context = super().get_context_data(**kwargs)
        context["active"] = True
        context["title"] = 'Detalle persona electrodependiente'
        context["prestamos"] = prestamos
        context["titular_edit_form"] = TitularEditForm()
        context["titular"] = TitularDeSuministro.objects.filter(electrodependiente = self.get_object()).last()
        context["diagnostico"] = Diagnostico.objects.get(electrodependiente = self.get_object())
        return context

"""Medicos"""
@permission_required('electrodependientes.add_medico', raise_exception=True)
def registrarMedico(request):

    medico = MedicoForm(usuario = request.user)

    context = {
        'title' : 'Registrar médico',
        'medico': medico,
        'active': True
    }

    if 'confirmar' in request.POST:
        medico = MedicoForm(request.POST, usuario = request.user)

        if medico.is_valid():
            print('Guardando instancias..')
            medico = medico.save()
            return redirect('electrodependientes:listado_medico')
        else:
            return render(request,'electro/medico/registrar.html', context)

    return render(request,'electro/medico/registrar.html', context)

@method_decorator(permission_required('electrodependientes.view_medico', raise_exception=True), name='dispatch')
class medicoListView(ListView):
    paginate_by = 15
    model = Medico
    template_name = 'electro/medico/listado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Crear url con filtros para mantener el paginador
        base_url = self.request.build_absolute_uri('/electro/medico/listado?')
        url = getRoute(self, base_url)

        context["active"] = True
        context["url"] = url
        context["segment"] = 'electro listado-medico'
        context["title"] = 'Listado de personas electrodependientes'
        return context

    def get_queryset(self):
        queryset = Medico.objects.all()

        if 'search' in self.request.GET:
            try:
                queryset = Medico.objects.filter(matricula_profesional=self.request.GET.get('search'))

            except Exception as e:
                print(e)
                queryset = Medico.objects.none()

            return queryset

        return queryset
