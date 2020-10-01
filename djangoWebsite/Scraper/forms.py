from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class NewsInput(forms.Form):
    input_ = forms.CharField(label = 'Input',max_length=100, required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                " ",
                'input_',
                " ",
            ),
            ButtonHolder(
                Submit('Submit', 'Submit Data', css_class='button white')
            )
        )