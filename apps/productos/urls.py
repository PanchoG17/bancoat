from . import views
from django.urls import path
from apps.productos.views import *
from apps.helpers import getNroSerie, getPrestamo

app_name = 'productos'

urlpatterns = [

    # Productos
    path( 'listado', productosListView.as_view(), name = 'listado_productos'),
    path( 'otorgados', otorgadosListView.as_view(), name = 'listado_otorgados'),
    path( 'baja', bajaProducto, name = 'baja_producto'),

    path( 'nro_serie/<int:articulo>', getNroSerie, name = 'nro_serie'),
    path( 'prestamo/<int:producto>/<int:sucursal>', getPrestamo, name = 'prestamo'),

    # Articulos
    path( 'articulos/crear', createNewArticulo, name = 'crear_articulo'),
    path( 'articulos/listado', ArticulosListView.as_view(), name = 'listado_articulos'),
    path( 'articulos/c_status', articuloChangeState, name = 'change_articulo'),

    # Marcas
    path( 'marcas/crear', createNewMarca, name = 'crear_marca'),
    path( 'marcas/listado', MarcasListView.as_view(), name = 'listado_marcas'),
    path( 'marcas/c_status', marcaChangeState, name = 'change_marca'),

    # Categorias
    path( 'categorias/crear', createNewCategoria, name = 'crear_categoria'),
    path( 'categorias/listado', CategoriasListView.as_view(), name = 'listado_categorias'),
    path( 'categorias/c_status', categoriaChangeState, name = 'change_categoria'),

    #Subcategorias
    path( 'subcategorias/crear', createNewSubcategoria, name = 'crear_subcategoria'),
    path( 'subcategorias/listado', SubcategoriasListView.as_view(), name = 'listado_subcategorias'),
    path( 'subcategorias/c_status', subcategoriaChangeState, name = 'change_subcategoria'),


]