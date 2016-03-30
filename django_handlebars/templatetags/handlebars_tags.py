
import json
import os

from django import template
from django_handlebars import appsettings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def handlebars_scripts():
    template = '''
<script>var handlebars_config = %(conf)s;</script>
<script src="%(base)s%(renderer)s"></script>
<script src="%(base)shandlebars.django.js"></script>''' % {
    "conf": json.dumps(appsettings.SCRIPT_CONF),
    "base": appsettings.SCRIPT_URL,
    "renderer": "handlebars.runtime.js" if appsettings.COMPILED else "handlebars.js",}
    return mark_safe(template)

@register.simple_tag()
def handlebars_template(name):
    basepath = os.path.realpath(appsettings.TPL_CMPDIR if appsettings.COMPILED else appsettings.TPL_DIR)
    ext = "js" if appsettings.COMPILED else "html"

    path = os.path.realpath("%s/%s.%s" % (basepath, name, ext))
    if not path.startswith(basepath) or not os.path.exists(path):
        return '<script>/* Invalid template spec "%s" */</script>' % name

    with open(path, "r") as f:
        src = f.read()

    if not appsettings.COMPILED:
        src = json.dumps(src)

    return mark_safe('<script>{0}</script>'.format(appsettings.SCRIPT_TPL % {"namespace": name, "compiled": src}))


@register.simple_tag()
def handlebars_load_template(name):
    return mark_safe('<script>Handlebars.tpl("{0}");</script>'.format(name))
