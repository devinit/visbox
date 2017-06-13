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
    
    def unpackSchema(self,field,variables):
        fieldKey = field["key"]
        fieldName = field["name"]
        if "description" in field:
            fieldHelp = field["description"]
        else:
            fieldHelp = None
            
        if "options" in field:
            fieldType = "select"
            fieldChoices = field["options"]
        elif "properties" in field:
            fieldType = "header"
        elif "type" not in field:
            fieldType = "hidden"
            
        if "type" in field:
            fieldType = field["type"]
            
        if fieldType=="header":
            self.fields[fieldKey] = forms.CharField(
                widget=forms.TextInput(attrs={"style": "display:none;"})
            )
        if fieldType=="hidden":
            self.fields[fieldKey] = forms.CharField(
                widget=forms.HiddenInput()
                ,initial = field["value"]
            )
        if fieldType=="string":
            self.fields[fieldKey] = forms.CharField()
            self.fields[fieldKey].strip = False
        if fieldType=="Array.<string>":
            self.fields[fieldKey] = forms.CharField()
        if fieldType=="number":
            self.fields[fieldKey] = forms.FloatField()
        if fieldType=="select":
            self.fields[fieldKey] = forms.ChoiceField(
                widget = forms.Select()
                ,choices=[(var, var) for var in fieldChoices]
            )
        # if fieldType=="radio":
        #     self.fields[fieldKey] = forms.ChoiceField(
        #         widget = forms.RadioSelect()
        #         ,choices=[(var, var) for var in fieldChoices]
        #     )
        # if fieldType=="indicator":
        #     self.fields[fieldKey] = forms.ChoiceField(
        #         widget = forms.Select()
        #         ,choices=[(var, var) for var in variables]
        #     )
        if fieldType=="indicator":
            self.fields[fieldKey] = forms.ChoiceField(
                widget = forms.Select()
                ,choices=[(var, var) for var in ["None"]+variables]
            )
        if fieldType=="boolean":
            self.fields[fieldKey] = forms.BooleanField()
            
        #Nothing required for now
        self.fields[fieldKey].required = False
        
        # self.fields[fieldKey].help_text = fieldHelp
        self.fields[fieldKey].label = fieldHelp
        if "default" in field:
            self.fields[fieldKey].initial = field["default"]

        self.Meta.fields.append(fieldKey)
        
        if "properties" in field:
            for subfield in field["properties"]:
                unpackSchema = self.unpackSchema
                unpackSchema(subfield,variables)

    def __init__(self, *args, **kwargs):
        schema = kwargs.pop('schema')
        variables = kwargs.pop('variables')
        super(VisForm, self).__init__(*args, **kwargs)
        unpackSchema = self.unpackSchema
        for field in schema['properties']:
            unpackSchema(field,variables)
        
    class Meta:
        model = Visualisation
        fields = ['save_as_template',]
        