from django import forms
from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.edit import FormView


class SampleForm(forms.Form):
    """
    Sample form that can switch editor on its field depending given editor definition.
    """
    def __init__(self, *args, **kwargs):
        editor = kwargs.pop("editor")

        super().__init__(*args, **kwargs)

        editor_field = editor.get_field_class()
        self.fields["textarea_empty"] = editor_field(label="Textarea empty")
        self.fields["textarea_initial"] = editor_field(label="Textarea initial")
        self.fields["textarea_filled"] = editor_field(
            label="Textarea filled",
            initial="<p>Foo <b>bar</b> pew.</p>",
        )

    def save(self):
        return {
            "textarea_empty": self.cleaned_data["textarea_empty"],
            "textarea_initial": self.cleaned_data["textarea_initial"],
            "textarea_filled": self.cleaned_data["textarea_filled"],
        }


class EditorSampleView(FormView):
    """
    A form view to check form render and behaviors with one of the available editor
    definitions.
    """
    template_name = "demo/editor_sample.html"
    form_class = SampleForm

    def get_editor(self, *args, **kwargs):
        if kwargs.get("editor_name", None) not in settings.EDITORS:
            raise Http404("Given editor name is not registered")

        return settings.EDITORS.get(kwargs["editor_name"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs.update({"editor": self.editor_definition})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["editor_definition"] = self.editor_definition
        context["payload"] = self.payload

        return context

    def form_valid(self, form):
        self.payload = form.save()
        return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        self.payload = None
        self.editor_definition = self.get_editor(*args, **kwargs)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.payload = None
        self.editor_definition = self.get_editor(*args, **kwargs)

        return super().post(request, *args, **kwargs)
