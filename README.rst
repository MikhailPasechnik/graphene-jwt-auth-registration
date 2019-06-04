=============================
Graphene JWT Auth
=============================

.. image:: https://badge.fury.io/py/graphene-jwt-auth.svg
    :target: https://badge.fury.io/py/graphene-jwt-auth

.. image:: https://travis-ci.org/fivethreeo/graphene-jwt-auth.svg?branch=master
    :target: https://travis-ci.org/fivethreeo/graphene-jwt-auth

.. image:: https://codecov.io/gh/fivethreeo/graphene-jwt-auth/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/fivethreeo/graphene-jwt-auth

Authentication using graphene and JWT 

Documentation
-------------

The full documentation is at https://graphene-jwt-auth.readthedocs.io.

Quickstart
----------

Install Graphene JWT Auth::

    pip install graphene-jwt-auth

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
