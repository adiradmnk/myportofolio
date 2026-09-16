from django.forms import ModelForm, TextInput, Textarea, URLInput
from main.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "role",
            "description",
            "link",
        ]
        labels = {
            "title": "Nama Proyek",
            "role": "Peran / Posisi",
            "description": "Deskripsi Proyek",
            "link": "Link Proyek",
        }
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Nama Proyek",
                    "maxlength": 255,
                }
            ),
            "role": TextInput(
                attrs={
                    "placeholder": "Frontend Developer, Lead, dll.",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan proyekmu...",
                    "rows": 4,
                }
            ),
            "link": URLInput(
                attrs={
                    "placeholder": "https://github.com/...",
                }
            ),
        }
