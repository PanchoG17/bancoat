from django.http import JsonResponse
from apps.inventario.models import DetallePrestamo

from apps.productos.models import Producto

def setStatus(obj):
    if obj.activo:
        obj.activo = False
    else:
        obj.activo = True
    obj.save()
    return JsonResponse({'status': obj.activo})

def getRoute(self, base_url):

    url = base_url
    if 'filter' in self.request.GET:
        query_params = self.request.get_full_path().split('?')[1]
        url = self.request.build_absolute_uri(base_url+query_params+'&')
        if 'page' in self.request.GET:
            params = query_params.split('&')
            del params[-1]
            query_params = '&'.join(str(p) for p in params)
            url = self.request.build_absolute_uri(base_url+query_params+'&')
    return url

def getFilters(self):

    final_filters = {}

    filters = self.request.GET.copy()
    del filters['filter']

    if 'page' in self.request.GET:
        del filters['page']

    # Iterar filters para armar diccionario de filtros
    for k,v in dict(filters).items():

        if k == 'estado' or k == 'situacion':
            final_filters['{}__in'.format(k)] = v
        elif k == 'valor-range' or k == 'modelo-range':
            final_filters['{}__gte'.format(k.split('-')[0])] = v[0].split(',')[0]
            final_filters['{}__lte'.format(k.split('-')[0])] = v[0].split(',')[1]
        else:
            final_filters['{}_id__in'.format(k)] = v

    return final_filters

def getNroSerie(request, articulo):
    try:
        nro_serie = Producto.objects.filter(articulo = articulo).last().numero_serie
    except:
        nro_serie = None
    return JsonResponse({'nro_serie':nro_serie})

def getPrestamo(request, producto, sucursal):
    try:
        prestamo = DetallePrestamo.objects.filter(producto = producto, comprobante__sucursal = sucursal).last()
    except:
        prestamo = None

    fecha = None if prestamo.fecha_devolucion is None else prestamo.fecha_devolucion
    electro = prestamo.electro.pk if prestamo.electro else None
    beneficiario = prestamo.beneficiario.pk if prestamo.beneficiario else None

    return JsonResponse({'beneficiario':beneficiario,'electro':electro,'fecha':fecha})