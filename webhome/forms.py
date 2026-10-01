from . models import Contact,Student
from django import forms

class ContactForm(forms.ModelForm) : 
    class Meta:
        model= Contact
        fields= '__all__'


class StudentForm(forms.ModelForm):

    HOBBY_CHOICES = [
        ('Reading', 'Reading'),
        ('Music', 'Music'),
        ('Sports', 'Sports'),
        ('Travel', 'Travel'),
        ('Drawing', 'Drawing'),
        ('Gaming', 'Gaming'),
    ]

    hobbies = forms.MultipleChoiceField(
        choices=HOBBY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Student

        fields = [
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'email',
            'phone_number',
            'country',
            'state',
            'city',
            'hobbies',
            'avatar',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'gender': forms.RadioSelect(
                choices=[
                    ('Male', 'Male'),
                    ('Female', 'Female'),
                    ('Other', 'Other'),
                ]
            ),

            'country': forms.Select(
                attrs={'id': 'id_country'}
            ),

            'state': forms.Select(
                attrs={'id': 'id_state'}
            ),

            'city': forms.Select(
                attrs={'id': 'id_city'}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data['email']

        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email