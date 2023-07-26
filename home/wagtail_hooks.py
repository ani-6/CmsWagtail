from wagtail import hooks
from wagtail.admin.userbar import AccessibilityItem
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from home.models import FooterText, Person

"""
N.B. To see what icons are available for use in Wagtail menus and StreamField block types,
enable the styleguide in settings:

INSTALLED_APPS = (
   ...
   'wagtail.contrib.styleguide',
   ...
)

or see https://thegrouchy.dev/general/2015/12/06/wagtail-streamfield-icons.html

This demo project also includes the wagtail-font-awesome-svg package, allowing further icons to be
installed as detailed here: https://github.com/allcaps/wagtail-font-awesome-svg#usage
"""


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        "wagtailfontawesomesvg/solid/suitcase.svg",
        "wagtailfontawesomesvg/solid/utensils.svg",
    ]


class CustomAccessibilityItem(AccessibilityItem):
    axe_run_only = None


@hooks.register("construct_wagtail_userbar")
def replace_userbar_accessibility_item(request, items):
    items[:] = [
        CustomAccessibilityItem() if isinstance(item, AccessibilityItem) else item
        for item in items
    ]





class PersonViewSet(SnippetViewSet):
    model = Person
    menu_label = "People"  # ditch this to use verbose_name_plural from model
    icon = "group"  # change as required
    list_display = ("first_name", "last_name", "job_title", "thumb_image")
    list_filter = {
        "job_title": ["icontains"],
    }


class FooterTextViewSet(SnippetViewSet):
    model = FooterText
    search_fields = ("body",)


class HubSnippetViewSetGroup(SnippetViewSetGroup):
    menu_label = "Hub Misc"
    menu_icon = "suitcase"  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (PersonViewSet, FooterTextViewSet)


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
register_snippet(HubSnippetViewSetGroup)
