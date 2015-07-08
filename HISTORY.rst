.. :changelog:

History
-------

0.2.2
++++++++++++++++++
* Fix URL construction. Thanks petedmarsh.

0.2.1
++++++++++++++++++
* Add accounts endpoints. Thanks joelpob.
* Speed up field inflection. Thanks petedmarsh.
* Add custom timeout. Thanks ms5.
* Update fields. Thanks ms5.

0.2.0
++++++++++++++++++
* Replace homegrown models with Schematics.
* Use custom JSON encoder to handle JSON-unsafe types. Thanks kwassmuss for the patch.
* Fix typos in models and constants. Thanks kwassmuss and petedmarsh.
* Fix pip install. Thanks petedmarsh.
* Add various helpers for working with Betfair prices. Thanks petedmarsh.
* Add `NotLoggedIn` exception. Thanks ms5.

0.1.4
++++++++++++++++++
* Various fixes to `README.rst`. Thanks dmitryTsatsarin, skolsuper, goetzk, and petedmarsh.
* Remove requirement parsing from `setup.py`. Thanks skolsuper, scotontheedge, seriousdude, and verganis.
* Fix typos in `StartingPrices` model. Thanks petedmarsh.
* Allow empty `filter` arguments. Thanks petedmarsh.
* Handle Australian and Italian exchanges. Thanks goetzk.
* Fix SSL certificate generation. Thanks goetzk.
* Add linting with flake8.
