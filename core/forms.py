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
    
    def diDefaults(self, field):
        fieldDefaults = {}
        
        fieldDefaults["showAxis"] = True
        fieldDefaults["showGridlines"] = True
        fieldDefaults["categoryAxis.innerPadding"] = 0.5
        fieldDefaults["categoryAxis.outerPadding"] = 0.5
        fieldDefaults["config.colors"] = "#e84439,#f8c1b2,#f0826d,#bc2629,#8f1b13"
        
        for key in fieldDefaults:
            if field.endswith(key):
                return fieldDefaults[key]
        
        return None
    
    def sectionField(self,field):
        fieldCategories = {}
        
        fieldCategories["config.linearAxis"] = "Axis options"     
        fieldCategories["config.categoryAxis"] = "Axis options"
        fieldCategories["config.circular"] = "Axis options"
        
        fieldCategories["config.colors"] = "Groups and colours"
        fieldCategories["config.groupBy"] = "Groups and colours"
        
        fieldCategories["sort"] = "Sort, filter, and divide"
        fieldCategories["sort_direction"] = "Sort, filter, and divide"
        fieldCategories["filter_by"] = "Sort, filter, and divide"
        fieldCategories["filter_selection"] = "Sort, filter, and divide"
        fieldCategories["unit_divisor"] = "Sort, filter, and divide"
        
        fieldCategories["config.orientation"] = "Whole chart options"
        
        fieldCategories["width"] = "Sizing"
        fieldCategories["height"] = "Sizing"
        fieldCategories["padding_top"] = "Sizing"
        fieldCategories["padding_bottom"] = "Sizing"
        fieldCategories["padding_left"] = "Sizing"
        fieldCategories["padding_right"] = "Sizing"
        
        fieldCategories["config.title"] = "Chart title"
        fieldCategories["config.titleAlignment"] = "Chart title"
        
        fieldCategories["config.legend."] = "Legend options"
        
        fieldCategories["save_as_template"] = "Visbox options"
        
        for key in fieldCategories:
            if field.startswith(key):
                return fieldCategories[key]
            
        return "Whole chart options"
    
    
    def unpackSchema(self,field,category,linear):
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
                widget=forms.HiddenInput()
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
            self.fields[fieldKey] = forms.FloatField(
                widget=forms.NumberInput(attrs={"step":"0.01"})
            )
        if fieldType=="select":
            self.fields[fieldKey] = forms.ChoiceField(
                widget = forms.Select()
                ,choices=[(var, var) for var in fieldChoices]
            )
        if fieldType=="indicator":
            if fieldKey.startswith("config.linearAxis"):
                variables = linear+category
            elif fieldKey.startswith("config.categoryAxis"):
                variables = category+linear
            elif fieldKey.startswith("config.circular"):
                variables = category+linear
            else:
                variables = ["None"]+category+linear
            self.fields[fieldKey] = forms.ChoiceField(
                widget = forms.Select()
                ,choices=[(var, var) for var in variables]
            )
        if fieldType=="boolean":
            self.fields[fieldKey] = forms.BooleanField()
            
        #Nothing required for now
        self.fields[fieldKey].required = False
        
        # self.fields[fieldKey].help_text = fieldSegment
        self.fields[fieldKey].label = fieldHelp
        if "default" in field:
            self.fields[fieldKey].initial = field["default"]

        self.Meta.fields.append(fieldKey)
        
        if "properties" in field:
            for subfield in field["properties"]:
                unpackSchema = self.unpackSchema
                unpackSchema(subfield,category,linear)

    def __init__(self, *args, **kwargs):
        schema = kwargs.pop('schema')
        category = kwargs.pop('category')
        linear = kwargs.pop('linear')
        super(VisForm, self).__init__(*args, **kwargs)
        unpackSchema = self.unpackSchema
        for field in schema['properties']:
            unpackSchema(field,category,linear)
        self.fields['sort'].widget = forms.Select(
            choices=[(var,var) for var in ['None']+category+linear]
        )
        self.fields['filter_by'].widget = forms.Select(
            choices=[(var,var) for var in ['None']+category+linear]
        )
        sectionField = self.sectionField
        diDefaults = self.diDefaults
        for key in self.fields:
            try:
                self.fields[key].widget.attrs["section"] = sectionField(key)
            except AttributeError:
                self.fields[key].widget.attrs = {"section": sectionField(key)}
            if diDefaults(key) is not None:
                self.fields[key].initial = diDefaults(key)
        
    class Meta:
        model = Visualisation
        fields = ['width','height','padding_top','padding_bottom',
                  'padding_left','padding_right','sort','sort_direction',
                  'filter_by','filter_selection','unit_divisor','save_as_template',]
        SORT_CHOICES = [('asc','Ascending'),('desc','Descending')]
        widgets = {
            'sort_direction':forms.Select(choices=SORT_CHOICES),
            'filter_selection':forms.Select(),
        }
        