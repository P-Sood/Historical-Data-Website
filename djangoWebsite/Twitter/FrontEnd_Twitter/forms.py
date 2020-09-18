from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


    

class Search(forms.Form):
    input_ = forms.CharField(label = 'Input',max_length=100, required=True)
    fromDate = forms.CharField(label = 'fromDate',max_length=10, required=False, widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    toDate = forms.CharField(label = 'toDate',max_length=10, required=False, widget=forms.TextInput(attrs={'placeholder' : 'YYYY-MM-DD'}))
    count = forms.IntegerField(max_value=5,min_value=1,required=False, widget=forms.NumberInput(attrs={ 'size': '50','placeholder': 'numPages to search'  }) )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                " ",
                'input_',
                'fromDate',
                'toDate',
                'count',
            ),
            ButtonHolder(
                Submit('Submit', 'Submit Data', css_class='button white')
            )
        )

class Query(forms.Form):
    searchDB = forms.CharField(label = "Search", max_length=100,required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(

            Fieldset(
                " ",
                "searchDB",
            ),
            ButtonHolder(
                Submit('submit','Query Data',css_class='button white'),
            ),
            
        )
class Login(forms.Form):
    username = forms.CharField(label = 'username' , max_length = 200 , required = True)
    password = forms.CharField(label = 'password' , max_length = 200 , required = True , widget = forms.PasswordInput())

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout (
            Fieldset(
                " ",
                "username",
                "password",

            ),
            ButtonHolder(
                Submit('submit','Login Data',css_class='button white'),
            ),
        )