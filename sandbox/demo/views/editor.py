from django.views.generic import TemplateView


class EditorSampleView(TemplateView):
    """
    Editor integration sample.
    """
    template_name = "demo/editor_sample.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
