from django.shortcuts import render
from django.views.generic import (
    ListView, DeleteView, DetailView, UpdateView
)
from . models import Issue
from . forms import IssueSearchForm


# def issue_create(request):
#     form = IssueCreateForm()
#     context = {
#         'form': form,
#         'title': 'Issues',
#     }
#     return render(request, 'base/issue_create.html', context)


# def issue_read(request):
#     context = {
#         'condition': True,
#         'title': 'Issues',
#     }
#     return render(request, 'base/issue_read.html', context)


class IssueDetailView(DetailView):
    model = Issue
    template_name = 'issues/issue_read.html'
    context_object_name = 'issue'
    slug_url_kwarg = 'issue_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'
        return context


# def issue_update(request):
#     form = IssueCreateForm()
#     context = {
#         'form': form,
#         'title': 'Issues',
#     }
#     return render(request, 'base/issue_update.html', context)


# def issue_delete(request):
#     context = {
#         'title': 'Issues',
#     }
#     return render(request, 'base/issue_delete.html', context)


# def issue_list(request):
#     # form = IssueSearchForm()
#     context = {
#         'form': form,
#         'title': 'Issues',
#     }
#     return render(request, 'base/issue_list.html', context)


class IssueListView(ListView):
    model = Issue
    template_name = 'issues/issue_list.html'
    context_object_name = 'issues'
    form_class = IssueSearchForm

    def get_queryset(self):
        queryset = Issue.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'
        return context
