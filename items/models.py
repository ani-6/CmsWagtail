from __future__ import unicode_literals

from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route, re_path
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index

from home.blocks import BaseStreamBlock

# Create your models here.
class ItemPage(RoutablePageMixin, Page):
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and 3000px.",
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True
    )
    subtitle = models.CharField(blank=True, max_length=255)
    link = models.CharField(blank=True, max_length=255)
    date_published = models.DateField("Date article published", blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("introduction"),
        FieldPanel("image"),
        FieldPanel("body"),
        FieldPanel("date_published"),
        FieldPanel("link"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]


    # Specifies parent to BlogPage as being BlogIndexPages
    parent_page_types = ["ItemIndexPage"]

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []


class ItemIndexPage(RoutablePageMixin, Page):

    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and 3000px.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
    ]

    # Specifies that only BlogPage objects can live under this index page
    subpage_types = ["ItemPage"]

    # Defines a method to access the children of the page (e.g. BlogPage
    # objects). On the demo site we use this on the HomePage
    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to list all child items, that are live, by the
    # date that they were published
    # https://docs.wagtail.org/en/stable/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(ItemIndexPage, self).get_context(request)
        context["posts"] = (
            ItemPage.objects.descendant_of(self).live().order_by("-date_published")
        )
        return context

    
    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child BlogPage objects for this BlogPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = ItemPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts
