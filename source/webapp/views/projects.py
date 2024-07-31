from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ArticleForm, SearchForm
from webapp.forms.projects import ProjectForm, AddUsersInProjectForm
from webapp.models import Article, Project


class ProjectsListView(ListView):
    model = Project
    template_name = "projects/projects_list.html"
    ordering = ['-created_at']
    context_object_name = "projects"


class CreateProjectView(PermissionRequiredMixin, CreateView):
    template_name = "projects/create_project.html"
    form_class = ProjectForm
    permission_required = "projects.add_projects"

    def form_valid(self, form):
        project = form.save()
        project.users.add(self.request.user)
        return redirect("webapp:projects")


#

class ProjectDetailView(DetailView):
    template_name = "projects/project_detail.html"
    model = Project


class UpdateProjectView(PermissionRequiredMixin, UpdateView):
    template_name = "projects/update_project.html"
    form_class = ProjectForm
    model = Project
    permission_required = "webapp.change_project"

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()

    def get_success_url(self):
        return reverse("webapp:project_detail", kwargs={"pk": self.object.pk})


class AddUsersView(PermissionRequiredMixin, UpdateView):
    template_name = "projects/add_users_in_project.html"
    form_class = AddUsersInProjectForm
    model = Project
    permission_required = "webapp.add_users_in_project"

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()

    def get_success_url(self):
        return reverse("webapp:project_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        result = super().get_form_kwargs()
        result["user"] = self.request.user
        return result
#
#
# class DeleteArticleView(PermissionRequiredMixin, DeleteView):
#     template_name = "articles/delete_article.html"
#     model = Article
#     success_url = reverse_lazy("webapp:articles")
#     permission_required = "webapp.delete_article"
#
#     def has_permission(self):
#         return super().has_permission() or self.request.user == self.get_object().author
