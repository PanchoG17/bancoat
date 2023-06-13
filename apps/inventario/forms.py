from django import forms
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError

from apps.inventario.models import Comprobante, DetalleEntrada, DetallePrestamo, DetalleDevolucion, DetalleRenovacion
from apps.electrodependientes.models import Electrodependiente
from apps.persona.models import Beneficiario
from apps.productos.models import Producto, Articulo
from apps.clasificadores.models import Empresa

class ComprobanteForm(forms.ModelForm):
    error_css_class = 'is-invalid'
    required_css_class = 'required-field'

    class Meta:
        model = Comprobante
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)

        super().__init__(*args, **kwargs)

        self.fields['usuario_creador'].widget = forms.HiddenInput()
        self.fields['usuario_creador'].initial = usuario.id

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class':'form-control'})

            if str(field) == 'proveedor':
                self.fields[str(field)].queryset = Empresa.objects.filter(tipo_servicio='PRV')

            if str(field) == 'fecha_operacion':
                self.fields[str(field)].widget = forms.widgets.DateInput(attrs={'type': 'date','class':'form-control','required':'required'})

            if str(field) == 'tipo_comprobante':
                self.fields[str(field)].widget.attrs.update({'disabled':'disabled'})

class DetalleEntradaForm(forms.ModelForm):
    error_css_class = 'is-invalid'
    required_css_class = 'required-field'

    class Meta:
        model = DetalleEntrada
        fields = '__all__'
        error_messages = {
            'numero_serie': {
                'unique': ("N° de serie ya existe"),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Excluir articulos que no estan activos
        self.fields['articulo'].queryset = Articulo.objects.exclude(activo = False)

        for field in self.fields:

            self.fields[str(field)].widget.attrs['required'] = 'required'
            self.fields[str(field)].widget.attrs.update({'class':'form-control'})

class DetallePrestamoForm(forms.ModelForm):
    error_css_class = 'is-invalid'
    required_css_class = 'required-field'

    class Meta:
        model = DetallePrestamo
        fields = '__all__'

    def __init__(self,*args,**kwargs):

        #Obtengo la sucursal y si corresponde a prestamo electro desde la vista para filtrar los productos
        sucursal = kwargs.pop('sucursal', None)
        electro = kwargs.pop('electro', None)

        super(DetallePrestamoForm, self).__init__(*args, **kwargs)

        # Los productos se filtran si corresponde a prestamo electro o no
        self.fields['producto'].queryset = Producto.objects.filter(sucursal=sucursal, situacion='DISP', articulo__electrodependientes=electro)
        self.fields['beneficiario'].queryset = Beneficiario.objects.filter(activo = True)
        self.fields['electro'].queryset = Electrodependiente.objects.filter(activo = True)

        self.fields.pop('beneficiario') if electro else self.fields.pop('electro')

        for field in self.fields:

            self.fields[str(field)].widget.attrs['required'] = 'required'
            self.fields[str(field)].widget.attrs.update({'class':'form-control'})

            if 'fecha' in str(field):
                self.fields[str(field)].widget = forms.widgets.DateInput(attrs={'type': 'date','class':'form-control','required':'required'})

class DetalleRenovacionForm(forms.ModelForm):

    class Meta:
        model = DetalleRenovacion
        fields = '__all__'

    def __init__(self, *args,**kwargs):
        super(DetalleRenovacionForm, self).__init__(*args, **kwargs)

        self.fields['producto'].widget.attrs['required'] = 'required'
        self.fields['nuevo_vencimiento'].widget.attrs['required'] = 'required'
        self.fields['nuevo_vencimiento'].widget = forms.widgets.DateInput(attrs={'type': 'date','class':'form-control','required':'required'})

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class':'form-control'})

class DetalleDevolucionForm(forms.ModelForm):
    error_css_class = 'is-invalid'
    required_css_class = 'required-field'

    class Meta:
        model = DetalleDevolucion
        fields = '__all__'

    def __init__(self,*args,**kwargs):

        #Obtengo la sucursal y si corresponde a prestamo electro desde la vista
        sucursal = kwargs.pop('sucursal', None)

        super(DetalleDevolucionForm, self).__init__(*args, **kwargs)

        self.fields['producto'].queryset = Producto.objects.filter(sucursal = sucursal, situacion = 'OTO')

        for field in self.fields:

            self.fields[str(field)].widget.attrs['required'] = 'required'
            self.fields[str(field)].widget.attrs.update({'class':'form-control'})

            if 'fecha' in str(field):
                self.fields[str(field)].widget = forms.widgets.DateInput(attrs={'type': 'date','class':'form-control','required':'required'})

#### Validar que no existan nros de serie duplicados en el mismo comprobante de entrada
class EntradaNroSerieFormset(forms.BaseInlineFormSet):

    def clean(self):
        if any(self.errors):
            return

        numeros = []
        for form in self.forms:
            n = form.cleaned_data.get('numero_serie')

            if n in numeros:
                raise ValidationError('No deben existir números de serie duplicados en el detalle.')

            numeros.append(n)

DetalleEntradaFormSet = inlineformset_factory(Comprobante, DetalleEntrada, DetalleEntradaForm, formset=EntradaNroSerieFormset, extra=1, fields='__all__', can_delete=False,)
DetallePrestamoFormSet = inlineformset_factory(Comprobante, DetallePrestamo, DetallePrestamoForm, extra=1, fields='__all__', can_delete=False)
DetalleDevolucionFormSet = inlineformset_factory(Comprobante, DetalleDevolucion, DetalleDevolucionForm, extra=1, fields='__all__', can_delete=False)
