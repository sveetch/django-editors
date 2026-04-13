"""
Default application settings
----------------------------

These are the default settings you can override in your own project settings
right after the line which load the default app settings.

"""
from .definitions import RichEditorDefinition


EDITORS = {
    "TipTap": RichEditorDefinition(
        name="TipTap",
        js=["js/bundle-tiptap.js"],
        widget="django_editors.widgets.TipTapWidget",
        formfield="django_editors.formfields.TipTapField",
        wrapper_options={"sync": True},
    ),
    "SunEditor": RichEditorDefinition(
        name="SunEditor",
        js=["js/bundle-suneditor.js"],
        css=["js/suneditor.min.css"],
        widget="django_editors.widgets.SunEditorWidget",
        formfield="django_editors.formfields.SunEditorField",
        editor_options={},
        wrapper_options={"sync": True},
    ),
    "CodeMirror6": RichEditorDefinition(
        name="CodeMirror6",
        js=["js/bundle-codemirror.js"],
        widget="django_editors.widgets.CodeMirror6Widget",
        formfield="django_editors.formfields.CodeMirror6Field",
        wrapper_options={
            "sync": True,
            # Possible extensions (must be implemented in editor wrapper)
            "allowed_extensions": [
                "css",
                "html",
                "javascript",
                "jinja",
                "python"
                "sass",
            ],
            # Enabled language extension
            "lang_extension": "html",
        },
    ),
}
