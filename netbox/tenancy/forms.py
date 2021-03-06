from django import forms
from django.db.models import Count

from utilities.forms import (
    BootstrapMixin, BulkImportForm, CommentField, CSVDataField, SlugField,
)

from .models import Tenant, TenantGroup


#
# Tenant groups
#

class TenantGroupForm(forms.ModelForm, BootstrapMixin):
    slug = SlugField()

    class Meta:
        model = TenantGroup
        fields = ['name', 'slug']


#
# Tenants
#

class TenantForm(forms.ModelForm, BootstrapMixin):
    slug = SlugField()
    comments = CommentField()

    class Meta:
        model = Tenant
        fields = ['name', 'slug', 'group', 'description', 'comments']


class TenantFromCSVForm(forms.ModelForm):
    group = forms.ModelChoiceField(TenantGroup.objects.all(), to_field_name='name',
                                   error_messages={'invalid_choice': 'Group not found.'})

    class Meta:
        model = Tenant
        fields = ['name', 'slug', 'group', 'description']


class TenantImportForm(BulkImportForm, BootstrapMixin):
    csv = CSVDataField(csv_form=TenantFromCSVForm)


class TenantBulkEditForm(forms.Form, BootstrapMixin):
    pk = forms.ModelMultipleChoiceField(queryset=Tenant.objects.all(), widget=forms.MultipleHiddenInput)
    group = forms.ModelChoiceField(queryset=TenantGroup.objects.all(), required=False)


def tenant_group_choices():
    group_choices = TenantGroup.objects.annotate(tenant_count=Count('tenants'))
    return [(g.slug, u'{} ({})'.format(g.name, g.tenant_count)) for g in group_choices]


class TenantFilterForm(forms.Form, BootstrapMixin):
    group = forms.MultipleChoiceField(required=False, choices=tenant_group_choices,
                                      widget=forms.SelectMultiple(attrs={'size': 8}))
