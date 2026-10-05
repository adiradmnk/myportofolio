from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project

class MainTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.admin = User.objects.create_superuser(username="adminuser", password="password123")
        self.editor_group = Group.objects.create(name="Editor")
        self.editor = User.objects.create_user(username="editoruser", password="password123")
        self.editor.groups.add(self.editor_group)
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
        self.assertContains(response, 'id="experience-search-form"')
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

        json_resp = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(json_resp.status_code, 200)
        self.assertIn("Intern Web Developer", json_resp.content.decode("utf-8"))

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada pengalaman")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        self.assertFalse(self.experience.is_ongoing)
        json_resp = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(json_resp.status_code, 200)
        data = json_resp.json()
        self.assertFalse(data[0]["fields"]["is_ongoing"])


    def test_projects_url_is_accessible(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_projects_page_with_data(self):
        Project.objects.create(title="BEFU", role="Project Leader", description="Aplikasi keren")
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, 'id="project-search-form"')

        json_resp = self.client.get(reverse("main:get_projects_json"))
        self.assertEqual(json_resp.status_code, 200)
        self.assertIn("BEFU", json_resp.content.decode("utf-8"))
        self.assertIn("Project Leader", json_resp.content.decode("utf-8"))

    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada proyek")

    def test_create_project_ajax_success(self):
        self.client.login(username="adminuser", password="password123")
        post_data = {
            "title": "Proyek AJAX Baru",
            "role": "Fullstack Engineer",
            "description": "Dibuat dengan AJAX",
            "link": "https://example.com/ajax",
        }
        response = self.client.post(reverse("main:create_project_ajax"), post_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["message"], "Proyek berhasil ditambahkan.")
        self.assertTrue(Project.objects.filter(title="Proyek AJAX Baru").exists())

    def test_create_project_ajax_unauthorized(self):
        response = self.client.post(reverse("main:create_project_ajax"), {"title": "Test"})
        self.assertEqual(response.status_code, 403)

        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("main:create_project_ajax"), {"title": "Test"})
        self.assertEqual(response.status_code, 403)

    def test_create_project_ajax_invalid(self):
        self.client.login(username="adminuser", password="password123")
        response = self.client.post(reverse("main:create_project_ajax"), {
            "title": "",
            "role": "Role",
            "description": "Desc",
        })
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("errors", data)

    def test_project_form_xss_protection(self):
        form_data = {
            "title": "<b>Proyek Bersih</b>",
            "role": "<b>Frontend</b> Lead",
            "description": "<p>Deskripsi aman</p>",
            "link": "https://example.com",
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Proyek Bersih")
        self.assertEqual(form.cleaned_data["role"], "Frontend Lead")
        self.assertEqual(form.cleaned_data["description"], "Deskripsi aman")

        empty_html_form = ProjectForm(data={
            "title": "<img src=x onerror=alert(1)>",
            "role": "Dev",
            "description": "Desc",
        })
        self.assertFalse(empty_html_form.is_valid())
        self.assertIn("title", empty_html_form.errors)


    def test_create_project_view(self):
        self.client.login(username="adminuser", password="password123")
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
        self.client.login(username="adminuser", password="password123")
        p = Project.objects.create(title="Proyek Hapus", role="Tester", description="Akan dihapus")
        delete_response = self.client.post(reverse("main:delete_project", kwargs={"project_id": p.id}))
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(Project.objects.filter(id=p.id).exists())

    def test_get_projects_json(self):
        Project.objects.create(title="Proyek JSON", role="Dev", description="Desc JSON")
        response = self.client.get(reverse("main:get_projects_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn("Proyek JSON", response.content.decode("utf-8"))

    def test_get_projects_xml(self):
        Project.objects.create(title="Proyek XML", role="Dev", description="Desc XML")
        response = self.client.get(reverse("main:get_projects_xml"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertIn("Proyek XML", response.content.decode("utf-8"))

    def test_create_experience_view(self):
        self.client.login(username="adminuser", password="password123")
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
        self.client.login(username="adminuser", password="password123")
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
        self.client.login(username="adminuser", password="password123")
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
        self.client.login(username="adminuser", password="password123")
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

    def test_user_cannot_access_protected_views(self):
        self.client.login(username="testuser", password="password123")
        p = Project.objects.create(title="P", role="R", description="D")
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 403)
        edit_resp = self.client.get(reverse("main:edit_project", kwargs={"project_id": p.id}))
        self.assertEqual(edit_resp.status_code, 403)
        del_resp = self.client.post(reverse("main:delete_project", kwargs={"project_id": p.id}))
        self.assertEqual(del_resp.status_code, 403)

    def test_editor_can_edit_but_cannot_create_or_delete(self):
        self.client.login(username="editoruser", password="password123")
        p = Project.objects.create(title="Editor Project", role="R", description="D")

        edit_url = reverse("main:edit_project", kwargs={"project_id": p.id})
        get_edit_resp = self.client.get(edit_url)
        self.assertEqual(get_edit_resp.status_code, 200)
        post_edit_resp = self.client.post(edit_url, {
            "title": "Editor Project Updated",
            "role": "Lead",
            "description": "Updated by editor",
            "link": "",
        })
        self.assertEqual(post_edit_resp.status_code, 302)
        p.refresh_from_db()
        self.assertEqual(p.title, "Editor Project Updated")

        exp_edit_url = reverse("main:edit_experience", kwargs={"experience_id": self.experience.id})
        get_exp_edit = self.client.get(exp_edit_url)
        self.assertEqual(get_exp_edit.status_code, 200)

        create_p_resp = self.client.get(reverse("main:create_project"))
        self.assertEqual(create_p_resp.status_code, 403)
        create_e_resp = self.client.get(reverse("main:create_experience"))
        self.assertEqual(create_e_resp.status_code, 403)

        del_p_resp = self.client.post(reverse("main:delete_project", kwargs={"project_id": p.id}))
        self.assertEqual(del_p_resp.status_code, 403)
        del_e_resp = self.client.post(reverse("main:delete_experience", kwargs={"experience_id": self.experience.id}))
        self.assertEqual(del_e_resp.status_code, 403)

    def test_toggle_star_project(self):
        self.client.login(username="testuser", password="password123")
        p = Project.objects.create(title="Star Test", role="Dev", description="Desc")
        star_url = reverse("main:toggle_star", kwargs={"project_id": p.id})
        
        resp = self.client.post(star_url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn(self.user, p.starred_by.all())

        resp2 = self.client.post(star_url)
        self.assertEqual(resp2.status_code, 302)
        self.assertNotIn(self.user, p.starred_by.all())

    def test_toggle_star_experience(self):
        self.client.login(username="testuser", password="password123")
        star_url = reverse("main:toggle_experience_star", kwargs={"experience_id": self.experience.id})

        resp = self.client.post(star_url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn(self.user, self.experience.starred_by.all())

        resp2 = self.client.post(star_url)
        self.assertEqual(resp2.status_code, 302)
        self.assertNotIn(self.user, self.experience.starred_by.all())

    def test_auth_flow(self):
        reg_response = self.client.get(reverse("main:register"))
        self.assertEqual(reg_response.status_code, 200)
        self.assertTemplateUsed(reg_response, "register.html")

        login_response = self.client.get(reverse("main:login"))
        self.assertEqual(login_response.status_code, 200)
        self.assertTemplateUsed(login_response, "login.html")

        post_login = self.client.post(reverse("main:login"), {"username": "testuser", "password": "password123"})
        self.assertEqual(post_login.status_code, 302)
        self.assertIn("last_login", post_login.cookies)

        logout_response = self.client.get(reverse("main:logout"))
        self.assertEqual(logout_response.status_code, 302)

    def test_create_experience_ajax_success(self):
        self.client.login(username="adminuser", password="password123")
        post_data = {
            "title": "Backend AI Researcher",
            "category": "research",
            "description": "Riset model AI",
            "thumbnail": "https://example.com/logo.png",
            "ended_at": "",
        }
        response = self.client.post(reverse("main:create_experience_ajax"), post_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["message"], "Pengalaman berhasil ditambahkan.")
        self.assertTrue(Experience.objects.filter(title="Backend AI Researcher").exists())

    def test_create_experience_ajax_unauthorized(self):
        response = self.client.post(reverse("main:create_experience_ajax"), {"title": "Test"})
        self.assertEqual(response.status_code, 403)

        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("main:create_experience_ajax"), {"title": "Test"})
        self.assertEqual(response.status_code, 403)

    def test_create_experience_ajax_invalid(self):
        self.client.login(username="adminuser", password="password123")
        response = self.client.post(reverse("main:create_experience_ajax"), {
            "title": "",
            "category": "internship",
            "description": "Desc",
        })
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("errors", data)

    def test_experience_form_xss_protection(self):
        form_data = {
            "title": "<b>Teaching Assistant</b>",
            "category": "part-time",
            "description": "<script>alert(1)</script>Membantu lab",
            "thumbnail": "https://example.com/logo.png",
            "ended_at": "",
        }
        form = ExperienceForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Teaching Assistant")
        self.assertNotIn("<script>", form.cleaned_data["description"])

        empty_html_form = ExperienceForm(data={
            "title": "<img src=x onerror=alert(1)>",
            "category": "internship",
            "description": "Desc",
        })
        self.assertFalse(empty_html_form.is_valid())
        self.assertIn("title", empty_html_form.errors)

    def test_get_experience_json_search_and_category_filter(self):
        Experience.objects.create(title="Volunteer UI UX", category="volunteer", description="Desain UI")
        response = self.client.get(reverse("main:get_experience_json") + "?category=volunteer")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["title"], "Volunteer UI UX")

        search_resp = self.client.get(reverse("main:get_experience_json") + "?q=Volunteer")
        self.assertEqual(search_resp.status_code, 200)
        search_data = search_resp.json()
        self.assertEqual(len(search_data), 1)


