import json

from django import forms
from django.conf import settings


class DjangoBaseEditorWidget(forms.Textarea):
    """
    Base form widget for an editor.

    Attributes:
        editor (RichEditorDefinition): Required Rich editor definition instance. Either
            your concrete base editor class define this attribute or it will have to
            give a value from argument.
        editor_init (boolean): If true the widget render will include the
            Javascript code to initialize editor (just below the input in default
            widget template). If disabled the editor component won't be automatically
            initialized and developer will have to do it himself.
        editor_options (dict): The options to pass to Javascript editor constructor.
            This will be converted to JSON if not empty else widget context will have
            an empty string.
        wrapper_options (dict): The options to pass to editor wrapper (commonly a
            concrete implementation of ``modules.base_editor.DjangoBaseEditor`` (from
            frontend JavaScript). This will be converted to JSON if not empty else
            widget context will have an empty string.

    Keyword Arguments:
        editor (RichEditorDefinition): To overwrite the homonym attribute value.
        editor_init (boolean): To overwrite the homonym attribute value.
        editor_options (dict): To overwrite the homonym attribute value.
        wrapper_options (dict): To overwrite the homonym attribute value.
    """
    template_name = "django_editors/widget.html"

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop("editor", getattr(self, "editor", None))
        self.editor_init = kwargs.pop("editor_init", getattr(self, "editor_init", True))
        self.editor_options = kwargs.pop(
            "editor_options",
            getattr(self, "editor_options", {})
        )
        self.wrapper_options = kwargs.pop(
            "wrapper_options",
            getattr(self, "wrapper_options", {})
        )

        if not self.editor:
            raise ValueError(
                "DjangoBaseEditorWidget requires 'editor' to be set."
            )

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
        context["widget"]["editor_options"] = (
            json.dumps(self.editor_options) if self.editor_options else ""
        )
        context["widget"]["wrapper_options"] = (
            json.dumps(self.wrapper_options) if self.wrapper_options else ""
        )

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
