from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from apps.productos.models import Producto

from core.services import ADWSGetDni, ADWSGetUsuarioYPass

# IMPORTS MODELOS
from apps.persona.models import Beneficiario
from apps.electrodependientes.models import Electrodependiente
from apps.clasificadores.models import PuntoVenta, Sucursal
from apps.inventario.models import Comprobante, DetalleDevolucion, Kardex, DetallePrestamo, DetalleRenovacion

# IMPORTS FORMS
from apps.inventario.forms import ComprobanteForm, DetalleRenovacionForm, DetalleEntradaFormSet, DetallePrestamoFormSet, DetalleDevolucionFormSet
from apps.forms import FilterForm

# Helpers
from apps.helpers import getRoute, getFilters

@permission_required('inventario.add_comprobante', raise_exception=True)
def newComprobante(request):

    comprobante = ComprobanteForm(instance=Comprobante(), usuario = request.user)
    sucursales = Sucursal.objects.all()

    context = {'title':'Agregar nuevo comprobante', 'sucursales':sucursales, 'segment':'inventario nuevo'}

    if 'continuar' in request.POST:

        sucursal = request.POST.get('sucursales')
        context['title'] = 'Nuevo comprobante'
        context['active'] = True

        if request.POST.get('tipo_comprobante_inicial') == 'CE':

            comprobante = ComprobanteForm(initial={'tipo_comprobante': 1, 'sucursal':sucursal}, usuario = request.user)
            comprobante.fields["punto_venta"].queryset = PuntoVenta.objects.filter(sucursal=sucursal)
            entradaFormset = DetalleEntradaFormSet()

            context['comprobante'] = comprobante
            context['entradaFormset'] = entradaFormset

        if request.POST.get('tipo_comprobante_inicial') == 'CP':

            comprobante = ComprobanteForm(initial={'tipo_comprobante': 2, 'sucursal':sucursal}, usuario = request.user)
            comprobante.fields["punto_venta"].queryset = PuntoVenta.objects.filter(sucursal=sucursal)
            prestamoFormset = DetallePrestamoFormSet(form_kwargs={'sucursal':sucursal, 'electro': False})

            context['comprobante'] = comprobante
            context['prestamoFormset'] = prestamoFormset

        if request.POST.get('tipo_comprobante_inicial') == 'CPE':

            comprobante = ComprobanteForm(initial={'tipo_comprobante': 2, 'sucursal':sucursal}, usuario = request.user)
            comprobante.fields["punto_venta"].queryset = PuntoVenta.objects.filter(sucursal=sucursal)
            prestamoFormset = DetallePrestamoFormSet(form_kwargs={'sucursal':sucursal, 'electro': True})

            context['comprobante'] = comprobante
            context['prestamoFormset'] = prestamoFormset

        if request.POST.get('tipo_comprobante_inicial') == 'CR':
            comprobante = ComprobanteForm(initial={'tipo_comprobante': 4, 'sucursal':sucursal}, usuario = request.user)
            comprobante.fields["punto_venta"].queryset = PuntoVenta.objects.filter(sucursal=sucursal)

            renovacion = DetalleRenovacionForm()
            renovacion.fields['producto'].queryset = Producto.objects.filter(sucursal=sucursal, situacion='OTO')

            context['comprobante'] = comprobante
            context['renovacion'] = renovacion

        if request.POST.get('tipo_comprobante_inicial') == 'CD':

            comprobante = ComprobanteForm(initial={'tipo_comprobante': 3, 'sucursal':sucursal}, usuario = request.user)
            comprobante.fields["punto_venta"].queryset = PuntoVenta.objects.filter(sucursal=sucursal)
            devolucionFormset = DetalleDevolucionFormSet(form_kwargs={'sucursal':sucursal})

            context['comprobante'] = comprobante
            context['devolucionFormset'] = devolucionFormset

    if 'guardar' in request.POST:

        sucursal = request.POST.get('sucursales')
        context['title'] = 'Nuevo comprobante'
        context['active'] = True

        # Comprobante de entrada
        if request.POST.get('tipo_comprobante') == '1':

            comprobante = ComprobanteForm(request.POST, usuario = request.user)
            entradaFormset = DetalleEntradaFormSet(request.POST)

            if comprobante.is_valid() and entradaFormset.is_valid():

                # Guardar instancias
                comprobante = comprobante.save()
                entrada = entradaFormset.save( commit=False )

                for e in entrada:
                    e.comprobante = comprobante
                    e.save()

                return redirect('/productos/listado')
            else:

                comprobante = ComprobanteForm(request.POST, usuario = request.user)
                entradaFormset = DetalleEntradaFormSet(request.POST)

                for entrada in entradaFormset:
                    for field in entrada.errors:
                        entrada[field].field.widget.attrs['class'] += ' is-invalid'

                context['comprobante'] = comprobante
                context['entradaFormset'] = entradaFormset

                return render(request,'inventario/inventario.html', context)

        #Comprobante de prestamo
        if request.POST.get('tipo_comprobante') == '2':

            comprobante = ComprobanteForm(request.POST, usuario = request.user)
            if 'detalleprestamo_set-0-electro' in request.POST:
                prestamoFormset = DetallePrestamoFormSet(request.POST, form_kwargs={'sucursal':request.POST['sucursal'], 'electro': True})
            else:
                prestamoFormset = DetallePrestamoFormSet(request.POST, form_kwargs={'sucursal':request.POST['sucursal'], 'electro': False})

            if comprobante.is_valid() and prestamoFormset.is_valid():

                # Guardar instancias
                comprobante = comprobante.save()
                prestamo = prestamoFormset.save( commit=False )

                for p in prestamo:
                    p.comprobante = comprobante
                    p.save()

                return redirect(reverse('inventario:print_comprobante', kwargs={ 'numero': comprobante.numero }))

        #Comprobante de devolución
        if request.POST.get('tipo_comprobante') == '3':

            comprobante = ComprobanteForm(request.POST, usuario = request.user)
            devolucionFormset = DetalleDevolucionFormSet(request.POST, form_kwargs={'sucursal':request.POST['sucursal']})

            if comprobante.is_valid() and devolucionFormset.is_valid():

                # Guardar instancias
                comprobante = comprobante.save()
                devolucion = devolucionFormset.save( commit=False )

                for d in devolucion:
                    d.comprobante = comprobante
                    d.save()

            return redirect(reverse('inventario:print_comprobante', kwargs={ 'numero': comprobante.numero }))

        #Comprobante de renovación
        if request.POST.get('tipo_comprobante') == '4':
            comprobante = ComprobanteForm(request.POST, usuario = request.user)
            renovacion = DetalleRenovacionForm(request.POST)

            if comprobante.is_valid() and renovacion.is_valid():
                comprobante = comprobante.save()
                renovacion = renovacion.save(commit=False)
                renovacion.comprobante = comprobante
                renovacion.save()

            return redirect(reverse('inventario:print_comprobante', kwargs={ 'numero': comprobante.numero }))

    return render(request,'inventario/inventario.html', context)


@permission_required('inventario.change_comprobante', raise_exception=True)
def historialComprobantes(request):

    comprobantes = {}

    if request.POST['electro'] == 'true':
        prestamos = DetallePrestamo.objects.filter(electro = request.POST['id'])
        renovaciones = DetalleRenovacion.objects.filter(electro = request.POST['id'])
        devoluciones = DetalleDevolucion.objects.filter(electro = request.POST['id'])
    else:
        prestamos = DetallePrestamo.objects.filter(beneficiario = request.POST['id'])
        renovaciones = DetalleRenovacion.objects.filter(beneficiario = request.POST['id'])
        devoluciones = DetalleDevolucion.objects.filter(beneficiario = request.POST['id'])

    prestamos = [{'cte':p.comprobante.numero, 'prod':p.producto.articulo.titulo, 'nserie':p.producto.numero_serie} for p in prestamos]
    renovaciones = [{'cte':r.comprobante.numero, 'prod':r.producto.articulo.titulo, 'nserie':r.producto.numero_serie} for r in renovaciones]
    devoluciones = [{'cte':d.comprobante.numero, 'prod':d.producto.articulo.titulo, 'nserie':d.producto.numero_serie} for d in devoluciones]

    comprobantes['prestamos-card'] = prestamos
    comprobantes['renovaciones-card'] = renovaciones
    comprobantes['devoluciones-card'] = devoluciones

    return JsonResponse({'data':comprobantes})

@permission_required('inventario.change_comprobante', raise_exception=True)
def printComprobante(request, numero):

    comprobante = get_object_or_404(Comprobante, numero=numero)
    usuario_documento = ADWSGetDni(comprobante.usuario_creador)
    usuario_datos = ADWSGetUsuarioYPass(comprobante.usuario_creador)
    usuario = {
        'documento': usuario_documento,
        'apellido' : usuario_datos['Apellido'],
        'nombre' : usuario_datos['Nombre']
    }

    if numero[:2] == 'CP':
        detalle = comprobante.detalleprestamo_set.last()
        template = 'inventario/pdf_prestamo.html'

    if numero[:2] == 'CR':
        detalle = comprobante.detallerenovacion
        template = 'inventario/pdf_renovacion.html'

    if numero[:2] == 'CD':
        detalle = comprobante.detalledevolucion_set.last()
        template = 'inventario/pdf_devolucion.html'

    try:
        persona = Beneficiario.objects.get(pk = detalle.beneficiario.pk).persona_beneficiaria
    except:
        persona = Electrodependiente.objects.get(pk = detalle.electro.pk).persona_electrodependiente

    context = {'comprobante':comprobante,'persona':persona,'detalle':detalle,'usuario':usuario}
    return render(request, template, context)

@method_decorator(permission_required('inventario.view_kardex', raise_exception=True), name='dispatch')
class KardexListView(ListView):
    paginate_by = 20
    model = Kardex
    template_name = 'inventario/kardex.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Crear url con filtros para mantener el paginador
        base_url = self.request.build_absolute_uri('/inventario/kardex?')
        url = getRoute(self, base_url)

        context["title"] = 'Kardex histórico'
        context["active"] = True
        context["url"] = url
        context["segment"] = 'inventario kardex'
        context["filter_form"] = FilterForm()
        return context

    def get_queryset(self):
        queryset = Kardex.objects.all().order_by('id')

        if 'search' in self.request.GET:
            try:
                comprobante = Comprobante.objects.get(numero = self.request.GET.get('search'))
                queryset = Kardex.objects.filter(comprobante = comprobante)

            except Exception as e:
                print(e)
                queryset = Kardex.objects.none()
            return queryset

        if 'filter' in self.request.GET:
            filters = getFilters(self)
            queryset = Kardex.objects.all().filter(**filters).order_by('articulo','fecha_operacion','cantidad_total')
            return queryset

        return queryset