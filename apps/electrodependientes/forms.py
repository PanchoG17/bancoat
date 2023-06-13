from django import forms
from django.db.models import Q
from django.forms.models import inlineformset_factory

# IMPORT MODELS
from django.contrib.auth.models import User
from apps.persona.models import Persona
from apps.clasificadores.models import Empresa, TipoParentesco
from apps.electrodependientes.models import Electrodependiente,DocumentacionElectro, TitularDeSuministro, Medico, Diagnostico

class ElectroForm(forms.ModelForm):
    error_css_class = 'is-invalid'
    required_css_class = 'required-field'

    class Meta:
        model = Electrodependiente
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        usuario = kwargs.pop('usuario', None)

        super().__init__(*args, **kwargs)

        for field in self.fields:

            if 'expediente' in str(field):
                self.fields[str(field)].widget.attrs.update({'class':'form-control pe-5'})
            else:
                self.fields[str(field)].widget.attrs['required'] = 'required'
                self.fields[str(field)].widget.attrs.update({'class':'form-select pe-5'})
            
        # Filtrar personas ya registradas como electrodependientes
        electros = Electrodependiente.objects.all().values('persona_electrodependiente__id')

        self.fields['persona_electrodependiente'].queryset = Persona.objects.exclude(Q(id__in = electros) | Q(activo = False)  )
        self.fields['usuario_creador'].widget = forms.HiddenInput()
        self.fields['usuario_creador'].initial = usuario.id
        self.fields['fecha_vencimiento_cud'].widget = forms.widgets.DateInput(attrs={'type': 'date','class':'form-control form-color'})
        self.fields['fecha_vencimiento_cud'].widget.attrs.update({'disabled':'disabled'})

class DocumentacionForm(forms.ModelForm):
    
    class Meta:
        model = DocumentacionElectro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['formulario'].widget.attrs.update({'class':'form-control pe-5'})
        self.fields['documentacion'].widget = forms.FileInput(attrs={'multiple':True, 'class': 'form-control'})

class TitularSuministroForm(forms.ModelForm):
    error_css_class = 'is-invalid'
    required_css_class = 'required-field'

    class Meta:
        model = TitularDeSuministro
        fields = '__all__'
        widgets = {
            'titularServicio': forms.Select({'class':'form-select'}),
            'vinculo': forms.Select({'class':'form-select'}),
            'proveedor_suministro': forms.Select({'class':'form-select'}),
            'numero_cliente': forms.TextInput({'class':'form-control'})
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

        # Filtrar por empresas de servicios
        self.fields['proveedor_suministro'].queryset = Empresa.objects.filter(tipo_servicio = 'ELE')
        self.fields['titularServicio'].queryset = Persona.objects.filter(activo = True)
        self.fields['usuario_creador'].widget = forms.HiddenInput()
        self.fields['usuario_creador'].initial = usuario.id

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'required':True})

class DiagnosticoForm(forms.ModelForm):
    error_css_class = 'is-invalid'
    required_css_class = 'required-field'

    class Meta:
        model = Diagnostico
        fields = '__all__'
        widgets = {
            'medico' : forms.Select({'class' : 'form-select','required':True}),
            'equipo_dialisis' : forms.Select({'class' : 'form-select'}),
            'equipo_alimentacion' : forms.Select({'class' : 'form-select'}),
            'tiempo_requerido' : forms.Select({'class' : 'form-select','required':True}),

            'historia_clinica' : forms.Textarea(attrs={'rows':3 , 'cols': 115, 'class' : 'form-control','required':True}),
            'diagnostico' : forms.Textarea(attrs={'rows':3 , 'cols': 115, 'class' : 'form-control','required':True}),
            'equipo_ventilacion' : forms.Textarea(attrs={'rows':2 , 'cols': 115, 'class' : 'form-control'}),
            'otro' : forms.Textarea(attrs={'rows':2 , 'cols': 115, 'class' : 'form-control'}),
            'fecha_diagnostico': forms.widgets.DateInput(attrs={'type': 'date','class':'form-control form-color'})
        }

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        usuario = kwargs.pop('usuario', None)

        super().__init__(*args, **kwargs)

        self.fields['usuario_creador'].widget = forms.HiddenInput()
        self.fields['usuario_creador'].initial = usuario.id

        for field in self.fields:

            self.fields[str(field)].widget.attrs.update({'class':'form-control pe-5'})

TitularSuministroFormSet = inlineformset_factory(Electrodependiente, TitularDeSuministro, TitularSuministroForm, extra=1, fields='__all__', can_delete=False)
DiagnosticoFormSet = inlineformset_factory(Electrodependiente, Diagnostico, DiagnosticoForm, extra=1, fields='__all__', can_delete=False)
