from django import forms
from django.conf import settings


class DjangoBaseEditorField(forms.CharField):
    """
    A CharField that is able to find its widget from given editor definition.

    Attributes:
        editor (RichEditorDefinition): Required Rich editor definition instance. Either
            your concrete base editor class define this attribute or it will have to
            give a value from argument.
        init_editor (boolean): If true the widget render will include the
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
        init_editor (boolean): To overwrite the homonym attribute value.
        editor_options (dict): To overwrite the homonym attribute value.
        wrapper_options (dict): To overwrite the homonym attribute value.
    """
    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop("editor", getattr(self, "editor", None))
        self.init_editor = kwargs.pop("init_editor", getattr(self, "init_editor", True))
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
                "DjangoBaseEditorField requires 'editor' to be set."
            )

        # Add widget to the field
        kwargs.update({
            "widget": self.editor.get_widget_object(
                editor=self.editor,
                editor_options=self.editor_options,
                init_editor=self.init_editor,
                wrapper_options=self.wrapper_options,
            )
        })

        super().__init__(*args, **kwargs)


class TipTapField(DjangoBaseEditorField):
    """
    TipTap form field.

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


class SunEditorField(DjangoBaseEditorField):
    """
    SunEditor form field.

    Keyword Arguments:
        editor (RichEditorDefinition): Rich editor definition instance. This will
            overwrite the default SunEditor editor definition. Default value use the
            SunEditor definition from ``settings.EDITORS``
    """
    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop(
            "editor",
            settings.EDITORS["SunEditor"]
        )

        super().__init__(*args, **kwargs)


class CodeMirror6Field(DjangoBaseEditorField):
    """
    CodeMirror 6 form field.

    Keyword Arguments:
        editor (RichEditorDefinition): Rich editor definition instance. This will
            overwrite the default CodeMirror editor definition. Default value use the
            CodeMirror6 definition from ``settings.EDITORS``
    """
    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop(
            "editor",
            settings.EDITORS["CodeMirror6"]
        )

        super().__init__(*args, **kwargs)
