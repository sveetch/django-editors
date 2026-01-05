from django import forms
from django.conf import settings

from .widgets import DjangoBaseEditorWidget


class DjangoBaseEditorField(forms.CharField):
    """
    A CharField that is able to find its widget from given editor definition.

    Keyword Arguments:
        editor_metadata (RichEditorRuler): Rich editor definition instance. Although
            it is a keyword argument, this is a required argument however inheriter
            can define an attribute ``editor_metadata`` to avoid giving this argument.
        editor_options (dict):
        editor_init (boolean): TODO: Receive, pop and pass it to widget
    """
    def __init__(self, *args, **kwargs):
        if not hasattr(self, "editor_metadata"):
            self.editor_metadata = kwargs.pop("editor_metadata", None)

        if not self.editor_metadata:
            raise ValueError(
                "DjangoBaseEditorField requires 'editor_metadata' to be set."
            )

        if not hasattr(self, "editor_options"):
            self.editor_options = kwargs.pop("editor_options", {})

        # Add widget to the field
        kwargs.update({
            "widget": self.editor_metadata.get_widget_object(**self.editor_options)
        })

        super().__init__(*args, **kwargs)


class TipTapField(DjangoBaseEditorField):
    """
    TipTap form field.

    Keyword Arguments:
        editor_metadata (RichEditorRuler): Rich editor definition instance. This will
            overwrite the default SunEditor editor definition. Default value use the
            TipTap definition from ``settings.EDITORS``
        editor_options (dict):
        editor_init (boolean):
    """
    def __init__(self, *args, **kwargs):
        self.editor_metadata = kwargs.pop(
            "editor_metadata",
            settings.EDITORS["TipTap"]
        )

        super().__init__(*args, **kwargs)


class SunEditorField(DjangoBaseEditorField):
    """
    SunEditor form field.

    Keyword Arguments:
        editor_metadata (RichEditorRuler): Rich editor definition instance. This will
            overwrite the default SunEditor editor definition. Default value use the
            SunEditor definition from ``settings.EDITORS``
        editor_options (dict):
        editor_init (boolean):
    """
    def __init__(self, *args, **kwargs):
        self.editor_metadata = kwargs.pop(
            "editor_metadata",
            settings.EDITORS["SunEditor"]
        )

        super().__init__(*args, **kwargs)
