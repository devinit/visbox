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
        exclude = ['creator','dataset']
        
class ColumnForm(ModelForm):
    class Meta:
        model = Visualisation
        fields = ('title','dataset','width','height','padding_top','padding_right','padding_bottom','padding_left',
                  'x_indicator','y_indicator','sort','y_maximum','y_maximum_value','filter_by','filter_selection','colour','x_label'
                  ,'y_label','x_text_rotation','labels_on_chart','label_font_size','label_format','save_as_template')
        SORT_CHOICES = [('yasc','Y ascending'),('ydes','Y descending'),('xasc','X ascending'),('xdes','X descending')]
        Y_AUTO_CHOICES = [('auto','Automatic'),('manual','Manual (define below)')]
        widgets = {
            'dataset':forms.HiddenInput(),
            'sort':forms.RadioSelect(choices=SORT_CHOICES),
            'y_maximum':forms.RadioSelect(choices=Y_AUTO_CHOICES),
            'filter_selection':forms.Select(),
        }
    def __init__(self, *args, **kwargs):
        x = kwargs.pop('x')
        y = kwargs.pop('y')
        super(ColumnForm, self).__init__(*args, **kwargs)
        self.fields['x_indicator'].widget = forms.Select(
            choices=[(var, var) for var in x+y]
        )
        self.fields['y_indicator'].widget = forms.Select(
            choices=[(var, var) for var in y+x]
        )
        self.fields['filter_by'].widget = forms.Select(
            choices=[(var,var) for var in ['None']+x+y]
        )
        self.fields['dataset'].required = False
        
class BarForm(ModelForm):
    class Meta:
        model = Visualisation
        fields = ('title','dataset','width','height','padding_top','padding_right','padding_bottom','padding_left',
                  'x_indicator','y_indicator','sort','x_maximum','x_maximum_value','filter_by','filter_selection','colour','x_label'
                  ,'y_label','x_text_rotation','labels_on_chart','label_font_size','label_format','save_as_template')
        SORT_CHOICES = [('yasc','Y ascending'),('ydes','Y descending'),('xasc','X ascending'),('xdes','X descending')]
        X_AUTO_CHOICES = [('auto','Automatic'),('manual','Manual (define below)')]
        widgets = {
            'dataset':forms.HiddenInput(),
            'sort':forms.RadioSelect(choices=SORT_CHOICES),
            'x_maximum':forms.RadioSelect(choices=X_AUTO_CHOICES),
            'filter_selection':forms.Select(),
        }
    def __init__(self, *args, **kwargs):
        x = kwargs.pop('x')
        y = kwargs.pop('y')
        super(BarForm, self).__init__(*args, **kwargs)
        self.fields['x_indicator'].widget = forms.Select(
            choices=[(var, var) for var in x+y]
        )
        self.fields['y_indicator'].widget = forms.Select(
            choices=[(var, var) for var in y+x]
        )
        self.fields['filter_by'].widget = forms.Select(
            choices=[(var,var) for var in ['None']+x+y]
        )
        self.fields['dataset'].required = False
        
class StackedColumnForm(ModelForm):
    class Meta:
        model = Visualisation
        fields = ('title','dataset','width','height','padding_top','padding_right','padding_bottom','padding_left',
                  'x_indicator','y_indicator','group_by','sort','y_maximum','y_maximum_value','unit_divisor','filter_by','filter_selection','colour','x_label'
                  ,'y_label','y_axis_ticks','x_text_rotation','labels_on_chart','label_font_size','label_format','legend_position','save_as_template')
        SORT_CHOICES = [('yasc','Y ascending'),('ydes','Y descending'),('xasc','X ascending'),('xdes','X descending')]
        Y_AUTO_CHOICES = [('auto','Automatic'),('manual','Manual (define below)')]
        LEGEND_POS_CHOICES = [('tr','Top right'),('tl','Top left')]
        widgets = {
            'dataset':forms.HiddenInput(),
            'sort':forms.RadioSelect(choices=SORT_CHOICES),
            'y_maximum':forms.RadioSelect(choices=Y_AUTO_CHOICES),
            'filter_selection':forms.Select(),
            'legend_position':forms.RadioSelect(choices=LEGEND_POS_CHOICES),
        }
    def __init__(self, *args, **kwargs):
        x = kwargs.pop('x')
        y = kwargs.pop('y')
        super(StackedColumnForm, self).__init__(*args, **kwargs)
        self.fields['x_indicator'].widget = forms.Select(
            choices=[(var, var) for var in x+y]
        )
        self.fields['y_indicator'].widget = forms.Select(
            choices=[(var, var) for var in y+x]
        )
        self.fields['group_by'].widget = forms.Select(
            choices=[(var, var) for var in x+y]
        )
        self.fields['filter_by'].widget = forms.Select(
            choices=[(var,var) for var in ['None']+x+y]
        )
        self.fields['dataset'].required = False
        self.fields['x_label'].strip = False
        
class DonutForm(ModelForm):
    class Meta:
        model = Visualisation
        fields = ('title','dataset','width','height','padding_top','padding_right','padding_bottom','padding_left',
                  'x_indicator','y_indicator','sort','filter_by','filter_selection','colour','label_font_size','label_format','save_as_template')
        SORT_CHOICES = [('native','Native ordering'),('avoid','Avoid text collisions'),('yasc','Y ascending'),('ydes','Y descending'),('xasc','X ascending'),('xdes','X descending')]
        widgets = {
            'dataset':forms.HiddenInput(),
            'sort':forms.RadioSelect(choices=SORT_CHOICES),
            'filter_selection':forms.Select(),
        }
    def __init__(self, *args, **kwargs):
        x = kwargs.pop('x')
        y = kwargs.pop('y')
        super(DonutForm, self).__init__(*args, **kwargs)
        self.fields['x_indicator'].widget = forms.Select(
            choices=[(var, var) for var in x+y]
        )
        self.fields['y_indicator'].widget = forms.Select(
            choices=[(var, var) for var in y+x]
        )
        self.fields['filter_by'].widget = forms.Select(
            choices=[(var,var) for var in ['None']+x+y]
        )
        self.fields['dataset'].required = False
        