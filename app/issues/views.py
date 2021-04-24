# Python Imports
import io

# Django Imports: Logic from the Django Framework
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render
from django.views.generic import (
    ListView, DeleteView, DetailView, UpdateView, CreateView
)

# Django Imports: Logic specific to this project
from . models import Issue
from . forms import IssueSearchForm, IssueEntryForm
from sync.github_client import create_issue, update_issue


#################################################################################################################################
# SUMMARY
#################################################################################################################################

'''
Let's define CRUD functionality for our issues. We use Django's pre-built class based views, ListView, DetailView, CreateView,
UpdateView, and DeleteView.

Any time we use a view to make changes to our issues, we'll also call our GitHub issue methods from github_client.py in the sync
app.

We'll pull GitHub login information from our settings.py file (in turn pulled from a config file) and pass the credentials into
our GitHub methods by overwriting form_valid on our edit views.

Issue Tracker will first save our form data to our database, then create the issue on GitHub, updating our database instance
with the newly created GitHub issue number.
'''

#################################################################################################################################
# BEGIN VIEWS
#################################################################################################################################


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


class IssueCreateView(CreateView):
    # Set our standard values for the create view
    model = Issue
    template_name = 'issues/issue_form.html'
    slug_url_kwarg = 'issue_slug'
    form_class = IssueEntryForm

    # Pull our GitHub login info from settings.py to pass to our 
    # create_issue method below
    token = settings.TEST_TOKEN
    gh_user = settings.GH_USER

    # Overwrite CreateView's form_valid method so we can call our GitHub create_issue
    # method when saving the form
    def form_valid(self, form):
        # form.instance.author = self.request.user
        # First save the valid form data to create the new object in our database
        response = super(IssueCreateView, self).form_valid(form)

        # Grab some data from our new instance as well as the form data
        stamp = self.object.stamp
        issue_id = self.object.id
        data = form.cleaned_data

        # Now call our create method from our github_client script to create the 
        # object in GitHub's database and update our database with the newly created
        # GitHub number
        create_issue(self.token, self.gh_user, data, stamp, issue_id)

        # Now that we've created matching instances in both databases, redirect to
        # our object detail page
        return response

    # Add additonal parameters to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'
        # Tell the template we need the create button for the form
        context['create'] = 'create'
        return context


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
        # stamp = self.object.stamp
        issue_number = self.object.number
        data = form.cleaned_data
        update_issue(self.token, self.gh_user, data, issue_number)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'
        # Tell the template we need the update buttons for the form
        context['update'] = 'update'
        return context


# def issue_delete(request):
#     context = {
#         'title': 'Issues',
#     }
#     return render(request, 'base/issue_delete.html', context)

#################################################################################################################################
# END
#################################################################################################################################
