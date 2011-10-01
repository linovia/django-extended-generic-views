
What does this application that Django doesn't ?
================================================

Named Keys/Slugs
----------------

The Django generic views expects you to have either pk or slug in your urls
regular expressions. You can bypass this with the ecbv views. For example
you can have your urls.py::

    from django.conf.urls.defaults import patterns, url, include
    from . import views


    urlpatterns = patterns('',
        url(r'^poll/(?P<poll_id>\d+)/$',
            views.PollDetail.as_view(),
            name='poll'),
    )

Then in order to match the poll_id, you'll set your views.py::

    from . import models
    import ecbv


    class PollDetail(ecbv.DetailView):
        model = models.Poll
        pk_name = 'poll_id'


That way, if you browse to ``/poll/4/`` you'll be able to see the Poll which
primary key matches 4.

This allows to chain urlpatterns without having to deal which id should be
called pk and which should have its real name::

    from django.conf.urls.defaults import patterns, url, include
    from . import views


    poll_urlpatterns = patterns('',
        url(r'^$',                              views.PollDetail.as_view(),     name='poll'),
        url(r'^choice/(?P<choice_id>\d+)/$',    views.ChoiceDetail.as_view(),   name='choice'),
    )


    urlpatterns = patterns('',
        url(r'^poll/(?P<poll_id>\d+)/', include(poll_urlpatterns)),

    )

Then in your views.py you can define your classes::

    from . import models
    import ecbv


    class PollDetail(ecbv.DetailView):
        model = models.Poll
        pk_name = 'poll_id'


    class ChoiceDetail(ecbv.DetailView):
        model = models.Choice
        pk_name = 'choice_id'


Easily extended context
-----------------------

Every Mixin class inherits from the BaseMixin. This makes context extension
much easier and safer. For example, if you need a form tied with a given object
you can easily create a view with both::

    import ecbv


    class MyView(ecbv.DetailMixin, ecbv.FormView):
        model = Poll
        form = SomeForm


In order to extend the context you can also easily create your own mixin::

    from . import models
    import ecbv


    class ProjectMixin(generic.BaseMixin):
        def setup(self, request, *args, **kwargs):
            project_id = kwargs['project_id']
            self.project = get_object_or_404(models.Project, pk=project_id)
            super(ProjectMixin, self).setup(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
            kwargs['project'] = self.project
            return super(ProjectMixin, self).get_context_data(**kwargs)


    class Milestone(ProjectMixin, generic.DetailView):
        model = models.Milestone


With this example, you'll have milestone and project available in your
context. Those who fully read the example will have noticed the presence of
the setup function. This is called early when the request is processed and
is the perfect location for enriching the view instance and checking
permissions::

    from django.core.exceptions import PermissionDenied
    from . import models
    import ecbv


    class ProjectMixin(generic.BaseMixin):
        def setup(self, request, *args, **kwargs):
            super(ProjectMixin, self).setup(request, *args, **kwargs)
            if not self.object.project_id == kwargs['project_id']:
                raise PermissionDenied("You don't have the right")

            self.project = self.object.project
            if not request.user == self.project.owner:
                raise PermissionDenied("You don't have the right")

        def get_context_data(self, **kwargs):
            kwargs['project'] = self.project
            return super(ProjectMixin, self).get_context_data(**kwargs)


    class Milestone(ProjectMixin, generic.DetailView):
        model = models.Milestone

In that example, only the owner will be allowed to access the milestone
associated with the project.


Revisited redirections
----------------------

The RedirectView can also use named arguments instead of just urls.
For example, if you have the following urls.py::

    from django.conf.urls.defaults import patterns, url, include
    import ecbv
    from . import views


    urlpatterns = patterns('',
           (r'^poll/(?P<poll_id>\d+)/$',        ecbv.RedirectView.as_view(view='poll')),
        url(r'^poll/(?P<poll_id>\d+)/about/$',  views.PollView.as_view(),   name='poll'),
    )


No tests
--------

On the radar !
