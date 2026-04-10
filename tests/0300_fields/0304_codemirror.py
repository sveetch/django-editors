from django import forms

from django_editors.formfields import CodeMirror6Field
from django_editors.utils.tests import html_element


def test_concrete_field(settings):
    """
    Building a form field with concrete field class.
    """
    # Without editor init
    class DummyForm(forms.Form):
        field = CodeMirror6Field(label="Rich text", init_editor=False)

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "</div>"
    )

    assert html_element(str(form.media)) == html_element(
        "<script src=\"/static/js/bundle-codemirror.js\">"
    )

    # Again with editor init and options
    class DummyForm(forms.Form):
        field = CodeMirror6Field(
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
        "let id_field = new DjangoCodeMirror6({"
        " \"source\": document.querySelector(\"#id_field\"),"
        " \"editor_options\": {\"dummy\": [\"pip\", \"pop\"], \"ping\": null},"
        " \"wrapper_options\": {\"sync\": true},"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )
