.. _install_intro:

=======
Install
=======

Install package in your environment : ::

    pip install django-editors

For development usage see :ref:`development_install`.


Configuration
*************

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        "django_editors",
    )

Then load default application settings in your settings file: ::

    from django_editors.settings import *

Then mount applications URLs: ::

    urlpatterns = [
        ...
        path("", include("django_editors.urls")),
    ]

There is not migration to apply because this application does not provide any model.


Settings
********

.. automodule:: django_editors.settings
   :members:
