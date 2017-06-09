from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Dataset, Visualisation

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
class UploadForm(ModelForm):
    class Meta:
        model = Dataset
        fields = ['name','data','sep']
        SEP_CHOICES = [
            ("t","Tab (pasted from Excel)"),
            (",","Comma"),
            ("|","Pipe"),
        ]
        widgets = {
            'sep':forms.RadioSelect(choices=SEP_CHOICES)
        }
        
class VisForm(ModelForm):

    def __init__(self, *args, **kwargs):
        schema = kwargs.pop('schema')
        variables = kwargs.pop('variables')
        super(VisForm, self).__init__(*args, **kwargs)
        for key in schema['properties']:
            field = schema['properties'][key]
            fieldName = key
            fieldType = field['type']
            if fieldType=="string":
                self.fields[fieldName] = forms.CharField()
                self.fields[fieldName].strip = False
            if fieldType=="integer":
                self.fields[fieldName] = forms.IntegerField()
            if fieldType=="float":
                self.fields[fieldName] = forms.FloatField()
            if fieldType=="select":
                fieldChoices = field['choices']
                self.fields[fieldName] = forms.ChoiceField(
                    widget = forms.Select()
                    ,choices=[(var[0], var[1]) for var in fieldChoices]
                )
            if fieldType=="radio":
                fieldChoices = field['choices']
                self.fields[fieldName] = forms.ChoiceField(
                    widget = forms.RadioSelect()
                    ,choices=[(var[0], var[1]) for var in fieldChoices]
                )
            if fieldType=="indicator":
                self.fields[fieldName] = forms.ChoiceField(
                    widget = forms.Select()
                    ,choices=[(var, var) for var in variables]
                )
            if fieldType=="boolean":
                self.fields[fieldName] = forms.BooleanField()
            try:
                fieldRequired = field['required']
            except KeyError:
                fieldRequired = True
            self.fields[fieldName].required = fieldRequired
            try:
                fieldInitial = field['default']
                self.fields[fieldName].initial = fieldInitial
            except KeyError:
                pass
            self.Meta.fields.append(fieldName)
        self.fields['dataset'].required = False
        
    class Meta:
        model = Visualisation
        fields = ['dataset',]
        widgets = {
            'dataset':forms.HiddenInput()
        }
        