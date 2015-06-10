.. image:: https://badge.fury.io/py/betfair.py.png
    :target: http://badge.fury.io/py/betfair.py

.. image:: https://travis-ci.org/jmcarp/betfair.py.png?branch=master
    :target: https://travis-ci.org/jmcarp/betfair.py

betfair.py is a Python wrapper for the Betfair API

Installation
------------

::

    $ pip install betfair.py

Requirements
------------

- Python >= 2.7 or >= 3.3

Testing
-------

To run tests ::

    $ py.test

Application Keys
----------------

You will need an Application Key to log in to the Betfair API. You can find
instructions for creating a key at https://api.developer.betfair.com/services/webapps/docs/display/1smk3cen4v3lu3yomq5qye0ni/Application+Keys

SSL Certificates
----------------

For non-interactive login, you must generate a self-signed SSL certificate
and upload it to your Betfair account. Betfair.py includes tools for
simplifying this process. To create a self-signed certificate, run ::

    invoke ssl

This will generate the following files in the ``certs`` directory ::

    betfair.crt
    betfair.csr
    betfair.key
    betfair.pem

You can write SSL certificates to another directory by passing the
``--name`` parameter ::

    invoke ssl --name=path/to/certs/betfair

Once you have generated the files, you can upload the ``betfair.crt`` file to
Betfair at https://myaccount.betfair.com/accountdetails/mysecurity?showAPI=1.

Examples
--------

Create a Betfair client and log in ::

    from betfair import Betfair
    client = Betfair('app_key', 'certs/betfair.pem')
    client.login('username', 'password')

Refresh session token ::

    client.keep_alive()

Log out ::

    client.logout()

List all tennis markets ::

    from betfair.models import MarketFilter
    event_types = client.list_event_types(
        MarketFilter(text_query='tennis')
    )
    print(len(event_types))                 # 2
    print(event_types[0].event_type.name)   # 'Tennis'
    tennis_event_type = event_types[0]
    markets = client.list_market_catalogue(
        MarketFilter(event_type_ids=[tennis_event_type.event_type.id])
    )
    markets[0].market_name                  # 'Djokovic Tournament Wins'

Author
------

Joshua Carp (jmcarp)

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/jmcarp/betfair.py/blob/master/LICENSE>`_ file for more details
