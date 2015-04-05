# -*- coding: utf-8 -*-

"""BetFair betting enums. See
https://api.developer.betfair.com/services/webapps/docs/display/1smk3cen4v3lu3yomq5qye0ni/Betting+Enums
"""

from enum import Enum


MarketProjection = Enum(
    'MarketProjection', [
        'COMPETITION',
        'MARKET_DESCRIPTION',
        'EVENT',
        'EVENT_TYPE',
        'RUNNER_METADATA',
        'RUNNER_DESCRIPTION',
        'MARKET_START_TIME',
    ]
)

PriceData = Enum(
    'PriceData', [
        'SP_AVAILABLE',
        'SP_TRADED',
        'EX_BEST_OFFERS',
        'EX_ALL_OFFERS',
        'EX_TRADED',
    ]
)

MatchProjection = Enum(
    'MatchProjection', [
        'NO_ROLLUP',
        'ROLLED_UP_BY_PRICE',
        'ROLLED_UP_BY_AVG_PRICE',
    ]
)

OrderProjection = Enum(
    'OrderProjection', [
        'ALL',
        'EXECUTABLE',
        'EXECUTION_COMPLETE',
    ]
)

MarketStatus = Enum(
    'MarketStatus', [
        'INACTIVE',
        'OPEN',
        'SUSPENDED',
        'CLOSED',
    ]
)

RunnerStatus = Enum(
    'RunnerStatus', [
        'ACTIVE',
        'WINNER',
        'LOSER',
        'REMOVED_VACANT',
        'REMOVED',
        'HIDDEN',
    ]
)

TimeGranularity = Enum(
    'TimeGranularity', [
        'DAYS',
        'HOURS',
        'MINUTES',
    ]
)

Side = Enum(
    'Side', [
        'BACK',
        'LAY',
    ]
)

OrderStatus = Enum(
    'OrderStatus', [
        'EXECUTION_COMPLETE',
        'EXECUTABLE',
    ]
)

OrderBy = Enum(
    'OrderBy', [
        'BY_BET',
        'BY_MARKET',
        'BY_MATCH_TIME',
        'BY_PLACE_TIME',
        'BY_SETTLED_TIME',
        'BY_VOID_TIME',
    ]
)

SortDir = Enum(
    'SortDir', [
        'EARLIEST_TO_LATEST',
        'LATEST_TO_EARLIEST',
    ]
)

OrderType = Enum(
    'OrderType', [
        'LIMIT',
        'LIMIT_ON_CLOSE',
        'MARKET_ON_CLOSE',
    ]
)

MarketSort = Enum(
    'MarketSort', [
        'MINIMUM_TRADED',
        'MAXIMUM_TRADED',
        'MINIMUM_AVAILABLE',
        'MAXIMUM_AVAILABLE',
        'FIRST_TO_START',
        'LAST_TO_START',
    ]
)

MarketBettingType = Enum(
    'MarketBettingType', [
        'ODDS',
        'LINE',
        'RANGE',
        'ASIAN_HANDICAP_DOUBLE_LINE',
        'ASIAN_HANDICAP_SINGLE_LINE',
        'FIXED_ODDS',
    ]
)

ExecutionReportStatus = Enum(
    'ExecutionReportStatus', [
        'SUCCESS',
        'FAILURE',
        'PROCESSED_WITH_ERRORS',
        'TIMEOUT',
    ]
)

ExecutionReportErrorCode = Enum(
    'ExecutionReportErrorCode', [
        'ERROR_IN_MATCHER',
        'PROCESSED_WITH_ERRORS',
        'BET_ACTION_ERROR',
        'INVALID_ACCOUNT_STATE',
        'INVALID_WALLET_STATUS',
        'INSUFFICIENT_FUNDS',
        'LOSS_LIMIT_EXCEEDED',
        'MARKET_SUSPENDED',
        'MARKET_NOT_OPEN_FOR_BETTING',
        'DUPLICATE_TRANSACTION',
        'INVALID_ORDER',
        'INVALID_MARKET_ID',
        'PERMISSION_DENIED',
        'DUPLICATE_BETIDS',
        'NO_ACTION_REQUIRED',
        'SERVICE_UNAVAILABLE',
        'REJECTED_BY_REGULATOR',
    ]
)

PersistenceType = Enum(
    'PersistenceType', [
        'LAPSE',
        'PERSIST',
        'MARKET_ON_CLOSE',
    ]
)

InstructionReportStatus = Enum(
    'InstructionReportStatus', [
        'SUCCESS',
        'FAILURE',
        'TIMEOUT',
    ]
)

InstructionReportErrorCode = Enum(
    'InstructionReportErrorCode', [
        'INVALID_BET_SIZE',
        'INVALID_RUNNER',
        'BET_TAKEN_OR_LAPSED',
        'BET_IN_PROGRESS',
        'RUNNER_REMOVED',
        'MARKET_NOT_OPEN_FOR_BETTING',
        'LOSS_LIMIT_EXCEEDED',
        'MARKET_NOT_OPEN_FOR_BSP_BETTING',
        'INVALID_PRICE_EDIT',
        'INVALID_ODDS',
        'INSUFFICIENT_FUNDS',
        'INVALID_PERSISTENCE_TYPE',
        'ERROR_IN_MATCHER',
        'INVALID_BACK_LAY_COMBINATION',
        'ERROR_IN_ORDER',
        'INVALID_BID_TYPE',
        'INVALID_BET_ID',
        'CANCELLED_NOT_PLACED',
        'RELATED_ACTION_FAILED',
        'NO_ACTION_REQUIRED',
    ]
)

RollupModel = Enum(
    'RollupModel', [
        'STAKE',
        'PAYOUT',
        'MANAGED_LIABILITY',
        'NONE',
    ]
)

GroupBy = Enum(
    'GroupBy', [
        'EVENT_TYPE',
        'EVENT',
        'MARKET',
        'SIDE',
        'BET',
    ]
)

BetStatus = Enum(
    'BetStatus', [
        'SETTLED',
        'VOIDED',
        'LAPSED',
        'CANCELLED',
    ]
)

Exchange = Enum(
    'Exchange', [
        'AUS',
        'UK',
    ]
)

Endpoint = Enum(
    'Endpoint', [
        'Betting',
        'Account',
    ]
)

Wallet = Enum(
    'Wallet', [
        'UK',
        'AUSTRALIAN',
    ]
)

IncludeItem = Enum(
    'IncludeItem', [
        'ALL',
        'DEPOSITS_WITHDRAWALS',
        'EXCHANGE',
        'POKER_ROOM',
    ]
)

ItemClass = Enum(
    'ItemClass', [
        'UNKNOWN',
    ]
)
