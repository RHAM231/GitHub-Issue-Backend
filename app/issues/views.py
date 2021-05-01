# Python Imports
import io

# Django Imports: Logic from the Django Framework
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render
# from django.views.generic.edit import FormMixin

# from django.http import HttpResponseForbidden
from django.views import View
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin

from django.views.generic import (
    ListView, DeleteView, DetailView, UpdateView, CreateView
)

# Django Imports: Logic specific to this project
from . models import Issue
from sync.github_client import create_issue, update_issue
from . forms import IssueSearchForm, IssueEntryForm, OpenCloseIssueForm, IssueStateFilterForm


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


# Define a view to list all our issues
class IssueListView(FormMixin, ListView):
    model = Issue
    template_name = 'issues/issue_list.html'
    context_object_name = 'issues'
    paginate_by = 5
    form_class = IssueSearchForm

    # Override ListView's get_queryset() method to add simple search to our view
    def get_queryset(self, **kwargs):
        form = self.form_class(self.request.GET)
        # If we have form data, use it to define a queryset
        if self.request.GET and form.is_valid():
            condition1 = Q(title__icontains=form.cleaned_data['search'])
            condition2 = Q(created_at__icontains=form.cleaned_data['search'])
            condition3 = Q(body__icontains=form.cleaned_data['search'])
            conditions = condition1 | condition2 | condition3
            queryset = Issue.objects.filter(conditions).order_by('created_at')
        # If we're visiting the page for the first time, return all our issues
        else:
            queryset = Issue.objects.all().order_by('created_at')
        return queryset

    # Add a page title and our search form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'
        context['form'] = IssueSearchForm()
        return context


# Define a generic view to display a single issue. Reroute to either a detail view or
# an update view depending on whether we're using get or post.
class IssueView(View):
    def get(self, request, *args, **kwargs):
        view = IssueDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = OpenCloseIssueView.as_view()
        return view(request, *args, **kwargs)


# If using get, just display the issue with it's parameters and the update form in context
class IssueDetailView(DetailView):
    model = Issue
    template_name = 'issues/issue_read.html'
    context_object_name = 'issue'
    slug_url_kwarg = 'issue_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Issues'

        # Get our stamp text to display as additional data
        issue = context['issue']
        stamp = issue._meta.get_field('stamp')
        stamp_value = stamp.value_from_object(issue)
        # Create a stamp path parameter from the stamp info to add to context
        if issue.associated_folder is not None:
            issue_path = stamp_value.splitlines()[0].replace('Issue Location: ', '')
        else:
            issue_path = None

        context['issue_path'] = issue_path
        context['form'] = OpenCloseIssueForm(initial={'state': self.object.state })
        return context


# If using post, check whether the issue is open or closed, update it, and 
# then return the issue's detail view
class OpenCloseIssueView(UpdateView):
    template_name = 'issues/issue_read.html'
    form_class = OpenCloseIssueForm
    model = Issue
    slug_url_kwarg = 'issue_slug'

    # If the issue is closed, open it. If open, close it.
    def form_valid(self, form):
        if self.object.state == 'open':
            self.object.state = 'closed'
        elif self.object.state == 'closed':
            self.object.state = 'open'
        self.object.save()
        return super(OpenCloseIssueView, self).form_valid(form)

    # Redirect to our detail view
    def get_success_url(self):
        return reverse('issue-read', kwargs={'issue_slug': self.object.slug})


class IssueCreateView(CreateView):
    # Set our standard values for the create view
    model = Issue
    template_name = 'issues/issue_form.html'
    slug_url_kwarg = 'issue_slug'
    form_class = IssueEntryForm

    # Pull our GitHub login info from settings.py to pass to our create_issue method below
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
    # Set our standard values for the create view
    model = Issue
    template_name = 'issues/issue_form.html'
    context_object_name = 'issue'
    slug_url_kwarg = 'issue_slug'
    form_class = IssueEntryForm

    # Pull our GitHub login info from settings.py to pass to our create_issue method below
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


#################################################################################################################################
# END
#################################################################################################################################
