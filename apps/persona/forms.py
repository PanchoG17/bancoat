from django import forms
from django.forms.models import inlineformset_factory
from django.db.models import Q

# IMPORT MODELS
from apps.persona.models import Persona, Beneficiario, DocumentacionBeneficiario
from apps.electrodependientes.models import Electrodependiente

class PersonaForm(forms.ModelForm):
    error_css_class = 'is-invalid'
    required_css_class = 'required-field'

    class Meta:
        model = Persona
        fields = '__all__'
        error_messages = {
            'documento': {
                'unique': ("Documento ya registrado."),
            },
            'cuit': {
                'unique': ("CUIT/CUIL ya registrado."),
            },
        }

    def __init__(self, *args, **kwargs):

        usuario = kwargs.pop('usuario', None)

        super().__init__(*args, **kwargs)

        self.fields['usuario_creador'].widget = forms.HiddenInput()
        self.fields['usuario_creador'].initial = usuario.id

        for field in self.fields:

            self.fields[str(field)].widget.attrs.update({'class':'form-control pe-5'})

            if 'fecha' in str(field):
                self.fields[str(field)].widget = forms.widgets.DateInput(attrs={'type': 'date','class':'form-control form-color'})

class PersonaEditForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        error_messages = {
            'documento': {
                'unique': ("Documento ya registrado."),
            },
            'cuit': {
                'unique': ("CUIT/CUIL ya registrado."),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['usuario_creador'].widget = forms.HiddenInput()

        for field in self.fields:

            self.fields[str(field)].widget.attrs.update({'class':'form-control pe-5'})
            self.fields[str(field)].widget.attrs.update({'disabled':True})

            if 'fecha' in str(field):
                self.fields[str(field)].widget = forms.widgets.DateInput(attrs={'type': 'date','class':'form-control form-color'}, format='%Y-%m-%d')
                self.fields[str(field)].widget.attrs.update({'disabled':True})


class BeneficiarioForm(forms.ModelForm):

    error_css_class = 'is-invalid'
    required_css_class = 'required-field'

    class Meta:
        model = Beneficiario
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        usuario = kwargs.pop('usuario', None)

        super().__init__(*args, **kwargs)

        # Filtrar personas ya registradas como beneficiario o electrodependiente
        beneficiarios = Beneficiario.objects.all().values('persona_beneficiaria__id')
        responsables = Beneficiario.objects.all().values('persona_responsable__id')
        electros = Electrodependiente.objects.all().values('persona_electrodependiente__id')

        self.fields['persona_beneficiaria'].queryset = Persona.objects.exclude(Q(id__in = beneficiarios) | Q(id__in = responsables) | Q(activo = False))
        self.fields['persona_responsable'].queryset = Persona.objects.exclude(Q(id__in = beneficiarios)| Q(id__in = electros) | Q(activo = False))

        self.fields['usuario_creador'].widget = forms.HiddenInput()
        self.fields['usuario_creador'].initial = usuario.id

        self.fields['obra_social'].empty_label = 'Ninguna'
        self.fields['archivo_cud'].widget.attrs.update({'disabled':'disabled'})
        self.fields['nro_afiliado'].widget.attrs.update({'disabled':'disabled'})

        for field in self.fields:

            self.fields[str(field)].widget.attrs.update({'class':'form-control pe-5'})

            if 'fecha' in str(field):
                self.fields[str(field)].widget = forms.widgets.DateInput(attrs={'type': 'date','class':'form-control form-color'})
                self.fields[str(field)].widget.attrs.update({'disabled':'disabled'})

class DocumentacionForm(forms.ModelForm):

    class Meta:
        model = DocumentacionBeneficiario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:

            self.fields[str(field)].widget.attrs['required'] = 'required'
            self.fields[str(field)].widget.attrs.update({'class':'form-control'})

            if 'fecha' in str(field):
                self.fields[str(field)].widget = forms.widgets.DateInput(attrs={'type': 'date','class':'form-control'})
                self.fields[str(field)].widget.attrs.update({'disabled':'disabled'})

DocumentacionFormset = inlineformset_factory(Beneficiario, DocumentacionBeneficiario, DocumentacionForm, extra=0, fields='__all__', can_delete=False)