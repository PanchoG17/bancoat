from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.db.models import Count, Value, F
from django.db.models import IntegerField, Sum, Case, When

from datetime import date

# Import models
from apps.electrodependientes.models import Electrodependiente, Diagnostico
from apps.persona.models import Beneficiario
from apps.productos.models import Producto
from apps.inventario.models import DetallePrestamo

@login_required(login_url="/login/")
def index(request):

    if request.user.has_perm('persona.view_persona'):
        ## Registrados
        electros = Electrodependiente.objects.filter(activo = True).count()
        beneficiarios = Beneficiario.objects.filter(activo = True).count()

        ## Porcentaje disponibilidad
        disponibles = Producto.objects.values('articulo__titulo').order_by('articulo__titulo').exclude(situacion = 'NO_DISP').annotate(count=Count('articulo__titulo'), disponibles = Sum(Case(When(situacion = 'DISP', then = 1),default=0,output_field=IntegerField())))

        for d in disponibles:
            percentaje = (d['disponibles'] * 100) / d['count']
            d['percentaje'] = int(percentaje)

        ## Productos / Electros - fechas de devolución - annotate para incluir campo 'restante' al queryset
        productos_otorgados = DetallePrestamo.objects.filter(regresado = False, baja = False).annotate(restante = F('fecha_devolucion') - Value(date.today())).order_by('restante')[:10]
        electros_vigentes = Diagnostico.objects.filter(activo = True, electrodependiente__activo = True ).annotate(restante = F('fecha_finalizacion') - Value(date.today())).order_by('restante')[:10]

        context = { 'segment': 'inicio','active': True,'electros':electros,'beneficiarios':beneficiarios,'disponibles':disponibles, 'otorgados':productos_otorgados, 'diagnosticos': electros_vigentes }
        html_template = loader.get_template('home/dashboard.html')
    else:
        context = { 'segment': 'inicio','active': False }
        html_template = loader.get_template('home/blank.html')
    return HttpResponse(html_template.render(context, request))


""""
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        return redirect('home')

    except:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
"""