import json
import hashlib
import hmac
from urllib import parse,request


def get_sign(params, secret_key):
    """
    这个函数用于对公钥，密钥签名
    :param params: 需要post的请求数据
    :param secret_key: 你的私钥
    :return:返回一个加密的信息
    """
    b_secret_key = bytes(secret_key, encoding='utf8')

    sign = ''
    for key in params.keys():
        value = str(params[key])
        sign += key + '=' + value + '&'
    b_sign = bytes(sign[:-1], encoding='utf8')

    my_sign = hmac.new(b_secret_key, b_sign, hashlib.sha512).hexdigest()
    return my_sign


def http_get(base_url, resource, params=''):
    """
    构建http get请求
    :param base_url:请求的主域名
    :param resource:请求的二级域名资源
    :param params:需要post的请求数据
    :return:返回请求结果
    """
    url = base_url + resource + '/' + params
    res = request.urlopen(url, timeout=15)
    data = res.read().decode('utf-8')
    data = json.loads(data)
    return data


def http_post(base_url, resource, params, api_key, secret_key):
    """
    构建http post 请求
    :param base_url: 请求的主域名
    :param resource: 请求的二级域名资源
    :param params: 需要post的请求数据
    :param api_key: api_key
    :param secret_key: 私钥
    :return: 返回一个posst请求
    """
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "KEY": api_key,
        "SIGN": get_sign(params, secret_key)
    }
    url = base_url + resource
    temp_params = parse.urlencode(params).encode()
    req = request.Request(url=url, headers=headers, data=temp_params)
    res = request.urlopen(req, timeout=15)
    data = res.read().decode('utf-8')
    data = json.loads(data)
    return data


# 定义一个类，gateio
class GateIO:
    def __init__(self, base_url, api_key, secret_key):
        """
        类初始化
        :param base_url: 主域名，Http方法
        :param api_key: api_key，公钥
        :param secret_key: 私钥
        """
        self.__url = base_url
        self.__api_key = api_key
        self.__secret_key = secret_key

    # 常规查询***************************************

    # 所有交易对
    def pairs(self):
        url2 = '/api2/1/pairs'
        params = ''
        return http_get(self.__url, resource=url2, params=params)

    # 所有货币
    def coins_info(self):
        url2 = '/api2/1/coininfo'
        params = ''
        return http_get(self.__url, resource=url2, params=params)

    # 市场订单参数
    def marketinfo(self):
        url2 = "/api2/1/marketinfo"
        params = ''
        return http_get(self.__url, resource=url2, params=params)

    # 交易市场详细行情
    def marketlist(self):
        url2 = "/api2/1/marketlist"
        params = ''
        return http_get(self.__url, resource=url2, params=params)

    # 所有交易行情
    def tickers(self):
        url2 = "/api2/1/tickers"
        params = ''
        return http_get(self.__url, resource=url2, params=params)

    # 所有交易对市场深度
    def orderBooks(self):
        url2 = "/api2/1/orderBooks"
        param = ''
        return http_get(self.__url, url2, param)

    # 单项交易行情
    def ticker(self, param):
        url2 = "/api2/1/ticker"
        return http_get(self.__url, url2, param)

    # 单项交易对市场深度
    def orderBook(self, param):
        url2 = "/api2/1/orderBook"
        return http_get(self.__url, url2, param)

    # 历史成交记录
    def tradeHistory(self, param):
        url2 = "/api2/1/tradeHistory"
        return http_get(self.__url, url2, param)

    # 需要用到key的查询**********************

    # 获取帐号资金余额
    def balances(self):
        url2 = "/api2/1/private/balances"
        param = {}
        return http_post(self.__url, url2, param, self.__api_key, self.__secret_key)

    # 获取充值地址
    def depositAddres(self, param):
        url2 = "/api2/1/private/depositAddress"
        params = {'currency': param}
        return http_post(self.__url, url2, params, self.__api_key, self.__secret_key)

    # 获取充值提现历史
    def depositsWithdrawals(self, start, end):
        url2 = "/api2/1/private/depositsWithdrawals"
        params = {'start': start, 'end': end}
        return http_post(self.__url, url2, params, self.__api_key, self.__secret_key)

    # 买入
    def buy(self, currencyPair, rate, amount):
        url2 = "/api2/1/private/buy"
        params = {'currencyPair': currencyPair, 'rate': rate, 'amount': amount}
        return http_post(self.__url, url2, params, self.__api_key, self.__secret_key)

    # 卖出
    def sell(self, currencyPair, rate, amount):
        url2 = "/api2/1/private/sell"
        params = {'currencyPair': currencyPair, 'rate': rate, 'amount': amount}
        return http_post(self.__url, url2, params, self.__api_key, self.__secret_key)

    # 取消订单
    def cancelOrder(self, orderNumber, currencyPair):
        url2 = "/api2/1/private/cancelOrder"
        params = {'orderNumber': orderNumber, 'currencyPair': currencyPair}
        return http_post(self.__url, url2, params, self.__api_key, self.__secret_key)

    # 取消所有订单
    def cancelAllOrders(self, type, currencyPair):
        url2 = "/api2/1/private/cancelAllOrders"
        params = {'type': type, 'currencyPair': currencyPair}
        return http_post(self.__url, url2, params, self.__api_key, self.__secret_key)

    # 获取下单状态
    def getOrder(self, orderNumber, currencyPair):
        url2 = "/api2/1/private/getOrder"
        params = {'orderNumber': orderNumber, 'currencyPair': currencyPair}
        return http_post(self.__url, url2, params, self.__api_key, self.__secret_key)

    # 获取我的当前挂单列表
    def openOrders(self):
        url2 = "/api2/1/private/openOrders"
        params = {}
        return http_post(self.__url, url2, params, self.__api_key, self.__secret_key)

    # 获取我的24小时内成交记录
    def mytradeHistory(self, currencyPair, orderNumber):
        url2 = "/api2/1/private/tradeHistory"
        params = {'currencyPair': currencyPair, 'orderNumber': orderNumber}
        return http_post(self.__url, url2, params, self.__api_key, self.__secret_key)

    # 提现
    def withdraw(self, currency, amount, address):
        url2 = "/api2/1/private/withdraw"
        params = {'currency': currency, 'amount': amount, 'address': address}
        return http_post(self.__url, url2, params, self.__api_key, self.__secret_key)
