from django import forms

from django_editors.formfields import SunEditorField
from django_editors.utils.tests import html_element


def test_concrete_field(settings):
    """
    Building a form field with concrete field class.
    """
    # Without editor init
    class DummyForm(forms.Form):
        field = SunEditorField(label="Rich text", init_editor=False)

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "</div>"
    )

    assert html_element(str(form.media)) == html_element(
        "<link href=\"/static/js/suneditor.min.css\" media=\"all\" rel=\"stylesheet\">"
        "<script src=\"/static/js/bundle-suneditor.js\">"
    )

    # Again with editor init and options
    class DummyForm(forms.Form):
        field = SunEditorField(
            label="Rich text",
            init_editor=True,
            editor_options={"dummy": ["pip", "pop"], "ping": None},
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoSunEditor({"
        " \"source\": document.querySelector(\"#id_field\"),"
        " \"editor_options\": {\"dummy\": [\"pip\", \"pop\"], \"ping\": null},"
        " \"wrapper_options\": {\"sync\": true},"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )
