from django import forms
from django.conf import settings


class DjangoBaseEditorWidget(forms.Textarea):
    """
    Base form widget for an editor.

    Keyword Arguments:
        editor (RichEditorDefinition): Rich editor definition instance. Although
            it is a keyword argument, this is a required argument however inheriter
            can define an attribute ``editor`` to avoid giving this argument.
        editor_init (boolean): If true the widget render will include the
            editor Javascript component init just below the input. Else the editor
            component won't be automatically initialized and developer will have to do
            it himself.
    """
    template_name = "django_editors/widget.html"

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "editor"):
            self.editor = kwargs.pop("editor", None)

        if not self.editor:
            raise ValueError(
                "DjangoBaseEditorWidget requires 'editor' to be set."
            )

        self.editor_init = kwargs.pop("editor_init", True)

        super().__init__(*args, **kwargs)

    @property
    def media(self):
        return forms.Media(**self.editor.get_assets())

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        # Widget allways need an id to be able to set CodeMirror Javascript
        # config
        if "id" not in context["widget"]["attrs"]:
            context["widget"]["attrs"]["id"] = "id_{}".format(name)

        context["widget"]["editor"] = self.editor
        context["widget"]["editor_init"] = self.editor_init

        return context


class TipTapWidget(DjangoBaseEditorWidget):
    """
    TipTap form widget.

    Keyword Arguments:
        editor (RichEditorDefinition): Rich editor definition instance. This will
            overwrite the default SunEditor editor definition. Default value use the
            TipTap definition from ``settings.EDITORS``
    """
    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop(
            "editor",
            settings.EDITORS["TipTap"]
        )

        super().__init__(*args, **kwargs)


class SunEditorWidget(DjangoBaseEditorWidget):
    """
    SunEditor form widget.

    Keyword Arguments:
        editor (RichEditorDefinition): Rich editor definition instance. This will
            overwrite the default SunEditor editor definition. Default value use the
            TipTap definition from ``settings.EDITORS``
    """
    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop(
            "editor",
            settings.EDITORS["SunEditor"]
        )

        super().__init__(*args, **kwargs)
