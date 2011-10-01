
from django.core.urlresolvers import get_urlconf, get_resolver, get_script_prefix
from django.utils.encoding import iri_to_uri
from django.core.urlresolvers import NoReverseMatch


def ecbv_reverse(viewname, urlconf=None, args=None, kwargs=None, prefix=None, current_app=None):
    if urlconf is None:
        urlconf = get_urlconf()
    resolver = get_resolver(urlconf)
    args = args or []
    kwargs = kwargs or {}

    if prefix is None:
        prefix = get_script_prefix()

    if not isinstance(viewname, basestring):
        view = viewname
    else:
        parts = viewname.split(':')
        parts.reverse()
        view = parts[0]
        path = parts[1:]

        resolved_path = []
        while path:
            ns = path.pop()

            # Lookup the name to see if it could be an app identifier
            try:
                app_list = resolver.app_dict[ns]
                # Yes! Path part matches an app in the current Resolver
                if current_app and current_app in app_list:
                    # If we are reversing for a particular app, use that namespace
                    ns = current_app
                elif ns not in app_list:
                    # The name isn't shared by one of the instances (i.e., the default)
                    # so just pick the first instance as the default.
                    ns = app_list[0]
            except KeyError:
                pass

            try:
                extra, resolver = resolver.namespace_dict[ns]
                resolved_path.append(ns)
                prefix = prefix + extra
            except KeyError, key:
                if resolved_path:
                    raise NoReverseMatch("%s is not a registered namespace inside '%s'" % (key, ':'.join(resolved_path)))
                else:
                    raise NoReverseMatch("%s is not a registered namespace" % key)

    return iri_to_uri(u'%s%s' % (prefix, resolver.ecbv_reverse(view,
            *args, **kwargs)))
