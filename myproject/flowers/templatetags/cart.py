from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def cart_contents(context):
    request = context['request']
    cart = request.session.get('cart', {})
    return cart