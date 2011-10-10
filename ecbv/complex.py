
from copy import copy

from . import base, edit, detail
# from django.core.exceptions import ImproperlyConfigured

# from django.forms import models as model_forms
from django.forms.models import modelformset_factory


class ModelInlineFormMixin(edit.ModelFormMixin):
    """
    A mixin that provides a way to show and handle an inline formset.
    """
    inline_forms = None

    def get_inline_forms(self):
        inlines = {}
        for name, conf in self.inline_forms.items():
            relation_name = conf['relation_name']
            field = getattr(self.object, relation_name)
            class_name = field.model
            conf = copy(conf)
            del conf['relation_name']
            FormSet = modelformset_factory(class_name, **conf)
            conf['queryset'] = getattr(self.object, relation_name).all()
            inlines[name] = FormSet()
        return inlines

    # def get_inline_form_kwargs(self, name):
    #     """
    #     Returns the keyword arguments for instanciating the form.
    #     """
    #     kwargs = copy(self.inline_forms[name])
    #     return kwargs

    def form_valid(self, form, inline_forms):
        self.object = form.save()
        map(lambda x, y: y.save(), inline_forms.items())
        return super(ModelInlineFormMixin, self).form_valid(form)

    def form_invalid(self, form, inline_forms):
        return self.render_to_response(self.get_context_data(form=form, inline_forms=inline_forms))


class ProcessMultiFormView(base.View):
    """
    A mixin that processes a form on POST.
    """
    def get(self, request, *args, **kwargs):
        self.setup(request, *args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        inline_forms = self.get_inline_forms()
        return self.render_to_response(self.get_context_data(form=form, inline_forms=inline_forms))

    def post(self, request, *args, **kwargs):
        self.setup(request, *args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        inline_forms = self.get_inline_forms()
        if form.is_valid() and reduce(lambda x, y: x and y, inline_forms, True):
            return self.form_valid(form, inline_forms)
        else:
            return self.form_invalid(form, inline_forms)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class InlineCreateView(detail.SingleObjectTemplateResponseMixin,
                        ModelInlineFormMixin, ProcessMultiFormView):
    """
    Base view for creating an new object instance.

    Using this base class requires subclassing to provide a response mixin.
    """
    template_name_suffix = '_form'

    def get(self, request, *args, **kwargs):
        return super(InlineCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(InlineCreateView, self).post(request, *args, **kwargs)
