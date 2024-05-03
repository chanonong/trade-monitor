from enum import Enum
from utils import Repr

class EventType(Enum):
    ACCOUNT_UPDATE = "ACCOUNT_UPDATE"
    MARGIN_CALL = "MARGIN_CALL"
    ORDER_TRADE_UPDATE = "ORDER_TRADE_UPDATE"
    ACCOUNT_CONFIG_UPDATE = "ACCOUNT_CONFIG_UPDATE"
    STRATEGY_UPDATE = "STRATEGY_UPDATE"
    GRID_UPDATE = "GRID_UPDATE"
    CONDITIONAL_ORDER_TRIGGER_REJECT = "CONDITIONAL_ORDER_TRIGGER_REJECT"

class MarginType(Enum):
    CROSS = "CROSS"
    ISOLATED = "ISOLATED"

class AccountUpdateReason(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    ORDER = "ORDER"
    FUNDING_FEE = "FUNDING_FEE"
    WITHDRAW_REJECT = "WITHDRAW_REJECT"
    ADJUSTMENT = "ADJUSTMENT"
    INSURANCE_CLEAR = "INSURANCE_CLEAR"
    ADMIN_DEPOSIT = "ADMIN_DEPOSIT"
    ADMIN_WITHDRAW = "ADMIN_WITHDRAW"
    MARGIN_TRANSFER = "MARGIN_TRANSFER"
    MARGIN_TYPE_CHANGE = "MARGIN_TYPE_CHANGE"
    ASSET_TRANSFER = "ASSET_TRANSFER"
    OPTIONS_PREMIUM_FEE = "OPTIONS_PREMIUM_FEE"
    OPTIONS_SETTLE_PROFIT = "OPTIONS_SETTLE_PROFIT"
    AUTO_EXCHANGE = "AUTO_EXCHANGE"
    COIN_SWAP_DEPOSIT = "COIN_SWAP_DEPOSIT"
    COIN_SWAP_WITHDRAW = "COIN_SWAP_WITHDRAW"

class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"

class PositionSide(Enum):
    BOTH = "BOTH"
    LONG = "LONG"
    SHORT = "SHORT"
    
class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_MARKET = "STOP_MARKET"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"
    LIQUIDATION = "LIQUIDATION"

class ExecutionType(Enum):
    NEW = "NEW"
    CANCELED = "CANCELED"
    CALCULATED = "CALCULATED"
    EXPIRED = "EXPIRED"
    TRADE = "TRADE"

class OrderStatus(Enum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"
    NEW_INSURANCE = "NEW_INSURANCE"
    NEW_ADL = "NEW_ADL"

class TimeInForce(Enum):
    GTC = "GTC"
    GTE_GTC = "GTE_GTC"
    IOC = "IOC"
    FOK = "FOK"
    GTX = "GTX"

class WorkingType(Enum):
    MARK_PRICE = "MARK_PRICE"
    CONTRACT_PRICE = "CONTRACT_PRICE"

class EventReasonType(Enum):
    DEPOSIT = "DEPOSIT" 
    WITHDRAW = "WITHDRAW" 
    ORDER = "ORDER" 
    FUNDING_FEE = "FUNDING_FEE" 
    WITHDRAW_REJECT = "WITHDRAW_REJECT" 
    ADJUSTMENT = "ADJUSTMENT" 
    INSURANCE_CLEAR = "INSURANCE_CLEAR" 
    ADMIN_DEPOSIT = "ADMIN_DEPOSIT" 
    ADMIN_WITHDRAW = "ADMIN_WITHDRAW" 
    MARGIN_TRANSFER = "MARGIN_TRANSFER" 
    MARGIN_TYPE_CHANGE = "MARGIN_TYPE_CHANGE" 
    ASSET_TRANSFER = "ASSET_TRANSFER" 
    OPTIONS_PREMIUM_FEE = "OPTIONS_PREMIUM_FEE" 
    OPTIONS_SETTLE_PROFIT = "OPTIONS_SETTLE_PROFIT" 
    AUTO_EXCHANGE = "AUTO_EXCHANGE" 

class PositionUpdate(Repr):
    def __init__(self, payload) -> None:
        self.symbol = payload['s']
        self.position_side = payload['ps']
        self.position_amount = float(payload['pa'])
        self.margin_type = MarginType[payload['mt'].upper()]
        self.isolated_wallet = float(payload['iw']) if 'iw' in payload.keys() else None
        self.mark_price = float(payload['mp']) if 'mp' in payload.keys() else None
        self.entry_price = float(payload['ep']) if 'ep' in payload.keys() else None
        self.unrelized_pnl = float(payload['up']) 
        self.maintainance_margin = float(payload['mm']) if 'mm' in payload.keys() else None
        self.accumulated_relized = float(payload['cr']) if 'cr' in payload.keys() else None

    def __str__(self) -> str:
        usd = self.position_amount * self.entry_price
        if usd == 0.0:
            return f"{self.symbol} closed" 
        return f"{self.symbol} {self.position_amount} {usd} | upnl: {self.unrelized_pnl}"

class BalanceUpdate(Repr):
    def __init__(self, payload) -> None:
        self.asset = payload['a']
        self.wallet_balance = float(payload['wb'])
        self.cross_wallet_balance = float(payload['cw'])
        self.balance_change = float(payload['bc'])
    
    def __str__(self) -> str:
        return f"{self.wallet_balance:.4f} {self.asset}"

class AccountUpdate(Repr):
    def __init__(self, payload) -> None:
         self.event_reason_type = EventReasonType[payload['m']]
         self.balances = [BalanceUpdate(_) for _ in payload['B']]
         self.positions = [PositionUpdate(_) for _ in payload['P']]
    
    def __str__(self) -> str:
        message = f"Reason: {self.event_reason_type.value}\n"
        if self.balances:
            message += f"Balance:\n"
            for _ in self.balances:
                message += f"\t{str(_)}\n"
        if self.positions:
            message += f"Positions:\n"
            for _ in self.positions:
                message += f"\t{str(_)}\n"
        return message

class OrderTradeUpdate(Repr):
    def __init__(self, payload) -> None:
        self.symbol = payload['s']
        self.client_order_id = payload['c']
        self.side = Side[payload['S']]
        self.order_type = OrderType[payload['o']]
        self.time_in_force = TimeInForce[payload['f']]
        self.original_quantity = float(payload['q'])
        self.original_price = float(payload['p'])
        self.average_price = float(payload['ap'])
        self.stop_price = float(payload['sp'])
        self.execution_type = ExecutionType[payload['x']]
        self.order_status = OrderStatus[payload['X']]
        self.order_id = int(payload['i'])
        self.order_last_filled_quantity = float(payload['l'])
        self.order_filled_accumulated_quantity = float(payload['z'])
        self.last_filled_price = float(payload['L'])
        self.commission_asset = payload['N'] if 'N' in payload.keys() else None
        self.commission = float(payload['n']) if 'n' in payload.keys() else None
        self.order_trade_time = int(payload['T'])
        self.trade_id = int(payload['t'])
        self.bids = float(payload['b'])
        self.asks = float(payload['a'])
        self.maker = bool(payload['m'])
        self.reduce_only = bool(payload['R'])
        self.working_type = WorkingType[payload['wt']]
        self.order_type = OrderType[payload['ot']]
        self.position_side = PositionSide[payload['ps']]
        self.close_all = bool(payload['cp'])
        self.activation_price = float(payload['AP']) if 'AP' in payload.keys() else None
        self.callback_rate = float(payload['cr'])  if 'cr' in payload.keys() else None
        self.realized_profit = float(payload['rp'])

        self.price = None
        if self.original_price:
            self.price = self.original_price
        elif self.average_price:
            self.price = self.average_price
        elif self.stop_price:
            self.price = self.stop_price

    def __str__(self) -> str:
        usd_accum = self.order_filled_accumulated_quantity * self.original_price
        usd = self.original_quantity * self.original_price
        return f"{self.execution_type.value} {self.symbol} {self.side.value} @ {self.price} ({usd_accum:.2f}/{usd:.2f})"


class AccountConfigUpdate(Repr):
    def __init__(self, payload) -> None:
        self.symbol = payload['s'] if 's' in payload.keys() else None
        self.leverage = int(payload['l']) if 'l' in payload.keys() else None
        self.multi_asset_mode = int(payload['j']) if 'j' in payload.keys() else None

    def __str__(self) -> str:
        if self.leverage:
            return f"leverage for {self.symbol} updated to {self.leverage}x"
        if self.multi_asset_mode is not None:
            return f"multi-asset mode is {'enabled' if self.multi_asset_mode else 'disabled'}"

class WsResponse(Repr):
    def __init__(self, payload) -> None:
        try:
            self.event_type = EventType[payload['e']]
        except KeyError:
            return f"Unknown Key {payload['e']}"
        self.event_time = payload['E']

        # self.account_update = None
        # self.margin_call = None
        # self.order_trade_update = None
        # self.account_config_update = None
        # self.strategy_update = None
        # self.grid_update = None
        # self.conditional_order_trigger_reject = None
      
        self.cross_wallet_balance = float(payload['cw']) if 'cw' in payload.keys() else None
        self.position_update = PositionUpdate(payload['p']) if 'p' in payload.keys() else None
        self.order_trade_update = OrderTradeUpdate (payload['o']) if 'o' in payload.keys() else None
        self.account_update = AccountUpdate(payload['a']) if 'a' in payload.keys() else None
        self.account_config_update = AccountConfigUpdate(payload['ac']) if 'ac' in payload.keys() else None
        self.account_info_update = AccountConfigUpdate(payload['ai']) if 'ai' in payload.keys() else None

    def __str__(self) -> str:
        message = f"[{self.event_type.value}]\n"# @ {self.event_time}\n----\n"
        if self.cross_wallet_balance:
            message += f"cross_wallet_balance: {self.cross_wallet_balance}"
        if self.position_update:
            message += repr(self.position_update)
        if self.order_trade_update:
            message += str(self.order_trade_update)
        if self.account_update:
            message += str(self.account_update)
        if self.account_config_update:
            message += repr(self.account_config_update)
        if self.account_info_update:
            message += repr(self.account_info_update)
        return f"```\n{message}```"
