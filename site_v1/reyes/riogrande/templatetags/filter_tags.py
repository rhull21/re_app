from django import template

register = template.Library()

@register.filter(name='get_field')
def get_field(form, field_name):
    return form.fields.get(field_name)

@register.filter(name='match_field')
def match_field(field_name, filter_name):
    if field_name == filter_name:
        return True
    else:
        return False