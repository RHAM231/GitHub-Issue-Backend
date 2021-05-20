import io
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
    ListView, DetailView, UpdateView, CreateView
)
from . models import Issue
from users.models import Profile
from repositories.models import RepoFolder, RepoFile, LineOfCode
from sync.github_client import create_issue, update_issue, open_close_issue
from . forms import IssueSearchForm, IssueEntryForm, OpenCloseIssueForm


class IssueListView(FormMixin, ListView):
    model = Issue
    template_name = 'issues/issue_list.html'
    context_object_name = 'issues'
    paginate_by = 8
    form_class = IssueSearchForm

    def get_queryset(self, **kwargs):
        form = self.form_class(self.request.GET)
        if self.request.GET and form.is_valid():
            condition1 = Q(title__icontains=form.cleaned_data['search'])
            condition2 = Q(created_at__icontains=form.cleaned_data['search'])
            condition3 = Q(body__icontains=form.cleaned_data['search'])
            conditions = condition1 | condition2 | condition3
            queryset = Issue.objects.filter(conditions).order_by('-created_at')
        else:
            queryset = Issue.objects.all().order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'
        context['form'] = IssueSearchForm()
        return context


class IssueView(View):
    def get(self, request, *args, **kwargs):
        view = IssueDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = OpenCloseIssueView.as_view()
        return view(request, *args, **kwargs)


class IssueDetailView(DetailView):
    model = Issue
    template_name = 'issues/issue_read.html'
    context_object_name = 'issue'
    slug_url_kwarg = 'issue_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'

        issue = context['issue']
        stamp = issue._meta.get_field('stamp')
        stamp_value = stamp.value_from_object(issue)
        if issue.associated_folder is not None:
            issue_path = stamp_value.splitlines()[0].replace('Issue Location: ', '')
        else:
            issue_path = None

        context['issue_path'] = issue_path
        context['form'] = OpenCloseIssueForm(initial={'state': self.object.state })
        return context


class OpenCloseIssueView(UpdateView):
    template_name = 'issues/issue_read.html'
    form_class = OpenCloseIssueForm
    model = Issue
    slug_url_kwarg = 'issue_slug'
    token = settings.TEST_TOKEN
    gh_user = settings.GH_USER

    def form_valid(self, form):
        if self.object.state == 'open':
            self.object.state = 'closed'
        elif self.object.state == 'closed':
            self.object.state = 'open'
        self.object.save()
        response = super(OpenCloseIssueView, self).form_valid(form)

        repo = self.object.repository.name
        issue_number = self.object.number
        state = self.object.state

        open_close_issue(self.token, self.gh_user, state, repo, issue_number)
        return response

    def get_success_url(self):
        return reverse('issue-read', kwargs={'issue_slug': self.object.slug})


class IssueCreateView(CreateView):
    model = Issue
    template_name = 'issues/issue_form.html'
    slug_url_kwarg = 'issue_slug'
    form_class = IssueEntryForm
    token = settings.TEST_TOKEN
    gh_user = settings.GH_USER

    def form_valid(self, form):
        if self.request.user.__class__.__name__ == "AnonymousUser":
            profile = Profile.objects.get(name='Guest')
        else:
            profile = Profile.objects.get(user=self.request.user)
        form.instance.author = profile
        response = super(IssueCreateView, self).form_valid(form)
        stamp = self.object.stamp
        issue_id = self.object.id
        data = form.cleaned_data
        create_issue(self.token, self.gh_user, data, stamp, issue_id)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'
        context['create'] = 'create'
        return context


def load_options(request):
    if request.GET.get('repo'):
        instance_id = request.GET.get('repo')
        instances = RepoFolder.objects.filter(repository=instance_id).order_by('name')
    elif request.GET.get('folder'):
        instance_id = request.GET.get('folder')
        instances = RepoFile.objects.filter(parent_folder=instance_id).order_by('name')
    elif request.GET.get('file'):
        instance_id = request.GET.get('file')
        instances = LineOfCode.objects.filter(repofile=instance_id).order_by('line_number')
    else:
        instances = None
    context = {'instances': instances}
    return render(request, 'issues/select_dropdown_list_options.html', context)


class IssueUpdateView(UpdateView):
    model = Issue
    template_name = 'issues/issue_form.html'
    context_object_name = 'issue'
    slug_url_kwarg = 'issue_slug'
    form_class = IssueEntryForm
    token = settings.TEST_TOKEN
    gh_user = settings.GH_USER

    def form_valid(self, form):
        response = super(IssueUpdateView, self).form_valid(form)
        stamp = self.object.stamp
        issue_number = self.object.number
        data = form.cleaned_data
        update_issue(self.token, self.gh_user, data, stamp, issue_number)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'
        context['update'] = 'update'
        return context
