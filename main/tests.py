from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Experience

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Intern Web Developer",
            description="Memimpin riset dan pengembangan EDLIG.",
            category="internship",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Intern Web Developer")
        self.assertEqual(self.experience.category, "internship")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Internship")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))
        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_projects_url_is_accessible(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_projects_page_with_data(self):
        from main.models import Project
        p = Project.objects.create(title="BEFU", role="Project Leader", description="Aplikasi keren")
        response = self.client.get(reverse("main:show_projects"))
        self.assertContains(response, "BEFU")
        self.assertContains(response, "Project Leader")
        self.assertContains(response, "Aplikasi keren")

    def test_empty_projects_page(self):
        from main.models import Project
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))
        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    def test_create_project_view(self):
        from main.models import Project
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")

        post_data = {
            "title": "Proyek Uji Coba",
            "role": "Developer",
            "description": "Deskripsi uji coba",
            "link": "https://github.com/example",
        }
        post_response = self.client.post(reverse("main:create_project"), post_data)
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(Project.objects.filter(title="Proyek Uji Coba").exists())

    def test_delete_project_view(self):
        from main.models import Project
        p = Project.objects.create(title="Proyek Hapus", role="Tester", description="Akan dihapus")
        delete_response = self.client.post(reverse("main:delete_project", kwargs={"project_id": p.id}))
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(Project.objects.filter(id=p.id).exists())

    def test_get_projects_json(self):
        from main.models import Project
        Project.objects.create(title="Proyek JSON", role="Dev", description="Desc JSON")
        response = self.client.get(reverse("main:get_projects_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn("Proyek JSON", response.content.decode("utf-8"))

    def test_get_projects_xml(self):
        from main.models import Project
        Project.objects.create(title="Proyek XML", role="Dev", description="Desc XML")
        response = self.client.get(reverse("main:get_projects_xml"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertIn("Proyek XML", response.content.decode("utf-8"))

    def test_create_experience_view(self):
        response = self.client.get(reverse("main:create_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")

        post_data = {
            "title": "Teaching Assistant",
            "category": "part-time",
            "description": "Membantu asistensi lab.",
            "thumbnail": "",
            "ended_at": "",
        }
        post_response = self.client.post(reverse("main:create_experience"), post_data)
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(Experience.objects.filter(title="Teaching Assistant").exists())

    def test_edit_experience_view(self):
        edit_url = reverse("main:edit_experience", kwargs={"experience_id": self.experience.id})
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_edit.html")

        post_data = {
            "title": "Senior Web Developer Intern",
            "category": "internship",
            "description": "Deskripsi baru terupdate",
            "thumbnail": "",
            "ended_at": "",
        }
        post_response = self.client.post(edit_url, post_data)
        self.assertEqual(post_response.status_code, 302)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Senior Web Developer Intern")

    def test_delete_experience_view(self):
        exp = Experience.objects.create(title="Exp to Delete", description="test", category="freelance")
        delete_url = reverse("main:delete_experience", kwargs={"experience_id": exp.id})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Experience.objects.filter(id=exp.id).exists())

    def test_get_experience_json(self):
        response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn("Intern Web Developer", response.content.decode("utf-8"))

    def test_edit_project_view(self):
        from main.models import Project
        p = Project.objects.create(title="Old Title", role="Dev", description="Desc")
        edit_url = reverse("main:edit_project", kwargs={"project_id": p.id})
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_edit.html")

        post_data = {
            "title": "New Title",
            "role": "Lead Dev",
            "description": "Updated Desc",
            "link": "https://example.com",
        }
        post_response = self.client.post(edit_url, post_data)
        self.assertEqual(post_response.status_code, 302)
        p.refresh_from_db()
        self.assertEqual(p.title, "New Title")
