from django import template
from django.db.models import Count

register = template.Library()


@register.filter
def get_range(value):
    value = int(value)
    """
      Filter - returns a list containing range made from given value
      Usage (in template):

      <ul>{% for i in 3|get_range %}
        <li>{{ i }}. Do something</li>
      {% endfor %}</ul>

      Results with the HTML:
      <ul>
        <li>0. Do something</li>
        <li>1. Do something</li>
        <li>2. Do something</li>
      </ul>

      Instead of 3 one may use the variable set in the views
    """
    return range(value)


@register.filter
def get_stars(value):
    value = int(value)
    html = ""
    for i in range(value):
        html += '<span class="fa fa-star"></span>'
    for i in range(5 - value):
        html += '<span class="fa fa-star-o"></span>'
    return html


@register.filter
def completeBuildCount(value):
    if value:
        t = value.filter(complete=True)
        if not t:
            return 0
        return len(t)
    return 0
