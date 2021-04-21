from django.shortcuts import render
from django.views.generic import (
    ListView, DeleteView, DetailView, UpdateView, CreateView
)
from . models import Issue
from . forms import IssueSearchForm, IssueEntryForm
from django.db.models import Q
import io

# def issue_create(request):
#     form = IssueCreateForm()
#     context = {
#         'form': form,
#         'title': 'Issues',
#     }
#     return render(request, 'base/issue_create.html', context)


class IssueCreateView(CreateView):
    model = Issue
    template_name = 'issues/issue_create.html'
    slug_url_kwarg = 'issue_slug'
    form_class = IssueEntryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'
        return context


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
    # pk_url_kwarg = 'issue_id'
    slug_url_kwarg = 'issue_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'

        issue = context['issue']
        stamp = issue._meta.get_field('stamp')
        stamp_value = stamp.value_from_object(issue)
        if issue.associated_folder is not None:
            issue_path = stamp_value.splitlines()[0].replace('Issue Location: ', '')
            # stamp_value = stamp_value.split('\n',7)[7]
        else:
            issue_path = None
        # context['issue_stamp'] = stamp_value
        context['issue_path'] = issue_path
        return context


class IssueUpdateView(UpdateView):
    model = Issue
    template_name = 'issues/issue_update.html'
    context_object_name = 'issue'
    slug_url_kwarg = 'issue_slug'
    form_class = IssueEntryForm
    # fields = ['title', 'associated_folder', 'associated_file', 'associated_loc', 'body']

    def form_valid(self, form):
        # form.instance.author = self.request.user
        return super(IssueUpdateView, self).form_valid(form)

    # def test_func(self)
    #     issue = self.get_object()
    #     if self.request.user == issue.author:
    #         return True
    #     return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'

        issue = context['issue']
        stamp = issue._meta.get_field('stamp')
        stamp_value = stamp.value_from_object(issue)
        if issue.associated_folder is not None:
            issue_path = stamp_value.splitlines()[0].replace('Issue Location: ', '')
            # stamp_value = stamp_value.split('\n',7)[7]
        else:
            issue_path = None
        # context['issue_stamp'] = stamp_value
        context['issue_path'] = issue_path
        return context


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
    # paginate_by = 5
    form_class = IssueSearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            # condition1 = Q(state=form.cleaned_data['search'])
            condition2 = Q(state=form.cleaned_data['filters'])
            # condition3 = Q(field=form.cleaned_data['author'])
            # condition4 = Q(repository=form.cleaned_data['projects'])
            # condition5 = Q(field=form.cleaned_data['sort'])
            # conditions = condition1 & condition2 & condition3 & condition4 & condition5
            conditions = condition2
            print(conditions)
            queryset = Issue.objects.filter(conditions)
            print(queryset)
        queryset = Issue.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'
        context['form'] = IssueSearchForm()
        return context
