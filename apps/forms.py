from django import forms

from apps.productos.models import Articulo, Marca
from apps.inventario.models import Sucursal
from apps.localizacion.models import Pais
from apps.persona.models import Persona
from apps.clasificadores.models import TipoParentesco, TipoBaja, Empresa

class FilterForm(forms.Form):

    SITUACION = (
        ('DISP', 'Disponible'),
        ('OTO', 'Otorgado'),
        ('NO_DISP', 'No disponible')
    )

    ESTADO = (
        ('Nuevo', 'Nuevo'),
        ('Usado', 'Usado'),
        ('Reacondicionado', 'Reacondicionado')
    )

    articulo = forms.ModelChoiceField(label='Articulo', queryset=Articulo.objects.all(),required=False)
    marca = forms.ModelChoiceField(label='Marca', queryset=Marca.objects.all(),required=False)
    origen = forms.ModelChoiceField(label='Origen', queryset=Pais.objects.all(),required=False)
    sucursal = forms.ModelChoiceField(label='Sucursal', queryset=Sucursal.objects.all(),required=False)

    situacion = forms.MultipleChoiceField(required=False)
    estado = forms.MultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[str(field)].widget = forms.SelectMultiple()
            self.fields[str(field)].widget.attrs.update({'class':'chosen-custom'})
            self.fields[str(field)].empty_label = None

        self.fields['articulo'].queryset = Articulo.objects.all()
        self.fields['marca'].queryset = Marca.objects.all()
        self.fields['origen'].queryset = Pais.objects.all()
        self.fields['sucursal'].queryset = Sucursal.objects.all()
        self.fields['situacion'].choices = self.SITUACION
        self.fields['estado'].choices = self.ESTADO

class BajasForm(forms.Form):
    motivo = forms.ModelChoiceField(label='Motivo de la baja', queryset=TipoBaja.objects.all(),required=True)
    descripcion = forms.CharField(max_length = 50, required = True )

    descripcion.widget.attrs.update({'class': 'form-control'})
    motivo.widget.attrs.update({'class': 'form-control'})

class TitularEditForm(forms.Form):
    titular_servicio = forms.ModelChoiceField(label='Nuevo titular del servicio eléctrico', queryset=Persona.objects.filter(activo = True), required=True)
    titular_servicio.widget.attrs.update({'class': 'form-select'})

    proveedor_suministro = forms.ModelChoiceField(label='Compañía proveedora del suministro', queryset=Empresa.objects.filter(tipo_servicio = 'ELE'), required=True)
    proveedor_suministro.widget.attrs.update({'class': 'form-select'})

    vinculo = forms.ModelChoiceField(label='Vinculo con la persona', queryset=TipoParentesco.objects.all(), required=True)
    vinculo.widget.attrs.update({'class': 'form-select'})

    nro_cliente = forms.CharField(max_length = 50, required = True, label='Numero de cliente' )
    nro_cliente.widget.attrs.update({'class': 'form-control'})

class ResponsableEditForm(forms.Form):
    responsable = forms.ModelChoiceField(label='Nuevo responsable', queryset=Persona.objects.filter(activo = True), required=True)
    responsable.widget.attrs.update({'class': 'form-select'})

    vinculo = forms.ModelChoiceField(label='Vinculo con la persona', queryset=TipoParentesco.objects.all(), required=True)
    vinculo.widget.attrs.update({'class': 'form-select'})