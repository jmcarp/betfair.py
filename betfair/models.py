# -*- coding: utf-8 -*-

import six

from . import constants

from .meta.datatype import DataType
from .meta.field import Field, ListField
from .datatype import EnumType, ModelType, datetime_type

from .model import BetfairModel


class Event(BetfairModel):
    id = Field(DataType(six.text_type))
    name = Field(DataType(six.text_type))
    country_code = Field(DataType(six.text_type))
    timezone = Field(DataType(six.text_type))
    venue = Field(DataType(six.text_type))
    open_date = Field(datetime_type)


class MarketDescription(BetfairModel):
    persistence_enabled = Field(DataType(bool), required=True)
    bsp_market = Field(DataType(bool), required=True)
    market_time = Field(datetime_type, required=True)
    suspend_time = Field(datetime_type, required=True)
    settle_time = Field(datetime_type)
    betting_type = Field(EnumType(constants.MarketBettingType), required=True)
    turn_in_play_enabled = Field(DataType(bool), required=True)
    market_type = Field(DataType(six.text_type), required=True)
    regulator = Field(DataType(six.text_type), required=True)
    market_base_rate = Field(DataType(float), required=True)
    discount_allowed = Field(DataType(bool), required=True)
    wallet = Field(DataType(six.text_type))
    rules = Field(DataType(six.text_type))
    rules_has_date = Field(DataType(bool))
    clarifications = Field(DataType(six.text_type))


class RunnerCatalog(BetfairModel):
    selection_id = Field(DataType(six.text_type), required=True)
    runner_name = Field(DataType(six.text_type), required=True)
    handicap = Field(DataType(float), required=True)
    sort_priority = Field(DataType(int), required=True)
    metadata = Field(DataType(dict))


class EventType(BetfairModel):
    id = Field(DataType(six.text_type))
    name = Field(DataType(six.text_type))


class Competition(BetfairModel):
    id = Field(DataType(six.text_type))
    name = Field(DataType(six.text_type))


class MarketCatalogue(BetfairModel):
    market_id = Field(DataType(six.text_type))
    market_name = Field(DataType(six.text_type))
    market_start_time = Field(datetime_type)
    description = Field(EnumType(MarketDescription))
    total_matched = Field(DataType(float))
    runners = ListField(ModelType(RunnerCatalog))
    event_type = Field(ModelType(EventType))
    competition = Field(ModelType(Competition))
    event = Field(ModelType(Event))


class TimeRange(BetfairModel):
    from_ = Field(datetime_type)
    to = Field(datetime_type)


class MarketFilter(BetfairModel):
    text_query = Field(DataType(six.text_type))
    exchange_ids = ListField(DataType(six.text_type))
    event_type_ids = ListField(DataType(six.text_type))
    event_ids = ListField(DataType(six.text_type))
    competition_ids = ListField(DataType(six.text_type))
    market_ids = ListField(DataType(six.text_type))
    venues = ListField(DataType(six.text_type))
    bsp_only = Field(DataType(bool))
    turn_in_play_enabled = Field(DataType(bool))
    in_play_only = Field(DataType(bool))
    market_betting_types = ListField(EnumType(constants.MarketBettingType))
    market_countries = ListField(DataType(six.text_type))
    market_type_codes = ListField(DataType(six.text_type))
    market_start_time = Field(ModelType(TimeRange))
    with_orders = ListField(EnumType(constants.OrderStatus))


class PriceSize(BetfairModel):
    price = Field(DataType(float), required=True)
    size = Field(DataType(float), required=True)


class StartingPrices(BetfairModel):
    near_price = Field(DataType(float))
    far_price = Field(DataType(float))
    back_state_taken = Field(ModelType(PriceSize))
    lay_liability_taken = Field(ModelType(PriceSize))
    actual_SP = Field(DataType(float))


class ExchangePrices(BetfairModel):
    available_to_back = ListField(ModelType(PriceSize))
    available_to_lay = ListField(ModelType(PriceSize))
    traded_volume = ListField(ModelType(PriceSize))


class Order(BetfairModel):
    bet_id = Field(DataType(six.text_type), required=True)
    order_type = Field(EnumType(constants.OrderType), required=True)
    status = Field(EnumType(constants.OrderStatus), required=True)
    persistence_type = Field(EnumType(constants.PersistenceType), required=True)
    side = Field(EnumType(constants.Side), required=True)
    price = Field(DataType(float), required=True)
    size = Field(DataType(float), required=True)
    bsp_liability = Field(DataType(float), required=True)
    placed_date = Field(datetime_type, required=True)
    avg_price_matched = Field(DataType(float))
    size_matched = Field(DataType(float))
    size_remaining = Field(DataType(float))
    size_lapsed = Field(DataType(float))
    size_cancelled = Field(DataType(float))
    size_voided = Field(DataType(float))


class Match(BetfairModel):
    bet_id = Field(DataType(six.text_type))
    match_id = Field(DataType(six.text_type))
    side = Field(EnumType(constants.Side), required=True)
    price = Field(DataType(float), required=True)
    size = Field(DataType(float), required=True)
    match_date = Field(datetime_type)


class Runner(BetfairModel):
    selection_id = Field(DataType(float), required=True)
    handicap = Field(DataType(float), required=True)
    status = Field(EnumType(constants.RunnerStatus), required=True)
    adjustment_factor = Field(DataType(float))
    last_price_traded = Field(DataType(float))
    total_matched = Field(DataType(float))
    removal_date = Field(datetime_type)
    sp = Field(ModelType(StartingPrices))
    ex = Field(ModelType(ExchangePrices))
    orders = ListField(ModelType(Order))
    matches = ListField(ModelType(Match))


class MarketBook(BetfairModel):
    market_id = Field(DataType(six.text_type), required=True)
    is_market_data_delayed = Field(DataType(bool), required=True)
    status = Field(EnumType(constants.MarketStatus))
    bet_delay = Field(DataType(int))
    bsp_reconciled = Field(DataType(bool))
    complete = Field(DataType(bool))
    inplay = Field(DataType(bool))
    number_of_winners = Field(DataType(int))
    number_of_runners = Field(DataType(int))
    number_of_active_runners = Field(DataType(int))
    last_match_time = Field(datetime_type)
    total_matched = Field(DataType(float))
    total_available = Field(DataType(float))
    cross_matching = Field(DataType(bool))
    runners_voidable = Field(DataType(bool))
    version = Field(DataType(float))
    runners = ListField(ModelType(Runner))


class RunnerProfitAndLoss(BetfairModel):
    selection_id = Field(DataType(float))
    if_win = Field(DataType(float))
    if_lose = Field(DataType(float))


class MarketProfitAndLoss(BetfairModel):
    market_id = Field(DataType(six.text_type))
    commission_applied = Field(DataType(float))
    profit_and_losses = ListField(ModelType(RunnerProfitAndLoss))


class ExBestOffersOverrides(BetfairModel):
    best_prices_depth = Field(DataType(int))
    rollup_model = Field(EnumType(constants.RollupModel))
    rollup_limit = Field(DataType(int))
    rollup_liability_threshold = Field(DataType(float))
    rollup_liability_factor = Field(DataType(int))


class PriceProjection(BetfairModel):
    price_data = ListField(EnumType(constants.PriceData))
    ex_best_offer_overrides = Field(ModelType(ExBestOffersOverrides))
    virtualize = Field(DataType(bool))
    rollover_stakes = Field(DataType(bool))


class LimitOrder(BetfairModel):
    size = Field(DataType(float), required=True)
    price = Field(DataType(float), required=True)
    persistence_type = Field(EnumType(constants.PersistenceType), required=True)


class LimitOnCloseOrder(BetfairModel):
    liability = Field(DataType(float), required=True)
    price = Field(DataType(float), required=True)


class MarketOnCloseOrder(BetfairModel):
    liability = Field(DataType(float), required=True)


# Results

class CompetitionResult(BetfairModel):

    competition = Field(ModelType(Competition))
    market_count = Field(DataType(int))
    competition_region = Field(DataType(six.text_type))


class CountryCodeResult(BetfairModel):
    country_code = Field(DataType(six.text_type))
    market_count = Field(DataType(int))


class EventResult(BetfairModel):

    event = Field(ModelType(Event))
    market_count = Field(DataType(int))


class EventTypeResult(BetfairModel):

    event_type = Field(ModelType(EventType))
    market_count = Field(DataType(int))


class MarketTypeResult(BetfairModel):
    market_type = Field(DataType(six.text_type))
    market_count = Field(DataType(int))


class TimeRangeResult(BetfairModel):

    time_range = Field(ModelType(TimeRange))
    market_count = Field(DataType(int))


class VenueResult(BetfairModel):
    venue = Field(DataType(six.text_type))
    market_count = Field(DataType(int))


# Instructions

class PlaceInstruction(BetfairModel):
    order_type = Field(EnumType(constants.OrderType), required=True)
    selection_id = Field(DataType(float), required=True)
    handicap = Field(DataType(float))
    side = Field(EnumType(constants.Side), required=True)
    limit_order = Field(ModelType(LimitOrder))
    limit_on_close_order = Field(ModelType(LimitOnCloseOrder))
    market_on_close_order = Field(ModelType(MarketOnCloseOrder))


class CancelInstruction(BetfairModel):
    bet_id = Field(DataType(six.text_type), required=True)
    size_reduction = Field(DataType(float))


class ReplaceInstruction(BetfairModel):
    bet_id = Field(DataType(six.text_type), required=True)
    new_price = Field(DataType(float), required=True)


class UpdateInstruction(BetfairModel):
    bet_id = Field(DataType(six.text_type), required=True)
    new_persistence_type = Field(EnumType(constants.PersistenceType), required=True)


# Summary reports

class CurrentOrderSummary(BetfairModel):
    bet_id = Field(DataType(six.text_type), required=True)
    market_id = Field(DataType(six.text_type), required=True)
    selection_id = Field(DataType(float), required=True)
    handicap = Field(DataType(float), required=True)
    price_size = Field(DataType(PriceSize), required=True)
    bsp_liability = Field(DataType(float), required=True)
    side = Field(EnumType(constants.Side), required=True)
    status = Field(EnumType(constants.OrderStatus), required=True)
    persistence_type = Field(EnumType(constants.PersistenceType), required=True)
    order_type = Field(EnumType(constants.OrderType), required=True)
    placed_date = Field(datetime_type, required=True)
    matched_date = Field(datetime_type, required=True)
    average_price_matched = Field(DataType(float))
    size_matched = Field(DataType(float))
    size_remaining = Field(DataType(float))
    size_lapsed = Field(DataType(float))
    size_cancelled = Field(DataType(float))
    size_voided = Field(DataType(float))
    regulator_auth_code = Field(DataType(six.text_type))
    regulator_code = Field(DataType(six.text_type))


class CurrentOrderSummaryReport(BetfairModel):
    current_orders = ListField(ModelType(CurrentOrderSummary), required=True)
    more_available = Field(DataType(bool), required=True)


class ItemDescription(BetfairModel):
    event_type_desc = Field(DataType(six.text_type))
    event_desc = Field(DataType(six.text_type))
    market_desc = Field(DataType(six.text_type))
    market_start_Time = Field(datetime_type)
    runner_desc = Field(DataType(six.text_type))
    number_of_winners = Field(DataType(int))


class ClearedOrderSummary(BetfairModel):
    event_type_id = Field(DataType(six.text_type))
    event_id = Field(DataType(six.text_type))
    market_id = Field(DataType(six.text_type))
    selection_id = Field(DataType(six.text_type))
    handicap = Field(DataType(float))
    bet_id = Field(DataType(six.text_type))
    placed_data = Field(datetime_type)
    persistence_type = Field(EnumType(constants.PersistenceType))
    order_type = Field(EnumType(constants.OrderType))
    side = Field(EnumType(constants.Side))
    item_description = Field(ModelType(ItemDescription))
    price_requested = Field(ModelType(float))
    settled_date = Field(datetime_type)
    bet_count = Field(DataType(int))
    commission = Field(ModelType(float))
    price_matched = Field(ModelType(float))
    price_reduced = Field(DataType(bool))
    size_settled = Field(ModelType(float))
    profit = Field(ModelType(float))
    size_cancelled = Field(ModelType(float))


class ClearedOrderSummaryReport(BetfairModel):
    current_orders = ListField(ModelType(ClearedOrderSummary), required=True)
    more_available = Field(DataType(bool), required=True)


# Instruction reports

class BaseInstructionReport(BetfairModel):
    status = Field(EnumType(constants.InstructionReportStatus), required=True)
    error_code = Field(EnumType(constants.InstructionReportErrorCode))


class PlaceInstructionReport(BaseInstructionReport):
    instruction = Field(ModelType(PlaceInstruction), required=True)
    bet_id = Field(DataType(six.text_type))
    placed_date = Field(datetime_type)
    average_price_matched = Field(DataType(float))
    size_matched = Field(DataType(float))


class CancelInstructionReport(BaseInstructionReport):
    instruction = Field(ModelType(CancelInstruction))
    size_cancelled = Field(DataType(float), required=True)
    cancelled_date = Field(datetime_type)


class ReplaceInstructionReport(BaseInstructionReport):
    cancel_instruction_report = Field(ModelType(CancelInstructionReport))
    place_instruction_report = Field(ModelType(PlaceInstructionReport))


class UpdateInstructionReport(BaseInstructionReport):
    instruction = Field(ModelType(UpdateInstruction), required=True)


# Execution reports

class BaseExecutionReport(BetfairModel):
    customer_ref = Field(DataType(six.text_type))
    status = Field(EnumType(constants.ExecutionReportStatus), required=True)
    error_code = Field(EnumType(constants.ExecutionReportErrorCode))
    market_id = Field(DataType(six.text_type))


class PlaceExecutionReport(BaseExecutionReport):
    instruction_reports = ListField(ModelType(PlaceInstructionReport))


class CancelExecutionReport(BaseExecutionReport):
    instruction_reports = ListField(ModelType(CancelInstructionReport))


class ReplaceExecutionReport(BaseExecutionReport):
    instruction_reports = ListField(ModelType(ReplaceInstructionReport))


class UpdateExecutionReport(BaseExecutionReport):
    instruction_reports = ListField(ModelType(UpdateInstructionReport))
