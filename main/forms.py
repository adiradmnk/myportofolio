from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, URLInput
from django.utils.html import strip_tags
from main.models import Experience, Project

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

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_role(self):
        return strip_tags(self.cleaned_data["role"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "category",
            "description",
            "thumbnail",
            "ended_at",
        ]
        labels = {
            "title": "Judul Pengalaman",
            "category": "Kategori",
            "description": "Deskripsi",
            "thumbnail": "URL Thumbnail / Logo",
            "ended_at": "Tanggal Selesai (Kosongkan jika masih berlangsung)",
        }
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Software Engineer Intern",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Deskripsikan pengalaman Anda...",
                    "rows": 4,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://...",
                }
            ),
        }
