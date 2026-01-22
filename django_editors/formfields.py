from django import forms
from django.conf import settings


class DjangoBaseEditorField(forms.CharField):
    """
    A CharField that is able to find its widget from given editor definition.

    Keyword Arguments:
        editor (RichEditorDefinition): Rich editor definition instance. Although
            it is a keyword argument, this is a required argument however inheriter
            can define an attribute ``editor`` to avoid giving this argument.
        editor_options (dict):
        editor_init (boolean): TODO: Receive, pop and pass it to widget
    """
    def __init__(self, *args, **kwargs):
        if not hasattr(self, "editor"):
            self.editor = kwargs.pop("editor", None)

        if not self.editor:
            raise ValueError(
                "DjangoBaseEditorField requires 'editor' to be set."
            )

        if not hasattr(self, "editor_options"):
            self.editor_options = kwargs.pop("editor_options", {})

        # Add widget to the field
        kwargs.update({
            "widget": self.editor.get_widget_object(**self.editor_options)
        })

        super().__init__(*args, **kwargs)


class TipTapField(DjangoBaseEditorField):
    """
    TipTap form field.

    Keyword Arguments:
        editor (RichEditorDefinition): Rich editor definition instance. This will
            overwrite the default SunEditor editor definition. Default value use the
            TipTap definition from ``settings.EDITORS``
        editor_options (dict):
        editor_init (boolean):
    """
    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop(
            "editor",
            settings.EDITORS["TipTap"]
        )

        super().__init__(*args, **kwargs)


class SunEditorField(DjangoBaseEditorField):
    """
    SunEditor form field.

    Keyword Arguments:
        editor (RichEditorDefinition): Rich editor definition instance. This will
            overwrite the default SunEditor editor definition. Default value use the
            SunEditor definition from ``settings.EDITORS``
        editor_options (dict):
        editor_init (boolean):
    """
    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop(
            "editor",
            settings.EDITORS["SunEditor"]
        )

        super().__init__(*args, **kwargs)
