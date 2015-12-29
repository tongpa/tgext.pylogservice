About tgext.pylogservice
-------------------------

tgext.pylogservice is a TurboGears2 extension

Installing
-------------------------------

tgext.pylogservice can be installed from pypi::

    pip install tgext.pylogservice

should just work for most of the users.

Enabling
-------------------------------

To enable tgext.pylogservice put inside your application
``config/app_cfg.py`` the following::

    import tgext.pylogservice
    tgext.pylogservice.plugme(base_config)

or you can use ``tgext.pluggable`` when available::

    from tgext.pluggable import plug
    plug(base_config, 'tgext.pylogservice')
