=====
Usage
=====

To use Graphene JWT Auth in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'gjwt_auth.apps.GjwtAuthConfig',
        ...
    )

Add Graphene JWT Auth's URL patterns:

.. code-block:: python

    from gjwt_auth import urls as gjwt_auth_urls


    urlpatterns = [
        ...
        url(r'^', include(gjwt_auth_urls)),
        ...
    ]
