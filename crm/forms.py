from django import forms
from django.core.exceptions import ValidationError

from .models import Company, Phone, Email, Manager, Project, Interaction, ManagerCRM, User, Customer
from ckeditor.widgets import CKEditorWidget
from django.forms.models import inlineformset_factory


class CompanyModelForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data.get('title')

        qs = Company.objects.filter(title__iexact=title)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Введите уникальное название')
        return title


PhoneFormSet = inlineformset_factory(Company, Phone,
                                        fields=['phone_number'],
                                        can_delete=False, extra=2)

EmailFormSet = inlineformset_factory(Company, Email,
                                        fields=['email_address'],
                                        can_delete=False, extra=2)

ManagerFormSet = inlineformset_factory(Company, Manager,
                                        fields=['manager_name'],
                                        can_delete=False, extra=2)


class ProjectModelForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['company', 'name', 'description', 'start_date', 'end_date', 'price']


    def clean_title(self):
        name = self.cleaned_data.get('name')

        qs = Project.objects.filter(title__iexact=name)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Введите уникальное название')
        return name

    # def clean(self):
    #     start_date = self.cleaned_data['start_date']
    #     end_date = self.cleaned_data['end_date']
    #
    #     if end_date <= start_date:
    #         raise forms.ValidationError("End date must be later than start date")
    #     return super(ProjectModelForm, self).clean()


class InteractionModelForm(forms.ModelForm):

    class Meta:
        model = Interaction
        fields = ['project', 'channel_of_reference', 'reference_obj', 'company', 'description', 'rating']


class UserModelForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['photo', 'username', 'first_name', 'last_name', 'email', 'phone_number']



ManagerCRMFormSet = inlineformset_factory(User, ManagerCRM,
                                        fields=['name'],
                                        can_delete=False, extra=0)


CustomerFormSet = inlineformset_factory(User, Customer,
                                        fields=['name'],
                                        can_delete=False, extra=0)
