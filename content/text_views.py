
from django.views.generic import ListView, DetailView

from .models import Text


class TextListView(ListView):
    model = Text
    template_name = "content/text_list.html"
    context_object_name = "texts"
    paginate_by = 8

    def get_queryset(self):
        return Text.objects.select_related(
            "philosopher"
        ).order_by("title")


class TextDetailView(DetailView):
    model = Text
    template_name = "content/text_detail.html"
    context_object_name = "text"

    def get_queryset(self):
        return Text.objects.select_related(
            "philosopher"
        )
