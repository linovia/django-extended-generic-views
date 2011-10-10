from .base import BaseMixin
from .base import View, TemplateView, RedirectView
from .dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView,
                                     WeekArchiveView, DayArchiveView, TodayArchiveView,
                                     DateDetailView)
from .detail import DetailView
from .edit import FormView, CreateView, UpdateView, DeleteView
from .list import ListView

import detail, edit, list, base, complex


class GenericViewError(Exception):
    """A problem in a generic view."""
    pass


#
# Dirty hack to make the resolve view much more powerful
#

from django.core.urlresolvers import get_callable
from django.core.urlresolvers import NoReverseMatch
from django.utils.encoding import force_unicode
import re


def class_ecbv_reverse(self, lookup_view, *args, **kwargs):
    '''
    Duplicate RegexURLPattern.reverse but removed the kwargs count check
    '''
    if args and kwargs:
        raise ValueError("Don't mix *args and **kwargs in call to reverse()!")
    try:
        lookup_view = get_callable(lookup_view, True)
    except (ImportError, AttributeError), e:
        raise NoReverseMatch("Error importing '%s': %s." % (lookup_view, e))
    possibilities = self.reverse_dict.getlist(lookup_view)
    for possibility, pattern in possibilities:
        for result, params in possibility:
            if args:
                if len(args) != len(params):
                    continue
                unicode_args = [force_unicode(val) for val in args]
                candidate = result % dict(zip(params, unicode_args))
            else:
                unicode_kwargs = dict([(k, force_unicode(v)) for (k, v) in kwargs.items()])
                candidate = result % unicode_kwargs
            if re.search(u'^%s' % pattern, candidate, re.UNICODE):
                return candidate
    # lookup_view can be URL label, or dotted path, or callable, Any of
    # these can be passed in at the top, but callables are not friendly in
    # error messages.
    m = getattr(lookup_view, '__module__', None)
    n = getattr(lookup_view, '__name__', None)
    if m is not None and n is not None:
        lookup_view_s = "%s.%s" % (m, n)
    else:
        lookup_view_s = lookup_view
    raise NoReverseMatch("Reverse for '%s' with arguments '%s' and keyword "
            "arguments '%s' not found." % (lookup_view_s, args, kwargs))

from django.core.urlresolvers import RegexURLResolver

RegexURLResolver.ecbv_reverse = class_ecbv_reverse
