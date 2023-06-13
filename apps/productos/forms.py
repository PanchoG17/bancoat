from django import forms

from apps.productos.models import Producto, Articulo, Marca, Categoria, Subcategoria
from apps.inventario.models import Sucursal
from apps.localizacion.models import Pais

class ArticuloForm(forms.ModelForm):

    class Meta:
        model = Articulo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

        self.fields['usuario_creador'].widget = forms.HiddenInput()
        self.fields['usuario_creador'].initial = usuario.id

        for field in self.fields:

            self.fields[str(field)].widget.attrs['required'] = 'required'
            self.fields[str(field)].widget.attrs.update({'class':'form-control'})

class MarcaForm(forms.ModelForm):

    class Meta:
        model = Marca
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

        self.fields['usuario_creador'].widget = forms.HiddenInput()
        self.fields['usuario_creador'].initial = usuario.id

        for field in self.fields:

            self.fields[str(field)].widget.attrs['required'] = 'required'
            self.fields[str(field)].widget.attrs.update({'class':'form-control'})

class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

        self.fields['usuario_creador'].widget = forms.HiddenInput()
        self.fields['usuario_creador'].initial = usuario.id

        for field in self.fields:

            self.fields[str(field)].widget.attrs['required'] = 'required'
            self.fields[str(field)].widget.attrs.update({'class':'form-control'})

class SubcategoriaForm(forms.ModelForm):

    class Meta:
        model = Subcategoria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

        self.fields['usuario_creador'].widget = forms.HiddenInput()
        self.fields['usuario_creador'].initial = usuario.id

        for field in self.fields:

            self.fields[str(field)].widget.attrs['required'] = 'required'
            self.fields[str(field)].widget.attrs.update({'class':'form-control'})