from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.db.models import Value, F, Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

from datetime import date

# Helpers
from apps.helpers import setStatus, getRoute, getFilters

# Import models
from apps.productos.models import Producto, ProductoBaja, Articulo, Marca, Categoria, Subcategoria
from apps.inventario.models import DetallePrestamo
from apps.persona.models import Persona

# Import forms
from apps.forms import FilterForm
from apps.productos.forms import ArticuloForm, MarcaForm, CategoriaForm, SubcategoriaForm


## Productos ##
@method_decorator(permission_required('productos.view_producto', raise_exception=True), name='dispatch')
class productosListView(ListView):
    paginate_by = 15
    model = Producto
    template_name = 'productos/listado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Crear url con filtros para mantener el paginador
        base_url = self.request.build_absolute_uri('/productos/listado?')
        url = getRoute(self, base_url)

        context["title"] = 'Listado de productos'
        context["active"] = True
        context["url"] = url
        context["segment"] = 'inventario productos'
        context["filter_form"] = FilterForm()
        return context

    def get_queryset(self):

        queryset = Producto.objects.all().order_by('articulo')

        if 'search' in self.request.GET:
            try:
                queryset = Producto.objects.filter(numero_serie = self.request.GET.get('search'))
            except Exception as e:
                queryset = Producto.objects.none()
            return queryset

        if 'filter' in self.request.GET:
            filters = getFilters(self)
            queryset = Producto.objects.all().filter(**filters)
            return queryset

        return queryset

@method_decorator(permission_required('productos.view_producto', raise_exception=True), name='dispatch')
class otorgadosListView(ListView):
    paginate_by = 15
    model = DetallePrestamo
    template_name = 'productos/listado-otorgados.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Crear url con filtros para mantener el paginador
        base_url = self.request.build_absolute_uri('/productos/otorgados?')
        url = getRoute(self, base_url)

        context["title"] = 'Listado de productos otorgados'
        context["active"] = True
        context["url"] = url
        context["segment"] = 'inventario otorgados'
        return context

    def get_queryset(self):
        queryset = DetallePrestamo.objects.filter(regresado = False).annotate(restante = F('fecha_devolucion') - Value(date.today())).order_by('baja','restante')

        if 'search' in self.request.GET:
            try:
                persona = Persona.objects.get(documento = self.request.GET.get('search'))
                queryset = DetallePrestamo.objects.filter(Q(beneficiario__persona_beneficiaria = persona) | Q(electro__persona_electrodependiente = persona),regresado = False).annotate(restante = F('fecha_devolucion') - Value(date.today())).order_by('baja','restante')

            except Exception as e:
                queryset = DetallePrestamo.objects.none()

            return queryset

        return queryset

@permission_required('productos.change_producto', raise_exception=True)
def bajaProducto(request):
    if 'confirmar' in request.POST:
        producto = Producto.objects.filter(pk = request.POST['id'])

        if producto[0].situacion == 'OTO':
            prestamo = DetallePrestamo.objects.filter(producto = producto[0], regresado=False)
            prestamo.update(baja = True)

        baja = ProductoBaja(
            producto = producto[0],
            motivo_baja = request.POST['motivo_baja'],
            fecha_baja = request.POST['fecha_baja'],
            usuario_baja = request.user
        )
        baja.save()
        producto.update(situacion = 'NO_DISP')

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

## Articulos ##
@permission_required('productos.add_articulo', raise_exception=True)
def createNewArticulo(request):

    if 'confirmar' in request.POST:
        articulo = ArticuloForm(request.POST, usuario = request.user)

        if articulo.is_valid():
            articulo.save()
            return redirect('productos:listado_articulos')
        else:
            for k,v in articulo.errors.items():
                messages.add_message(request, messages.ERROR, v)

            return redirect('productos:listado_articulos')
    else:
        return redirect('productos:listado_articulos')

@method_decorator(permission_required('productos.view_articulo', raise_exception=True), name='dispatch')
class ArticulosListView(ListView):
    paginate_by = 15
    model = Articulo
    template_name = 'articulos/listado_articulos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Crear url con filtros para mantener el paginador
        base_url = self.request.build_absolute_uri('/productos/articulos/listado?')
        url = getRoute(self, base_url)

        context["title"] = 'Listado de artículos'
        context["active"] = True
        context["url"] = url
        context["segment"] = 'articulos listado-articulos'
        context["articuloForm"] = ArticuloForm(usuario = self.request.user)
        #context["filter_form"] = FilterForm()
        return context

    def get_queryset(self):

        queryset = Articulo.objects.all().order_by('categoria')

        if 'search' in self.request.GET:
            try:
                queryset = Articulo.objects.filter(titulo = self.request.GET.get('search')).order_by('categoria')

            except Exception as e:
                queryset = Articulo.objects.none()

            return queryset

        if 'filter' in self.request.GET:

            filters = self.request.GET.copy()
            del filters['filter']

            if 'page' in self.request.GET:
                del filters['page']

            queryset = self.getFilters(**filters)

            return queryset

        return queryset

## Marcas ##
@permission_required('productos.add_marca', raise_exception=True)
def createNewMarca(request):

    if 'confirmar' in request.POST:
        marca = MarcaForm(request.POST, usuario = request.user)

        if marca.is_valid():
            marca.save()
            return redirect('productos:listado_marcas')
        else:
            for k,v in marca.errors.items():
                messages.add_message(request, messages.ERROR, v)
            return redirect('productos:listado_marcas')
    else:
        return redirect('productos:listado_marcas')

@method_decorator(permission_required('productos.view_marca', raise_exception=True), name='dispatch')
class MarcasListView(ListView):
    paginate_by = 15
    model = Marca
    template_name = 'articulos/listado_marcas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Crear url con filtros para mantener el paginador
        base_url = self.request.build_absolute_uri('/productos/marcas/listado?')
        url = getRoute(self, base_url)

        context["title"] = 'Listado de marcas'
        context["active"] = True
        context["url"] = url
        context["segment"] = 'articulos listado-marcas'
        context["marcaForm"] = MarcaForm(usuario = self.request.user)
        return context

    def get_queryset(self):

        queryset = Marca.objects.all()
        if 'search' in self.request.GET:
            try:
                queryset = Marca.objects.filter(titulo = self.request.GET.get('search'))
            except Exception as e:
                queryset = Marca.objects.none()
            return queryset

        return queryset

## Categorias ##
@permission_required('productos.add_categoria', raise_exception=True)
def createNewCategoria(request):

    if 'confirmar' in request.POST:
        categoria = CategoriaForm(request.POST, usuario = request.user)

        if categoria.is_valid():
            categoria.save()

            return redirect('productos:listado_categorias')
        else:
            for k,v in categoria.errors.items():
                messages.add_message(request, messages.ERROR, v)
            return redirect('productos:listado_categorias')
    else:
        return redirect('productos:listado_categorias')

@method_decorator(permission_required('productos.view_categoria', raise_exception=True), name='dispatch')
class CategoriasListView(ListView):
    paginate_by = 15
    model = Categoria
    template_name = 'articulos/listado_categorias.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Crear url con filtros para mantener el paginador
        base_url = self.request.build_absolute_uri('/productos/categorias/listado?')
        url = getRoute(self, base_url)

        context["title"] = 'Listado de categorías'
        context["active"] = True
        context["url"] = url
        context["segment"] = 'articulos listado-categorias'
        context["categoriaForm"] = CategoriaForm(usuario = self.request.user)
        return context

    def get_queryset(self):

        queryset = Categoria.objects.all()
        if 'search' in self.request.GET:
            try:
                queryset = Categoria.objects.filter(titulo = self.request.GET.get('search'))
            except Exception as e:
                queryset = Categoria.objects.none()
            return queryset

        return queryset

## Subategorias ##
@permission_required('productos.add_subcategoria', raise_exception=True)
def createNewSubcategoria(request):

    if 'confirmar' in request.POST:
        subcategoria = SubcategoriaForm(request.POST, usuario = request.user)

        if subcategoria.is_valid():
            subcategoria.save()
            return redirect('productos:listado_subcategorias')
        else:
            for k,v in subcategoria.errors.items():
                messages.add_message(request, messages.ERROR, v)
            return redirect('productos:listado_subcategorias')
    else:
        return redirect('productos:listado_subcategorias')

@method_decorator(permission_required('productos.view_subcategoria', raise_exception=True), name='dispatch')
class SubcategoriasListView(ListView):
    paginate_by = 15
    model = Subcategoria
    template_name = 'articulos/listado_subcategorias.html'
    ordering = ['categoria']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Crear url con filtros para mantener el paginador
        base_url = self.request.build_absolute_uri('/productos/subcategorias/listado?')
        url = getRoute(self, base_url)

        context["title"] = 'Listado de subcategorías'
        context["active"] = True
        context["url"] = url
        context["segment"] = 'articulos listado-subcategorias'
        context["subcategoriaForm"] = SubcategoriaForm(usuario = self.request.user)
        return context

    def get_queryset(self):

        queryset = Subcategoria.objects.all().order_by('categoria')
        if 'search' in self.request.GET:
            try:
                queryset = Subcategoria.objects.filter(titulo = self.request.GET.get('search'))
            except Exception as e:
                queryset = Subcategoria.objects.none()
            return queryset

        return queryset

## Funciones cambio de estado
@csrf_exempt
def articuloChangeState(request):
    articulo = Articulo.objects.get(id = request.POST['id'])
    return setStatus(articulo)

@csrf_exempt
def marcaChangeState(request):
    marca = Marca.objects.get(id = request.POST['id'])
    return setStatus(marca)

@csrf_exempt
def categoriaChangeState(request):
    categoria = Categoria.objects.get(id = request.POST['id'])
    return setStatus(categoria)

@csrf_exempt
def subcategoriaChangeState(request):
    subcategoria = Subcategoria.objects.get(id = request.POST['id'])
    return setStatus(subcategoria)

