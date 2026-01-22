from django import forms

from django_editors.widgets import DjangoBaseEditorWidget
from django_editors.formfields import DjangoBaseEditorField, TipTapField
from django_editors.utils.tests import html_element


def test_base(settings):
    """
    Build a TipTap form field in the raw way should render as expected.
    """
    class DummyForm(forms.Form):
        field = forms.CharField(
            label="Rich text",
            widget=DjangoBaseEditorWidget(editor=settings.EDITORS["TipTap"])
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoTipTap({"
        " \"source\": document.querySelector('#id_field'),"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )


def test_from_ruler(settings):
    """
    TipTap field render and form media assets should be as expected.
    """
    class DummyForm(forms.Form):
        field = forms.CharField(
            label="Rich text",
            widget=settings.EDITORS["TipTap"].get_widget_class()
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoTipTap({"
        " \"source\": document.querySelector('#id_field'),"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )

    assert html_element(str(form.media)) == html_element(
        "<script src=\"/static/js/bundle-tiptap.js\"></script>"
    )

    # Again but setting widget within form initialization
    class DummyForm(forms.Form):
        field = forms.CharField(
            label="Rich text",
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields["field"].widget = settings.EDITORS["TipTap"].get_widget_object()

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoTipTap({"
        " \"source\": document.querySelector('#id_field'),"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )

    assert html_element(str(form.media)) == html_element(
        "<script src=\"/static/js/bundle-tiptap.js\"></script>"
    )


def test_base_field(settings):
    """
    Build a form field with DjangoBaseEditorField
    """
    class DummyForm(forms.Form):
        field = DjangoBaseEditorField(
            label="Rich text",
            editor=settings.EDITORS["TipTap"],
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoTipTap({"
        " \"source\": document.querySelector('#id_field'),"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )

    assert html_element(str(form.media)) == html_element(
        "<script src=\"/static/js/bundle-tiptap.js\"></script>"
    )


def test_field_tiptap_default(settings):
    """
    TODO
    """
    class DummyForm(forms.Form):
        field = TipTapField(label="Rich text")

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoTipTap({"
        " \"source\": document.querySelector('#id_field'),"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )

    assert html_element(str(form.media)) == html_element(
        "<script src=\"/static/js/bundle-tiptap.js\"></script>"
    )


def test_field_tiptap_custom(settings):
    """
    TODO
    """
    class DummyForm(forms.Form):
        field = TipTapField(label="Rich text")

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoTipTap({"
        " \"source\": document.querySelector('#id_field'),"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )

    assert html_element(str(form.media)) == html_element(
        "<script src=\"/static/js/bundle-tiptap.js\"></script>"
    )
