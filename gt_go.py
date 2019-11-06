#!/usr/bin/python3
import time
import datetime
from gateAPI import GateIO
from User_input import user_info,other_info
from my_fun import basic_query_fun, trade_star, func2

# 获取用户信息
(apiKey, secretKey, btcAddress, API_QUERY_URL, API_TRADE_URL) = user_info()
(UserName, free_b, loced_type, loced_num, Vip_level, refresh_time, base_b) = other_info()

# 创建连接
gate_query = GateIO(API_QUERY_URL, apiKey, secretKey)  # 查询连接
gate_trade = GateIO(API_TRADE_URL, apiKey, secretKey)  # 交易连接

today = datetime.date.today()
f_name = str(today)+"操作日志.txt"
f = open(f_name, 'w', encoding="utf-8")
f.write(str(today))
f.close()

m = 15  # 15分钟查询一次买入或者卖出
while True:
    try:
        # 可用货币名称、数量、点卡、基础币总量、可用基础币、各类币种持仓成本
        (b_name, b_num, point_num, base_b_num, base_b_mum_available2, b_trade_cost, btc_num) = basic_query_fun()
        time.sleep(2)
        b_name_len = len(b_name)
        print("可用基础货币为：", base_b_mum_available2)

        for i in range(b_name_len):
            data = trade_star(b_name[i], m)
            print(data)
            if data == "buy":
                print(b_name[i])
                buy_rate0 = func2(float(gate_query.ticker(b_name[i] +"_" + base_b)['last']), 2)  # 对最近成交价取三个点
                data2 = gate_query.orderBook(b_name[i] +"_" + base_b)['bids']  # 查一下买方交易最高价
                buy_rate1 = func2(float(data2[0][0]), 2)  # 第一个就是买方最高价,对它加价2个点
                buy_rate = min(buy_rate0, buy_rate1)  # 两者取最低
                buy_amount = round(base_b_mum_available2 * 0.25/buy_rate, 4)  # 1/4仓买入，取4位小数
                # 买入(类型，价格，数量)
                print(gate_trade.buy(b_name[i] +"_" + base_b, str(buy_rate), str(buy_amount)))
                f = open(f_name, 'a', encoding="utf-8")
                message = """
                买入%s, 价格：%s  ，数量：%s ；
                """ % (b_name[i], str(buy_rate), str(buy_amount))
                f.write(message)
                f.close()
                print("买入成功，等待%d分钟" % (120/m))
                time.sleep(7200/m)  # 防止持续下单
                print(gate_trade.cancelAllOrders('1', b_name[i] +"_" + base_b))  # 下单失败则取消
            if data == "sale":
                print(b_name[i])
                sell_rate0 = func2(float(gate_query.ticker(b_name[i] +"_" + base_b)['last']), -2)  # 降2个点卖出
                data2 = gate_query.orderBook(b_name[i] +"_" + base_b)['asks']  # 查一下卖方交易最低价
                data2_len = len(data2)
                sell_rate1 = func2(float(data2[data2_len-1][0]), -2)  # 最后一个是卖方最低价,降低两个点
                sell_rate = min(sell_rate0, sell_rate1)  # 两者取低价
                sell_amount = round(b_num[i] * 0.3, 4)  # 卖出30%,取4位小数)
                # 卖出（(类型，价格，数量)）
                print(gate_trade.sell(b_name[i] +"_" + base_b, sell_rate, str(sell_amount)))
                f = open(f_name, 'a', encoding="utf-8")
                message = """
                卖出%s, 价格：%s  ，数量：%s ；
                """ % (b_name[i], str(sell_rate), str(sell_amount))
                f.write(message)
                f.close()
                print("买入成功，等待%d分钟" % (120 / m))
                time.sleep(7200 / m)  # 防止持续下单
                print(gate_trade.cancelAllOrders('0', b_name[i] + "_" + base_b))  # 下单失败则取消
            else:
                print(b_name[i])
                time.sleep(5)
                print("*********************************")
        m = m * 2
        if m > 60:
            m = 15
        print("查询结束，等待%d秒" % (3600/m))
        time.sleep(3600/m)  # 等会再查，防止出问题
    except Exception as err:
        print(err)