# -*- coding: utf-8 -*-

from __future__ import absolute_import

from schematics.types import IntType
from schematics.types import LongType
from schematics.types import FloatType
from schematics.types import StringType
from schematics.types import BooleanType
from schematics.types.compound import DictType
from schematics.types.compound import ListType
from schematics.types.compound import ModelType

from betfair.meta.types import EnumType
from betfair.meta.types import DateTimeType
from betfair.meta.models import BetfairModel

from betfair import constants


class Event(BetfairModel):
    id = StringType()
    name = StringType()
    country_code = StringType()
    timezone = StringType()
    venue = StringType()
    open_date = DateTimeType()


class MarketDescription(BetfairModel):
    persistence_enabled = BooleanType(required=True)
    bsp_market = BooleanType(required=True)
    market_time = DateTimeType(required=True)
    suspend_time = DateTimeType(required=True)
    settle_time = DateTimeType()
    betting_type = EnumType(constants.MarketBettingType, required=True)
    turn_in_play_enabled = BooleanType(required=True)
    market_type = StringType(required=True)
    regulator = StringType(required=True)
    market_base_rate = FloatType(required=True)
    discount_allowed = BooleanType(required=True)
    wallet = StringType()
    rules = StringType()
    rules_has_date = BooleanType()
    clarifications = StringType()
    each_way_divisor = FloatType()


class RunnerCatalog(BetfairModel):
    selection_id = IntType(required=True)
    runner_name = StringType(required=True)
    handicap = FloatType(required=True)
    sort_priority = IntType(required=True)
    metadata = DictType(StringType)


class EventType(BetfairModel):
    id = StringType()
    name = StringType()


class Competition(BetfairModel):
    id = StringType()
    name = StringType()


class MarketCatalogue(BetfairModel):
    market_id = StringType()
    market_name = StringType()
    market_start_time = DateTimeType()
    description = ModelType(MarketDescription)
    total_matched = FloatType()
    runners = ListType(ModelType(RunnerCatalog))
    event_type = ModelType(EventType)
    competition = ModelType(Competition)
    event = ModelType(Event)


class TimeRange(BetfairModel):
    from_ = DateTimeType(deserialize_from='from', serialized_name='from')
    to = DateTimeType()


class MarketFilter(BetfairModel):
    text_query = StringType()
    exchange_ids = StringType()
    event_type_ids = ListType(StringType)
    event_ids = ListType(StringType)
    competition_ids = ListType(StringType)
    market_ids = ListType(StringType)
    venues = ListType(StringType)
    bsp_only = BooleanType()
    turn_in_play_enabled = BooleanType()
    in_play_only = BooleanType()
    market_betting_types = ListType(EnumType(constants.MarketBettingType))
    market_countries = ListType(StringType)
    market_type_codes = ListType(StringType)
    market_start_time = ModelType(TimeRange)
    with_orders = ListType(EnumType(constants.OrderStatus))


class PriceSize(BetfairModel):
    price = FloatType(required=True)
    size = FloatType(required=True)


class StartingPrices(BetfairModel):
    near_price = FloatType()
    far_price = FloatType()
    back_stake_taken = ListType(ModelType(PriceSize))
    lay_liability_taken = ListType(ModelType(PriceSize))
    actual_SP = FloatType()


class ExchangePrices(BetfairModel):
    available_to_back = ListType(ModelType(PriceSize))
    available_to_lay = ListType(ModelType(PriceSize))
    traded_volume = ListType(ModelType(PriceSize))


class Order(BetfairModel):
    bet_id = StringType(required=True)
    order_type = EnumType(constants.OrderType, required=True)
    status = EnumType(constants.OrderStatus, required=True)
    persistence_type = EnumType(constants.PersistenceType, required=True)
    side = EnumType(constants.Side, required=True)
    price = FloatType(required=True)
    size = FloatType(required=True)
    bsp_liability = BooleanType(required=True)
    placed_date = DateTimeType(required=True)
    avg_price_matched = FloatType()
    size_matched = FloatType()
    size_remaining = FloatType()
    size_lapsed = FloatType()
    size_cancelled = FloatType()
    size_voided = FloatType()


class Match(BetfairModel):
    bet_id = StringType()
    match_id = StringType()
    side = EnumType(constants.Side, required=True)
    price = FloatType(required=True)
    size = FloatType(required=True)
    match_date = DateTimeType()


class Runner(BetfairModel):
    selection_id = IntType(required=True)
    handicap = FloatType(required=True)
    status = EnumType(constants.RunnerStatus, required=True)
    adjustment_factor = FloatType()
    last_price_traded = FloatType()
    total_matched = FloatType()
    removal_date = DateTimeType()
    sp = ModelType(StartingPrices)
    ex = ModelType(ExchangePrices)
    orders = ListType(ModelType(Order))
    matches = ListType(ModelType(Match))


class MarketBook(BetfairModel):
    market_id = StringType(required=True)
    is_market_data_delayed = BooleanType(required=True)
    status = EnumType(constants.MarketStatus)
    bet_delay = IntType()
    bsp_reconciled = BooleanType()
    complete = BooleanType()
    inplay = BooleanType()
    number_of_winners = IntType()
    number_of_runners = IntType()
    number_of_active_runners = IntType()
    last_match_time = DateTimeType()
    total_matched = FloatType()
    total_available = FloatType()
    cross_matching = BooleanType()
    runners_voidable = BooleanType()
    version = FloatType()
    runners = ListType(ModelType(Runner))


class RunnerProfitAndLoss(BetfairModel):
    selection_id = IntType()
    if_win = FloatType()
    if_lose = FloatType()


class MarketProfitAndLoss(BetfairModel):
    market_id = StringType()
    commission_applied = FloatType()
    profit_and_losses = ListType(ModelType(RunnerProfitAndLoss))


class ExBestOffersOverrides(BetfairModel):
    best_prices_depth = IntType()
    rollup_model = EnumType(constants.RollupModel)
    rollup_limit = IntType()
    rollup_liability_threshold = FloatType()
    rollup_liability_factor = IntType()


class PriceProjection(BetfairModel):
    price_data = ListType(EnumType(constants.PriceData))
    ex_best_offers_overrides = ModelType(ExBestOffersOverrides)
    virtualise = BooleanType()
    rollover_stakes = BooleanType()


class LimitOrder(BetfairModel):
    size = FloatType(required=True)
    price = FloatType(required=True)
    persistence_type = EnumType(constants.PersistenceType, required=True)


class LimitOnCloseOrder(BetfairModel):
    liability = FloatType(required=True)
    price = FloatType(required=True)


class MarketOnCloseOrder(BetfairModel):
    liability = FloatType(required=True)


# Results

class CompetitionResult(BetfairModel):

    competition = ModelType(Competition)
    market_count = IntType()
    competition_region = StringType()


class CountryCodeResult(BetfairModel):
    country_code = StringType()
    market_count = IntType()


class EventResult(BetfairModel):

    event = ModelType(Event)
    market_count = IntType()


class EventTypeResult(BetfairModel):

    event_type = ModelType(EventType)
    market_count = IntType()


class MarketTypeResult(BetfairModel):
    market_type = StringType()
    market_count = IntType()


class TimeRangeResult(BetfairModel):

    time_range = ModelType(TimeRange)
    market_count = IntType()


class VenueResult(BetfairModel):
    venue = StringType()
    market_count = IntType()


# Instructions

class PlaceInstruction(BetfairModel):
    order_type = EnumType(constants.OrderType, required=True)
    selection_id = IntType(required=True)
    handicap = FloatType()
    side = EnumType(constants.Side, required=True)
    limit_order = ModelType(LimitOrder)
    limit_on_close_order = ModelType(LimitOnCloseOrder)
    market_on_close_order = ModelType(MarketOnCloseOrder)


class CancelInstruction(BetfairModel):
    bet_id = StringType(required=True)
    size_reduction = FloatType()


class ReplaceInstruction(BetfairModel):
    bet_id = StringType(required=True)
    new_price = FloatType(required=True)


class UpdateInstruction(BetfairModel):
    bet_id = StringType(required=True)
    new_persistence_type = EnumType(constants.PersistenceType, required=True)


# Summary reports

class CurrentOrderSummary(BetfairModel):
    bet_id = StringType(required=True)
    market_id = StringType(required=True)
    selection_id = IntType(required=True)
    handicap = FloatType(required=True)
    price_size = ModelType(PriceSize, required=True)
    bsp_liability = FloatType(required=True)
    side = EnumType(constants.Side, required=True)
    status = EnumType(constants.OrderStatus, required=True)
    persistence_type = EnumType(constants.PersistenceType, required=True)
    order_type = EnumType(constants.OrderType, required=True)
    placed_date = DateTimeType(required=True)
    matched_date = DateTimeType()
    average_price_matched = FloatType()
    size_matched = FloatType()
    size_remaining = FloatType()
    size_lapsed = FloatType()
    size_cancelled = FloatType()
    size_voided = FloatType()
    regulator_auth_code = StringType()
    regulator_code = StringType()


class CurrentOrderSummaryReport(BetfairModel):
    current_orders = ListType(ModelType(CurrentOrderSummary), required=True)
    more_available = BooleanType(required=True)


class ItemDescription(BetfairModel):
    event_type_desc = StringType()
    event_desc = StringType()
    market_desc = StringType()
    market_start_Time = DateTimeType()
    runner_desc = StringType()
    number_of_winners = IntType()


class ClearedOrderSummary(BetfairModel):
    event_type_id = StringType()
    event_id = StringType()
    market_id = StringType()
    selection_id = IntType()
    handicap = FloatType()
    bet_id = StringType()
    placed_date = DateTimeType()
    persistence_type = EnumType(constants.PersistenceType)
    order_type = EnumType(constants.OrderType)
    side = EnumType(constants.Side)
    item_description = ModelType(ItemDescription)
    price_requested = FloatType()
    settled_date = DateTimeType()
    bet_count = IntType()
    commission = FloatType()
    price_matched = FloatType()
    price_reduced = BooleanType()
    size_settled = FloatType()
    profit = FloatType()
    size_cancelled = FloatType()


class ClearedOrderSummaryReport(BetfairModel):
    cleared_orders = ListType(ModelType(ClearedOrderSummary), required=True)
    more_available = BooleanType(required=True)


# Instruction reports

class BaseInstructionReport(BetfairModel):
    status = EnumType(constants.InstructionReportStatus, required=True)
    error_code = EnumType(constants.InstructionReportErrorCode)


class PlaceInstructionReport(BaseInstructionReport):
    instruction = ModelType(PlaceInstruction, required=True)
    bet_id = StringType()
    placed_date = DateTimeType()
    average_price_matched = FloatType()
    size_matched = FloatType()


class CancelInstructionReport(BaseInstructionReport):
    instruction = ModelType(CancelInstruction)
    size_cancelled = FloatType(required=True)
    cancelled_date = DateTimeType()


class ReplaceInstructionReport(BaseInstructionReport):
    cancel_instruction_report = ModelType(CancelInstructionReport)
    place_instruction_report = ModelType(PlaceInstructionReport)


class UpdateInstructionReport(BaseInstructionReport):
    instruction = ModelType(UpdateInstruction, required=True)


# Execution reports

class BaseExecutionReport(BetfairModel):
    customer_ref = StringType()
    status = EnumType(constants.ExecutionReportStatus, required=True)
    error_code = EnumType(constants.ExecutionReportErrorCode)
    market_id = StringType()


class PlaceExecutionReport(BaseExecutionReport):
    instruction_reports = ListType(ModelType(PlaceInstructionReport))


class CancelExecutionReport(BaseExecutionReport):
    instruction_reports = ListType(ModelType(CancelInstructionReport))


class ReplaceExecutionReport(BaseExecutionReport):
    instruction_reports = ListType(ModelType(ReplaceInstructionReport))


class UpdateExecutionReport(BaseExecutionReport):
    instruction_reports = ListType(ModelType(UpdateInstructionReport))


# Accounts

class AccountFundsResponse(BetfairModel):
    available_to_bet_balance = FloatType()
    exposure = FloatType()
    retained_commission = FloatType()
    exposure_limit = FloatType()
    discount_rate = FloatType()
    points_balance = IntType()
    wallet = EnumType(constants.Wallet)


class StatementLegacyData(BetfairModel):
    avg_price = FloatType()
    bet_size = FloatType()
    bet_type = StringType()
    bet_category_type = StringType()
    commission_rate = StringType()
    event_id = LongType()
    event_type_id = LongType()
    full_market_name = StringType()
    gross_bet_amount = FloatType()
    market_name = StringType()
    market_type = StringType()
    placed_date = DateTimeType()
    selection_id = LongType()
    selection_name = StringType()
    start_date = DateTimeType()
    transaction_type = StringType()
    transaction_id = LongType()
    win_lose = StringType()


class StatementItem(BetfairModel):
    ref_id = StringType()
    item_date = DateTimeType()
    amount = FloatType()
    balance = FloatType()
    item_class = EnumType(constants.ItemClass)
    item_class_data = DictType(StringType)
    legacy_data = ModelType(StatementLegacyData)


class AccountDetailsResponse(BetfairModel):
    currency_code = StringType()
    first_name = StringType()
    last_name = StringType()
    locale_code = StringType()
    region = StringType()
    timezone = StringType()
    discount_rate = FloatType()
    points_balance = IntType()
    country_code = StringType()


class AccountStatementReport(BetfairModel):
    account_statement = ListType(ModelType(StatementItem))
    more_available = BooleanType()


class CurrencyRate(BetfairModel):
    currency_code = StringType()
    rate = FloatType()


class TransferResponse(BetfairModel):
    transaction_id = StringType()
