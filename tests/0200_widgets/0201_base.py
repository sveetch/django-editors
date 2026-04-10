from django_editors.widgets import DjangoBaseEditorWidget
from django_editors.utils.tests import html_element
from django_editors.definitions import RichEditorDefinition


def test_basic(settings):
    """
    Build a TipTap widget in the raw way should render as expected.
    """
    widget = DjangoBaseEditorWidget(
        editor=RichEditorDefinition(
            name="Foobar",
            css=["css/bundle-foo.css"],
            js=["js/bundle-bar.js"],
        ),
        attrs={"foo": "bar"},
        init_editor=False,
    )

    # On default, just the widget input
    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" foo=\"bar\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
    )

    assert html_element(str(widget.media)) == html_element(
        "<link href=\"/static/css/bundle-foo.css\" media=\"all\" rel=\"stylesheet\">"
        "<script src=\"/static/js/bundle-bar.js\"></script>"
    )


def test_init_basic_conf(settings):
    """
    Build a widget with JavaScript initialization for editor without custom options.
    """
    widget = DjangoBaseEditorWidget(
        editor=RichEditorDefinition(
            name="Foobar",
            css=["css/bundle-foo.css"],
            js=["js/bundle-bar.js"],
        ),
        init_editor=True,
    )

    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
        "<script>"
        "let id_text = new DjangoFoobar({"
        " \"source\": document.querySelector(\"#id_text\"),"
        " \"classNames\": \"form-control\""
        " });"
        " id_text.provide();"
        " </script>"
    )


def test_editor_options_without_init(settings):
    """
    Build a widget with some option but without JavaScript initialization.
    """
    widget = DjangoBaseEditorWidget(
        editor=RichEditorDefinition(
            name="Foobar",
            css=["css/bundle-foo.css"],
            js=["js/bundle-bar.js"],
        ),
        init_editor=False,
        editor_options={"dummy": ["pip", "pop"], "ping": None},
    )
    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
    )


def test_editor_options_with_init(settings):
    """
    Build a widget with some options and with JavaScript initialization.
    """
    widget = DjangoBaseEditorWidget(
        editor=RichEditorDefinition(
            name="Foobar",
        ),
        init_editor=True,
        editor_options={
            "dummy": ["pip", "pop"],
            "ping": None,
        },
        widget_options={
            "attrs": {"required": ""},
        },
        wrapper_options={"ping": "pong"},
    )
    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" required rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
        "<script>"
        "let id_text = new DjangoFoobar({"
        " \"source\": document.querySelector(\"#id_text\"),"
        " \"editor_options\": {\"dummy\": [\"pip\", \"pop\"], \"ping\": null},"
        " \"wrapper_options\": {\"ping\": \"pong\"},"
        " \"classNames\": \"form-control\""
        " });"
        " id_text.provide();"
        " </script>"
    )
