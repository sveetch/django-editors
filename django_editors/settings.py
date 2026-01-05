"""
Default application settings
----------------------------

These are the default settings you can override in your own project settings
right after the line which load the default app settings.

"""
from .editors import RichEditorRuler


EDITORS = {
    "TipTap": RichEditorRuler(
        name="TipTap",
        js=["js/bundle-tiptap.js"],
        widget="django_editors.widgets.TipTapWidget",
        formfield="django_editors.formfields.TipTapField",
    ),
    "SunEditor": RichEditorRuler(
        name="SunEditor",
        js=["js/bundle-suneditor.js"],
        css=["js/suneditor.min.css"],
        widget="django_editors.widgets.SunEditorWidget",
        formfield="django_editors.formfields.SunEditorField",
    ),
}
