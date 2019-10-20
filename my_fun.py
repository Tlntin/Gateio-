#!/usr/bin/python3
from gateAPI import GateIO
import json
from User_input import user_info
from User_input import other_info

# 获取用户信息
(apiKey, secretKey, btcAddress, API_QUERY_URL, API_TRADE_URL) = user_info()
(UserName, free_b, loced_type, loced_num, Vip_level, refresh_time, base_b) = other_info()

# 创建连接
gate_query = GateIO(API_QUERY_URL, apiKey, secretKey)  # 查询连接
gate_trade = GateIO(API_TRADE_URL, apiKey, secretKey)  # 交易连接


# 定义一个函数用于计算vip等级优惠
def vip_fun(vip):
    if vip == 0:
        maker = 0.2 / 100
        taker = 0.2 / 100

    else:
        maker = (0.195 - 0.01 * vip) / 100
        taker = (0.205 - 0.01 * vip) / 100
    return maker, taker


(Maker, Taker) = vip_fun(Vip_level)


def trade_cost_query():  # 定义一个查询支出的函数,暂未考虑持币总额
    # 获取帐号资金余额
    date0 = gate_trade.balances()
    date1 = json.loads(date0)
    total_money1 = date1["available"]  # 数字货币

    # 可用货币
    money_key_available = list(total_money1.keys())
    b_name_all = money_key_available
    b_name_all.remove('POINT')
    b_name_all.remove(base_b)
    b_types_all = len(b_name_all)  # 计算所有币种
    cost = 0.0  # 初始支出为零,此时币种全为USDT
    cost_qc = 0.0  # 初始支出（去手续费）为零，币种只有USDT
    for z in range(b_types_all):
        data_1 = json.loads(gate_trade.mytradeHistory(b_name_all[z] + "_" + base_b, ""))  # 订单号留空,查询成功后转json字典
        data_trade_1 = data_1['trades']  # 提取交易信息
        data_trade_len_1 = len(data_trade_1)  # 计算交易信息长度
        for ii in range(data_trade_len_1):  # 遍历交易信息历史记录
            if data_trade_1[ii]['type'] == 'buy':  # 假设为买入
                cost = cost + float(data_trade_1[ii]['total'])  # 订单总支出增加
                cost_qc = cost_qc + float(data_trade_1[ii]['total']) * (1 + Taker)  # 附加的手续费
            else:  # 假设为卖出
                cost = cost - float(data_trade_1[ii]['total'])  # 订单总支出减少
                cost_qc = cost_qc - float(data_trade_1[ii]['total']) * (1 - Maker)  # 附加的手续费
    cost = cost - float(gate_query.ticker(loced_type + "_" + base_b)['last']) * loced_num
    cost_qc = cost_qc - float(gate_query.ticker(loced_type + "_" + base_b)['last']) * loced_num
    # 返回订单总支出
    return cost, cost_qc


def total_money_query():  # 定义一个计算钱包总额，以及各类货币实时价格的函数
    # 获取帐号资金余额
    date0 = gate_trade.balances()
    date1 = json.loads(date0)
    total_money1 = date1["available"]  # 可用数字货币
    total_money0 = date1["locked"]  # 锁定数字货币

    # 可交易货币
    money_key_available = list(total_money1.keys())
    money_num_available = list(total_money1.values())
    key_types = len(money_key_available)

    # 不可交易货币(处于挂单状态中，暂时不可交易)
    # money_key_locked = list(total_money0.keys()) 这个和上面的可交易币种名称是一样的
    money_num_locked = list(total_money0.values())

    # 总货币数量
    money_num_all = []
    for i in range(key_types):
        money_num_all.append(float(money_num_available[i]) + float(money_num_locked[i]))  # 将挂单中的币数量加上去

    # 去除货币中的点卡 、USDT、以及数量为零的可用货币
    b_name = []  # 创建数组用于储存可用数字货币名称
    b_num = []  # 创建数组用于储存可用数字货币数量
    base_b_num = 0.0  # 基础货币总数
    base_b_mum_available = 0.0  # 可用基础货币
    for i in range(key_types):
        if money_key_available[i] != 'POINT' and money_key_available[i] != base_b:
            if money_num_all[i] != 0.0:
                b_name.append(money_key_available[i])
                b_num.append(money_num_all[i])

        if money_key_available[i] == base_b:
            base_b_num = money_num_all[i]
            base_b_mum_available = float(money_num_available[i])

    b_types = len(b_name)  # 持仓币种数量

    # 计算钱包余额--------------------------------------------------------
    b_price_last = []  # 建立数组储存币种最近的价格
    total_money = 0.00  # 钱包总余额
    query_b = []  # 待查询的币种交易对
    for n in range(b_types):
        query_b.append(b_name[n] + "_" + base_b)  # 查询的币种交易对
        b_price_last.append(float(gate_query.ticker(query_b[n])['last']))  # 查询币种最近的价格,并且储存
        total_money = total_money + b_price_last[n] * b_num[n]  # 币种最近的价格乘以数量则为可用余额

    # 计算完后还需要加上基础货币(USDT)的数量---------------------------------
    total_money = total_money + base_b_num  # 计算总资产
    print(total_money)

    # 转换为人民币----------------------------------------------------------
    price_cny = gate_query.ticker(base_b + '_CNY')['last']
    total_cny = float(price_cny) * total_money
    # 返回钱包总额(美元)，钱包总额（人民币），币种最近价格
    return total_money, total_cny, b_price_last, base_b_mum_available


def basic_query_fun():  # 自定义一个基础查询函数
    # 获取帐号资金余额
    date0 = gate_trade.balances()
    date1 = json.loads(date0)
    total_money1 = date1["available"]  # 数字货币
    total_money0 = date1["locked"]  # 锁定数字货币

    # 可用货币
    money_key_available = list(total_money1.keys())
    money_num_available = list(total_money1.values())
    key_types = len(money_key_available)

    # 锁仓货币(处于挂单状态中，暂时不可交易)
    money_key_locked = list(total_money0.keys())
    money_num_locked = list(total_money0.values())
    money_num_all = []
    for i in range(key_types):
        money_num_all.append(float(money_num_available[i]) + float(money_num_locked[i]))  # 将挂单中的币数量加上去

    # 去除货币中的点卡 、USDT、以及数量为零的可用货币
    b_name = []  # 创建数组用于储存可用数字货币名称
    b_num = []  # 创建数组用于储存可用数字货币数量
    point_num = 0.0  # 初始点卡数量为0.0
    base_b_num = 0.0  # 基础货币数量为0.0
    for i in range(key_types):
        if money_key_available[i] != 'POINT' and money_key_available[i] != base_b:
            if money_num_all[i] != 0.0:
                b_name.append(money_key_available[i])
                b_num.append(money_num_all[i])

        if money_key_available[i] == 'POINT':
            point_num = money_num_all[i]
        if money_key_available[i] == base_b:
            base_b_num = money_num_all[i]

    b_types = len(b_name)  # 持仓币种数量

    # 计算持仓成本------------------------------------------------
    b_trade_cost = []  # 持仓成本
    for m in range(b_types):
        b_trade_amount = 0.0  # 订单中单次累计持有的币
        cost_1 = 0.0  # 用于储存单个币种的总成本
        data = json.loads(gate_trade.mytradeHistory(b_name[m] + "_" + base_b, ""))  # 订单号留空,查询成功后转json字典
        data_trade = data['trades']  # 提取交易信息
        data_trade_len = len(data_trade)  # 计算交易信息长度

        # 计算单个币种的累计------------------------------------------
        for y in range(data_trade_len):  # 遍历交易信息历史记录
            if data_trade[y]['type'] == 'buy':  # 假设为买入
                b_trade_amount = b_trade_amount + float(data_trade[y]['amount'])  # 计算累计持有的币的数量
                cost_1 = cost_1 + float(data_trade[y]['total']) * (1 + Taker)  # 买入则动态成本增加
            else:  # 假设为卖出
                b_trade_amount = b_trade_amount - float(data_trade[y]['amount'])  # 计算累计持有的币的数量
                cost_1 = cost_1 - float(data_trade[y]['total']) * (1 - Maker)  # 卖出则动态成本减少

            if round(b_trade_amount, 6) == round(b_num[m], 6):  # 增加取6位小数操作，防止小数点过多引起误差
                cost_last = cost_1 / b_trade_amount  # 单个币种的动态成本 / 单个币种的持币数量
                b_trade_cost.append(round(cost_last, 4))  # 添加持仓成本到数组
                break  # 退出该循环，不需进行下面的操作，防止偶然性的满足if要求
    # 返回可用货币名称、数量、点卡、基础币数量、各类币种持仓成本
    return b_name, b_num, point_num, base_b_num, b_trade_cost


def orders_fun():  # 挂单状态函数
    data = json.loads(gate_query.openOrders())  # 获取文本后转字典
    data1 = data["orders"]
    order_len = len(data1)  # 获取订单数量
    order_name = []  # 交易对名称
    order_type = []  # 定义数组储存类型
    initial_rate = []  # 下单价格
    initial_amount = []  # 下单数量
    order_total = []  # 订单总价
    deal_rate = []  # 成交价格
    deal_amount = []  # 成交数量
    fill_rate = []  # 完成率
    order_status = []  # 交易状态
    for i in range(order_len):
        order_name.append(data1[i]['currencyPair'].upper())
        data2 = data1[i]['type']
        if data2 == "sell":
            data2 = "卖出"
        else:
            data2 = "买入"
        order_type.append(data2)
        initial_rate.append(float(data1[i]['initialRate']))
        initial_amount.append(float(data1[i]['initialAmount']))
        order_total.append(float(data1[i]['total']))
        deal_rate.append(float(data1[i]['filledRate']))
        deal_amount.append(float(data1[i]['filledAmount']))
        fill_rate.append(deal_amount[i] / initial_amount[i])
        data3 = data1[i]['status']
        if data3 == "open":
            data3 = "已挂单"
        elif data3 == "cancelled":
            data3 = "已取消"
        else:
            data3 = "已完成"
        order_status.append(data3)
    return order_len, order_name, order_type, initial_rate, initial_amount, order_total, deal_rate, fill_rate, \
        order_status
