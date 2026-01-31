from django_editors.widgets import DjangoBaseEditorWidget
from django_editors.utils.tests import html_element
from django_editors.editors import RichEditorDefinition


def test_base(settings):
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
        editor_init=False,
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


def test_base_init(settings):
    """
    Build a widget with JavaScript initialization for editor.
    """
    widget = DjangoBaseEditorWidget(
        editor=RichEditorDefinition(
            name="Foobar",
            css=["css/bundle-foo.css"],
            js=["js/bundle-bar.js"],
        ),
        editor_init=True,
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


def test_base_editor_options(settings):
    """
    Build a widget with JavaScript initialization for editor.
    """
    # Without init
    widget = DjangoBaseEditorWidget(
        editor=RichEditorDefinition(
            name="Foobar",
            css=["css/bundle-foo.css"],
            js=["js/bundle-bar.js"],
        ),
        editor_init=False,
        editor_options={"dummy": ["pip", "pop"], "ping": None},
    )
    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
    )

    # With init
    widget = DjangoBaseEditorWidget(
        editor=RichEditorDefinition(
            name="Foobar",
            css=["css/bundle-foo.css"],
            js=["js/bundle-bar.js"],
        ),
        editor_init=True,
        editor_options={"dummy": ["pip", "pop"], "ping": None},
    )
    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
        "<script>"
        "let id_text = new DjangoFoobar({"
        " \"source\": document.querySelector(\"#id_text\"),"
        " \"editor_options\": {\"dummy\": [\"pip\", \"pop\"], \"ping\": null},"
        " \"classNames\": \"form-control\""
        " });"
        " id_text.provide();"
        " </script>"
    )


def test_widget_tiptap(settings):
    """
    TipTap widget render and media assets should be as expected.
    """
    definition = settings.EDITORS["TipTap"]
    widget = definition.get_widget_object(editor_init=False)

    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
    )

    widget = definition.get_widget_object(
        editor_init=True,
        editor_options={"dummy": ["pip", "pop"], "ping": None},
    )
    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
        "<script>"
        "let id_text = new DjangoTipTap({"
        " \"source\": document.querySelector(\"#id_text\"),"
        " \"editor_options\": {\"dummy\": [\"pip\", \"pop\"], \"ping\": null},"
        " \"classNames\": \"form-control\""
        " });"
        " id_text.provide();"
        " </script>"
    )

    assert html_element(str(widget.media)) == html_element(
        "<script src=\"/static/js/bundle-tiptap.js\"></script>"
    )


def test_widget_suneditor(settings):
    """
    SunEditor widget render and media assets should be as expected.
    """
    definition = settings.EDITORS["SunEditor"]
    widget = definition.get_widget_object(editor_init=False)

    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
    )

    widget = definition.get_widget_object(editor_init=True)
    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
        "<script>"
        "let id_text = new DjangoSunEditor({"
        " \"source\": document.querySelector(\"#id_text\"),"
        " \"classNames\": \"form-control\""
        " });"
        " id_text.provide();"
        " </script>"
    )

    assert html_element(str(widget.media)) == html_element(
        "<link href=\"/static/js/suneditor.min.css\" media=\"all\" rel=\"stylesheet\">"
        "<script src=\"/static/js/bundle-suneditor.js\">"
    )
