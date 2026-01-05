from django import forms
from django.conf import settings


class DjangoBaseEditorWidget(forms.Textarea):
    """
    Base form widget for an editor.

    TODO: Rename 'editor_metadata' to 'editor' everywhere.
    TODO: Rename 'embed_editor_init' to 'editor_init' everywhere.

    Keyword Arguments:
        editor_metadata (RichEditorRuler): Rich editor definition instance. Although
            it is a keyword argument, this is a required argument however inheriter
            can define an attribute ``editor_metadata`` to avoid giving this argument.
        embed_editor_init (boolean): If true the widget render will include the
            editor Javascript component init just below the input. Else the editor
            component won't be automatically initialized and developer will have to do
            it himself.
    """
    template_name = "django_editors/widget.html"

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "editor_metadata"):
            self.editor_metadata = kwargs.pop("editor_metadata", None)

        if not self.editor_metadata:
            raise ValueError(
                "DjangoBaseEditorWidget requires 'editor_metadata' to be set."
            )

        self.embed_editor_init = kwargs.pop("embed_editor_init", True)

        super().__init__(*args, **kwargs)

    @property
    def media(self):
        return forms.Media(**self.editor_metadata.get_assets())

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        # Widget allways need an id to be able to set CodeMirror Javascript
        # config
        if "id" not in context["widget"]["attrs"]:
            context["widget"]["attrs"]["id"] = "id_{}".format(name)

        context["widget"]["editor"] = self.editor_metadata
        context["widget"]["editor_init"] = self.embed_editor_init

        ## Append HTML for CodeMirror Javascript config just below the textarea
        #if self.embed_config:
            #context["widget"].update({
                #"script": self.codemirror_script(context["widget"]["attrs"]["id"]),
            #})

        return context


class TipTapWidget(DjangoBaseEditorWidget):
    """
    TipTap form widget.

    Keyword Arguments:
        editor_metadata (RichEditorRuler): Rich editor definition instance. This will
            overwrite the default SunEditor editor definition. Default value use the
            TipTap definition from ``settings.EDITORS``
    """
    def __init__(self, *args, **kwargs):
        self.editor_metadata = kwargs.pop(
            "editor_metadata",
            settings.EDITORS["TipTap"]
        )

        super().__init__(*args, **kwargs)


class SunEditorWidget(DjangoBaseEditorWidget):
    """
    SunEditor form widget.

    Keyword Arguments:
        editor_metadata (RichEditorRuler): Rich editor definition instance. This will
            overwrite the default SunEditor editor definition. Default value use the
            TipTap definition from ``settings.EDITORS``
    """
    def __init__(self, *args, **kwargs):
        self.editor_metadata = kwargs.pop(
            "editor_metadata",
            settings.EDITORS["SunEditor"]
        )

        super().__init__(*args, **kwargs)
