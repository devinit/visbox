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
    class Meta:
        model = Visualisation
        fields = ['dataset']

    def __init__(self, *args, **kwargs):
        schema = kwargs.pop('schema')
        variables = kwargs.pop('variables')
        super(VisForm, self).__init__(*args, **kwargs)
        fields = []
        choiceDict = {}
        for vis in schema:
            for field in vis['properties']:
                fieldName = field['name']
                fieldType = field['type']
                if fieldType=="string":
                    self.fields[fieldName] = forms.CharField(fieldName)
                    self.fields[fieldName].strip = False
                if fieldType=="integer":
                    self.fields[fieldName] = forms.FloatField(fieldName)
                if fieldType=="float":
                    self.fields[fieldName] = forms.IntegerField(fieldName)
                if fieldType=="select":
                    fieldChoices = field['choices']
                    self.fields[fieldName] = forms.Select(
                        fieldName
                        ,choices=[(var, var) for var in fieldChoices]
                    )
                if fieldType=="radio":
                    fieldChoices = field['choices']
                    self.fields[fieldName] = forms.RadioSelect(
                        fieldName
                        ,choices=[(var, var) for var in fieldChoices]
                    )
                if fieldType=="indicator":
                    self.fields[fieldName] = forms.Select(
                        fieldName
                        ,choices=[(var, var) for var in variables]
                    )
                self.Meta.fields.append(fieldName)
        self.fields['dataset'].required = False
        