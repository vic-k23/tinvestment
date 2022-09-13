from enum import Enum


class AccountType(Enum):
    UNSPECIFIED = 0
    USUAL = 1
    IIS = 2
    INVEST_BOX = 3

    def __str__(self):
        return self.name


class AccountStatus(Enum):
    UNSPECIFIED = 0
    NEW = 1
    OPEN = 2
    CLOSED = 3

    def __str__(self):
        return self.name


class OperationStatus(Enum):
    UNSPECIFIED = 0
    EXECUTED = 1
    CANCELED = 2
    PROGRESS = 3

    def __str__(self):
        return self.name


class OperationType(Enum):
    UNSPECIFIED = 0
    INPUT = 1
    BOND_TAX = 2
    OUTPUT_SECURITIES = 3
    OVERNIGHT = 4
    TAX = 5
    BOND_REPAYMENT_FULL = 6
    SELL_CARD = 7
    DIVIDEND_TAX = 8
    OUTPUT = 9
    BOND_REPAYMENT = 10
    TAX_CORRECTION = 11
    SERVICE_FEE = 12
    BENEFIT_TAX = 13
    MARGIN_FEE = 14
    BUY = 15
    BUY_CARD = 16
    INPUT_SECURITIES = 17
    SELL_MARGIN = 18
    BROKER_FEE = 19
    BUY_MARGIN = 20
    DIVIDEND = 21
    SELL = 22
    COUPON = 23
    SUCCESS_FEE = 24
    DIVIDEND_TRANSFER = 25
    ACCRUING_VARMARGIN = 26
    WRITING_OFF_VARMARGIN = 27
    DELIVERY_BUY = 28
    DELIVERY_SELL = 29
    TRACK_MFEE = 30
    TRACK_PFEE = 31
    TAX_PROGRESSIVE = 32
    BOND_TAX_PROGRESSIVE = 33
    DIVIDEND_TAX_PROGRESSIVE = 34
    BENEFIT_TAX_PROGRESSIVE = 35
    TAX_CORRECTION_PROGRESSIVE = 36
    TAX_REPO_PROGRESSIVE = 37
    TAX_REPO = 38
    TAX_REPO_HOLD = 39
    TAX_REPO_REFUND = 40
    TAX_REPO_HOLD_PROGRESSIVE = 41
    TAX_REPO_REFUND_PROGRESSIVE = 42
    DIV_EXT = 43
    TAX_CORRECTION_COUPON = 44

    def __str__(self):
        return self.name


class InstrumentType(Enum):
    UNSPECIFIED = 0
    BOND = 1
    SHARE = 2
    CURRENCY = 3
    ETF = 4
    FUTURES = 5
    SP = 6
    OPTION = 7

    def __str__(self):
        return self.name


class CouponType(Enum):
    UNSPECIFIED = 0
    CONSTANT = 1
    FLOATING = 2
    DISCOUNT = 3
    MORTGAGE = 4
    FIX = 5
    VARIABLE = 6
    OTHER = 7

    def __str__(self):
        return self.name


class TradingStatus(Enum):
    UNSPECIFIED = 0
    NOT_AVAILABLE_FOR_TRADING = 1
    OPENING_PERIOD = 2
    CLOSING_PERIOD = 3
    BREAK_IN_TRADING = 4
    NORMAL_TRADING = 5
    CLOSING_AUCTION = 6
    DARK_POOL_AUCTION = 7
    DISCRETE_AUCTION = 8
    OPENING_AUCTION_PERIOD = 9
    TRADING_AT_CLOSING_AUCTION_PRICE = 10
    SESSION_ASSIGNED = 11
    SESSION_CLOSE = 12
    SESSION_OPEN = 13
    DEALER_NORMAL_TRADING = 14
    DEALER_BREAK_IN_TRADING = 15
    DEALER_NOT_AVAILABLE_FOR_TRADING = 16

    def __str__(self):
        return self.name
