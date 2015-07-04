# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import json
import itertools
import collections

import requests
from six.moves import http_client as httplib
from six.moves import urllib_parse as urllib

from betfair import utils
from betfair import models
from betfair import exceptions


IDENTITY_URLS = collections.defaultdict(
    lambda: 'https://identitysso.betfair.com/api/',
    italy='https://identitysso.betfair.it/api/',
)

API_URLS = collections.defaultdict(
    lambda: 'https://api.betfair.com/exchange/betting/json-rpc/v1',
    australia='https://api-au.betfair.com/exchange/betting/json-rpc/v1',
)


class Betfair(object):
    """Betfair API client.

    :param str app_key: Optional application identifier
    :param str cert_file: Path to self-signed SSL certificate file(s); may be
        a *.pem file or a tuple of (*.crt, *.key) files
    :param str content_type: Optional content type
    :param str locale: Optional location ("australia", "italy", etc.)
    :param Session session: Optional Requests session
    :param int timeout: Optional timeout duration (seconds)
    """
    def __init__(self, app_key, cert_file, content_type='application/json', locale=None,
                 session=None, timeout=None):
        self.app_key = app_key
        self.cert_file = cert_file
        self.content_type = content_type
        self.locale = locale
        self.session = session or requests.Session()
        self.session_token = None
        self.timeout = timeout

    @property
    def identity_url(self):
        return IDENTITY_URLS[self.locale]

    @property
    def api_url(self):
        return API_URLS[self.locale]

    @property
    def headers(self):
        return {
            'X-Application': self.app_key,
            'X-Authentication': self.session_token,
            'Content-Type': self.content_type,
            'Accept': 'application/json',
        }

    def make_auth_request(self, method):
        response = self.session.post(
            os.path.join(self.identity_url, method),
            headers=self.headers,
            timeout=self.timeout,
        )
        utils.check_status_code(response)
        data = response.json()
        if data.get('status') != 'SUCCESS':
            raise exceptions.AuthError(response, data)

    def make_api_request(self, base, method, params, codes=None, model=None):
        payload = utils.make_payload(base, method, params)
        response = self.session.post(
            self.api_url,
            data=json.dumps(payload, cls=utils.BetfairEncoder),
            headers=self.headers,
            timeout=self.timeout,
        )
        utils.check_status_code(response, codes=codes)
        result = utils.result_or_error(response)
        return utils.process_result(result, model)

    # Authentication methods

    def login(self, username, password):
        """Log in to Betfair. Sets `session_token` if successful.

        :param str username: Username
        :param str password: Password
        :raises: BetfairLoginError
        """
        response = self.session.post(
            os.path.join(self.identity_url, 'certlogin'),
            cert=self.cert_file,
            data=urllib.urlencode({
                'username': username,
                'password': password,
            }),
            headers={
                'X-Application': self.app_key,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            timeout=self.timeout,
        )
        utils.check_status_code(response, [httplib.OK])
        data = response.json()
        if data.get('loginStatus') != 'SUCCESS':
            raise exceptions.LoginError(response, data)
        self.session_token = data['sessionToken']

    @utils.requires_login
    def keep_alive(self):
        """Reset session timeout.

        :raises: AuthError
        """
        self.make_auth_request('keepAlive')

    @utils.requires_login
    def logout(self):
        """Log out and clear `session_token`.

        :raises: AuthError
        """
        self.make_auth_request('logout')
        self.session_token = None

    # Bet query methods

    @utils.requires_login
    def list_event_types(self, filter=None, locale=None):
        """

        :param MarketFilter filter:
        :param str locale:
        """
        filter = filter or models.MarketFilter()
        return self.make_api_request(
            'Sports',
            'listEventTypes',
            utils.get_kwargs(locals()),
            model=models.EventTypeResult,
        )

    @utils.requires_login
    def list_competitions(self, filter=None, locale=None):
        """

        :param MarketFilter filter:
        :param str locale:
        """
        filter = filter or models.MarketFilter()
        return self.make_api_request(
            'Sports',
            'listCompetitions',
            utils.get_kwargs(locals()),
            model=models.CompetitionResult,
        )

    @utils.requires_login
    def list_time_ranges(self, granularity, filter=None):
        """

        :param TimeGranularity granularity:
        :param MarketFilter filter:
        """
        filter = filter or models.MarketFilter()
        return self.make_api_request(
            'Sports',
            'listTimeRanges',
            utils.get_kwargs(locals()),
            model=models.TimeRangeResult,
        )

    @utils.requires_login
    def list_events(self, filter=None, locale=None):
        """

        :param MarketFilter filter:
        :param str locale:
        """
        filter = filter or models.MarketFilter()
        return self.make_api_request(
            'Sports',
            'listEvents',
            utils.get_kwargs(locals()),
            model=models.EventResult,
        )

    @utils.requires_login
    def list_market_types(self, filter=None, locale=None):
        """

        :param MarketFilter filter:
        :param str locale:
        """
        filter = filter or models.MarketFilter()
        return self.make_api_request(
            'Sports',
            'listMarketTypes',
            utils.get_kwargs(locals()),
            model=models.MarketTypeResult,
        )

    @utils.requires_login
    def list_countries(self, filter=None, locale=None):
        """

        :param MarketFilter filter:
        :param str locale:
        """
        filter = filter or models.MarketFilter()
        return self.make_api_request(
            'Sports',
            'listCountries',
            utils.get_kwargs(locals()),
            model=models.CountryCodeResult,
        )

    @utils.requires_login
    def list_venues(self, filter=None, locale=None):
        """

        :param MarketFilter filter:
        :param str locale:
        """
        filter = filter or models.MarketFilter()
        return self.make_api_request(
            'Sports',
            'listCountries',
            utils.get_kwargs(locals()),
            model=models.VenueResult,
        )

    @utils.requires_login
    def list_market_catalogue(
            self, filter=None, max_results=100, market_projection=None, locale=None,
            sort=None):
        """

        :param MarketFilter filter:
        :param int max_results:
        :param list market_projection:
        :param MarketSort sort:
        :param str locale:
        """
        filter = filter or models.MarketFilter()
        return self.make_api_request(
            'Sports',
            'listMarketCatalogue',
            utils.get_kwargs(locals()),
            model=models.MarketCatalogue,
        )

    @utils.requires_login
    def list_market_book(
            self, market_ids, price_projection=None, order_projection=None,
            match_projection=None, currency_code=None, locale=None):
        """

        :param list market_ids: List of market IDs
        :param PriceProjection price_projection:
        :param OrderProjection order_projection:
        :param MatchProjection match_projection:
        :param str currency_code:
        :param str locale:
        """
        return self.make_api_request(
            'Sports',
            'listMarketBook',
            utils.get_kwargs(locals()),
            model=models.MarketBook,
        )

    @utils.requires_login
    def list_market_profit_and_loss(
            self, market_ids, include_settled_bets=False,
            include_bsp_bets=None, net_of_commission=None):
        """Retrieve profit and loss for a given list of markets.

        :param list market_ids: List of markets to calculate profit and loss
        :param bool include_settled_bets: Option to include settled bets
        :param bool include_bsp_bets: Option to include BSP bets
        :param bool net_of_commission: Option to return profit and loss net of
            users current commission rate for this market including any special
            tariffs
        """
        return self.make_api_request(
            'Sports',
            'listMarketProfitAndLoss',
            utils.get_kwargs(locals()),
            model=models.MarketProfitAndLoss,
        )

    # Chunked iterators for list methods

    def iter_list_market_book(self, market_ids, chunk_size, **kwargs):
        """Split call to `list_market_book` into separate requests.

        :param list market_ids: List of market IDs
        :param int chunk_size: Number of records per chunk
        :param dict kwargs: Arguments passed to `list_market_book`
        """
        return itertools.chain(*(
            self.list_market_book(market_chunk, **kwargs)
            for market_chunk in utils.get_chunks(market_ids, chunk_size)
        ))

    def iter_list_market_profit_and_loss(
            self, market_ids, chunk_size, **kwargs):
        """Split call to `list_market_profit_and_loss` into separate requests.

        :param list market_ids: List of market IDs
        :param int chunk_size: Number of records per chunk
        :param dict kwargs: Arguments passed to `list_market_profit_and_loss`
        """
        return itertools.chain(*(
            self.list_market_profit_and_loss(market_chunk, **kwargs)
            for market_chunk in utils.get_chunks(market_ids, chunk_size)
        ))

    # Betting methods

    @utils.requires_login
    def list_current_orders(
            self, bet_ids=None, market_ids=None, order_projection=None,
            date_range=None, order_by=None, sort_dir=None, from_record=None,
            record_count=None):
        """

        :param bet_ids:
        :param market_ids:
        :param order_projection:
        :param date_range:
        :param order_by:
        :param sort_dir:
        :param from_record:
        :param record_count:
        """
        return self.make_api_request(
            'Sports',
            'listCurrentOrders',
            utils.get_kwargs(locals()),
            model=models.CurrentOrderSummaryReport,
        )

    @utils.requires_login
    def list_cleared_orders(
            self, bet_status, event_type_ids, event_ids, market_ids,
            runner_ids, bet_ids, side, settled_date_range, group_by,
            include_item_description, locale, from_record, record_count):
        """

        :param bet_status:
        :param event_type_ids:
        :param event_ids:
        :param market_ids:
        :param runner_ids:
        :param bet_ids:
        :param side:
        :param settled_date_range:
        :param group_by:
        :param include_item_description:
        :param locale:
        :param from_record:
        :param record_count:
        """
        return self.make_api_request(
            'Sports',
            'listClearedOrders',
            utils.get_kwargs(locals()),
            model=models.ClearedOrderSummaryReport,
        )

    @utils.requires_login
    def place_orders(self, market_id, instructions, customer_ref=None):
        """Place new orders into market. This operation is atomic in that all
        orders will be placed or none will be placed.

        :param str market_id: The market id these orders are to be placed on
        :param list instructions: List of `PlaceInstruction` objects
        :param str customer_ref: Optional order identifier string
        """
        return self.make_api_request(
            'Sports',
            'placeOrders',
            utils.get_kwargs(locals()),
            model=models.PlaceExecutionReport,
        )

    @utils.requires_login
    def cancel_orders(self, market_id, instructions, customer_ref=None):
        """Cancel all bets OR cancel all bets on a market OR fully or
        partially cancel particular orders on a market.

        :param str market_id: If not supplied all bets are cancelled
        :param list instructions: List of `CancelInstruction` objects
        :param str customer_ref: Optional order identifier string
        """
        return self.make_api_request(
            'Sports',
            'cancelOrders',
            utils.get_kwargs(locals()),
            model=models.CancelInstructionReport,
        )

    @utils.requires_login
    def replace_orders(self, market_id, instructions, customer_ref=None):
        """This operation is logically a bulk cancel followed by a bulk place.
        The cancel is completed first then the new orders are placed.

        :param str market_id: The market id these orders are to be placed on
        :param list instructions: List of `ReplaceInstruction` objects
        :param str customer_ref: Optional order identifier string
        """
        return self.make_api_request(
            'Sports',
            'replaceOrders',
            utils.get_kwargs(locals()),
            model=models.ReplaceExecutionReport,
        )

    @utils.requires_login
    def update_orders(self, market_id, instructions, customer_ref=None):
        """Update non-exposure changing fields.

        :param str market_id: The market id these orders are to be placed on
        :param list instructions: List of `UpdateInstruction` objects
        :param str customer_ref: Optional order identifier string
        """
        return self.make_api_request(
            'Sports',
            'updateOrders',
            utils.get_kwargs(locals()),
            model=models.UpdateExecutionReport,
        )

    @utils.requires_login
    def get_account_funds(self, wallet=None):
        """Get available to bet amount.

        :param Wallet wallet: Name of the wallet in question
        """
        result = self.make_api_request(
            'Account',
            'getAccountFunds',
            utils.get_kwargs(locals()),
            model=models.AccountFundsResponse,
        )

    @utils.requires_login
    def get_account_statement(
            self, locale=None, from_record=None, record_count=None,
            item_date_range=None, include_item=None, wallet=None):
        """Get account statement.

        :param str locale: The language to be used where applicable
        :param int from_record: Specifies the first record that will be returned
        :param int record_count: Specifies the maximum number of records to be returned
        :param TimeRange item_date_range: Return items with an itemDate within this date range
        :param IncludeItem include_item: Which items to include
        :param Wallet wallte: Which wallet to return statementItems for
        """
        result = self.make_api_request(
            'Account',
            'getAccountStatement',
            utils.get_kwargs(locals()),
            model=models.AccountStatementReport,
        )

    @utils.requires_login
    def get_account_details(self):
        """Returns the details relating your account, including your discount
        rate and Betfair point balance.
        """
        result = self.make_api_request(
            'Account',
            'getAccountDetails',
            utils.get_kwargs(locals()),
            model=models.AccountDetailsResponse,
        )

    @utils.requires_login
    def list_currency_rates(self, from_currency=None):
        """Returns a list of currency rates based on given currency

        :param str from_currency: The currency from which the rates are computed
        """
        result = self.make_api_request(
            'Account',
            'listCurrencyRates',
            utils.get_kwargs(locals()),
            model=models.CurrencyRate,
        )

    @utils.requires_login
    def transfer_funds(self, from_, to, amount):
        """Transfer funds between the UK Exchange and Australian Exchange wallets.

        :param Wallet from_: Source wallet
        :param Wallet to: Destination wallet
        :param float amount: Amount to transfer
        """
        result = self.make_api_request(
            'Account',
            'transferFunds',
            utils.get_kwargs(locals()),
            model=models.TransferResponse,
        )
