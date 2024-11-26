from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .utils import generate_random_password

class CustomUserCreationForm(forms.ModelForm):
    generated_password = forms.CharField(
        label="Сгенерированный пароль",
        initial=generate_random_password,
        widget=forms.TextInput(attrs={"readonly": "readonly"})
    )

    class Meta:
        model = User
        fields = ['username']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['generated_password']
        user.set_password(password)
        if commit:
            user.save()
        return user

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'generated_password'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data['generated_password'])
        super().save_model(request, obj, form, change)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
