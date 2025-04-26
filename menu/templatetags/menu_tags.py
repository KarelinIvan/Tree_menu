from django import template
from django.urls import resolve, Resolver404
from ..models import MenuItem

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path_info

    try:
        resolved_url = resolve(current_url)
        resolved_url_name = resolved_url.url_name
    except Resolver404:
        resolved_url_name = None

    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')

    def mark_active(items, active_item=None):
        for item in items:
            item_url = item.get_url()
            item.is_active = (
                    item_url == current_url or
                    (resolved_url_name and item.named_url == resolved_url_name)
            )
            if item.is_active:
                active_item = item
            item.children = mark_active(item.children.all(), active_item)
            if active_item and (item == active_item or item in active_item.parents):
                item.is_expanded = True
            else:
                item.is_expanded = False
        return items

    root_items = menu_items.filter(parent__isnull=True)
    menu_tree = mark_active(root_items)

    return {
        'menu_items': menu_tree,
        'menu_name': menu_name,
        'current_url': current_url,
    }