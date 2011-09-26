from .base import View, TemplateView, RedirectView
from .dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView,
                                     WeekArchiveView, DayArchiveView, TodayArchiveView,
                                     DateDetailView)
from .detail import DetailView
from .edit import FormView, CreateView, UpdateView, DeleteView
from .list import ListView

import detail, edit, list, base

class GenericViewError(Exception):
    """A problem in a generic view."""
    pass
