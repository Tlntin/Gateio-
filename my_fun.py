from user_input import user_info, other_info
from gate_api import GateIO
# 获取用户信息
(api_key, secret_key, btc_address, query_url, trade_url) = user_info()
(user_name, free_b, locked_type, loced_num, vip_level, refresh_time, base_b) = other_info()

# 创建连接
gate_query = GateIO(query_url, api_key, secret_key)  # 查询连接
gate_trade = GateIO(trade_url, api_key, secret_key)  # 交易连接


def vip_fun(vip):
    """
    此函数用于计算vip等级优惠
    :param vip: 需要输入vip等级
    :return: 返回Taker,Maker费率
    """
    if vip == 0:
        maker = 0.2 / 100
        taker = 0.2 / 100

    else:
        maker = (0.195 - 0.01 * vip) / 100
        taker = (0.205 - 0.01 * vip) / 100
    return maker, taker


def decimal_n(decimal):
    """
    定义一个查询小数后多少位的函数
    :param decimal: 需要给出小数
    :return: 返回小数多少位
    """
    n = len(str(decimal).split(".")[1])
    print(n)
    return n


def fun_num_raise(num, t):
    """
    定义一个小数位最后一位增加n的函数
    :param num: 数字
    :param t: 增加多少
    :return: 返回增加的值
    """
    n = decimal_n(num)
    s_sum = num + 10**(-n)*t
    s_sum = round(s_sum, n)  # 取n位小数
    return s_sum


def func_basic():
    """
    创建一个基础查询函数
    :return: 返回总的货币数量，可用货币数量，总的货币名称
    """
    # 获取帐号资金余额
    date = gate_trade.balances()
    total_money1 = date["available"]  # 可用数字货币
    total_money0 = date["locked"]  # 锁定数字货币
    # 可交易货币
    money_key_available = list(total_money1.keys())
    money_num_available = list(total_money1.values())
    key_types = len(money_key_available)

    # 不可交易货币(处于挂单状态中，暂时不可交易)
    money_num_locked = list(total_money0.values())

    # 总货币数量
    money_num_all = []
    for i in range(key_types):
        money_num_all.append(float(money_num_available[i]) + float(money_num_locked[i]))  # 将挂单中的币数量加上去
    return money_num_all, money_num_available, money_key_available


def fun_all_bitcoin():
    """
    定义一个计算所有持仓币种的函数
    :return: 持仓币种名称，持仓币种数量，总基础货币，可用基础货币
    """
    (money_num_all, money_num_available, money_key_available) = func_basic()
    key_types = len(money_key_available)
    b_name = []  # 创建数组用于储存可用数字货币名称
    b_num = []  # 创建数组用于储存可用数字货币数量
    for i in range(key_types):
        # 去除货币中的点卡 、USDT、以及数量为零的可用货币
        if money_key_available[i] not in ['POINT', base_b]:
            if money_num_all[i] >= 0.001:  # 大于0.001才录入
                b_name.append(money_key_available[i])
                b_num.append(money_num_all[i])
    return b_name, b_num


def func_base_b():
    """
    定义一个函数用于查询基础货币余额的
    :return:返回总的基础币，可用基础币
    """
    (money_num_all, money_num_available, money_key_available) = func_basic()
    key_types = len(money_key_available)
    base_b_num = 0.0  # 总基础货币
    base_b_mum_available = 0.0  # 可用基础货币
    point_num = 0.0  # 可用点卡数量
    btc_num = 0.0
    for i in range(key_types):
        if money_key_available[i] == base_b:
            base_b_num = float(money_num_all[i])
            base_b_mum_available = float(money_num_available[i])
        if money_key_available[i] == 'POINT':
            point_num = float(money_num_all[i])

        if money_key_available[i] == 'BTC':
            btc_num = float(money_num_all[i])
    return base_b_num, base_b_mum_available, point_num, btc_num


def trade_cost_query():
    """
    定义一个查询支出的函数,暂未考虑持币总额
    注意：这个函数消耗比较大，建议不要经常运行
    :return:返回总成本，总成本去除手续费
    """
    # 获取帐号资金余额
    date = gate_trade.balances()
    total_money1 = date["available"]  # 数字货币
    # 获取vip等级
    maker, taker = vip_fun(vip_level)
    # 可用货币
    money_key_available = list(total_money1.keys())
    b_name_all = money_key_available
    b_name_all.remove('POINT')
    b_name_all.remove(base_b)
    b_types_all = len(b_name_all)  # 计算所有币种
    cost = 0.0  # 初始支出为零,此时币种全为USDT
    cost_qc = 0.0  # 初始支出（去手续费）为零，币种只有USDT
    for z in range(b_types_all):
        data_1 = gate_trade.mytradeHistory(b_name_all[z] + "_" + base_b, "")  # 订单号留空,查询成功后转json字典
        data_trade_1 = data_1['trades']  # 提取交易信息
        data_trade_len_1 = len(data_trade_1)  # 计算交易信息长度
        for ii in range(data_trade_len_1):  # 遍历交易信息历史记录
            if data_trade_1[ii]['type'] == 'buy':  # 假设为买入
                cost = cost + float(data_trade_1[ii]['total'])  # 订单总支出增加
                cost_qc = cost_qc + float(data_trade_1[ii]['total']) * (1 + taker)  # 附加的手续费
            else:  # 假设为卖出
                cost = cost - float(data_trade_1[ii]['total'])  # 订单总支出减少
                cost_qc = cost_qc - float(data_trade_1[ii]['total']) * (1 - maker)  # 附加的手续费
    cost = cost - float(gate_query.ticker(locked_type + "_" + base_b)['last']) * loced_num
    cost_qc = cost_qc - float(gate_query.ticker(locked_type + "_" + base_b)['last']) * loced_num
    # 返回订单总支出
    return cost, cost_qc


def get_total_money():
    """
    用于计算钱包总额,以及币种最近价格
    这个函数也比较消耗资源，建议不要长期使用
    :return: 返回钱包总额(美元)，钱包总额（人民币），币种最近价格
    """
    # 获取可用货币名称以及数量
    b_name, b_num = fun_all_bitcoin()
    b_types = len(b_name)
    # 获取总的稳定币数量
    base_b_num, base_b_mum_available, point_num, btc_num = func_base_b()
    # 计算钱包余额--------------------------------------------------------
    b_price_last = []  # 建立数组储存币种最近的价格
    total_money = 0.00  # 钱包总余额
    query_b = []  # 待查询的币种交易对
    b_hold = []  # 总持仓
    for n in range(b_types):
        query_b.append(b_name[n] + "_" + base_b)  # 查询的币种交易对
        b_price_last.append(float(gate_query.ticker(query_b[n])['last']))  # 查询币种最近的价格,并且储存
        b_hold.append(b_price_last[n] * b_num[n])  # 计算总持仓
        total_money = total_money + b_price_last[n] * b_num[n]  # 币种最近的价格乘以数量则为可用余额

    # 计算完后还需要加上基础货币(USDT)的数量---------------------------------
    total_money = total_money + base_b_num  # 计算总资产

    # 转换为人民币----------------------------------------------------------
    price_cny = gate_query.ticker(base_b + '_CNY')['last']
    total_cny = float(price_cny) * total_money
    return total_money, total_cny, b_price_last, b_hold


def hold_cost():
    """
    定义一个计算持仓成本的函数
    :return:返回各个币种的持仓成本
    """
    # 获取vip等级
    maker, taker = vip_fun(vip_level)
    # 获取可用货币名称以及数量
    b_name, b_num = fun_all_bitcoin()
    b_types = len(b_name)   # 持仓币种数量
    # 计算持仓成本------------------------------------------------
    b_trade_cost = []  # 持仓成本
    for m in range(b_types):
        b_trade_amount = 0.0  # 订单中单次累计持有的币
        cost_1 = 0.0  # 用于储存单个币种的总成本
        data = gate_trade.mytradeHistory(b_name[m] + "_" + base_b, "")  # 订单号留空,查询成功后转json字典
        data_trade = data['trades']  # 提取交易信息
        data_trade_len = len(data_trade)  # 计算交易信息长度

        # 计算单个币种的累计------------------------------------------
        for y in range(data_trade_len):  # 遍历交易信息历史记录
            if data_trade[y]['type'] == 'buy':  # 假设为买入
                b_trade_amount = b_trade_amount + float(data_trade[y]['amount'])  # 计算累计持有的币的数量
                cost_1 = cost_1 + float(data_trade[y]['total']) * (1 + taker)  # 买入则动态成本增加
            else:  # 假设为卖出
                b_trade_amount = b_trade_amount - float(data_trade[y]['amount'])  # 计算累计持有的币的数量
                cost_1 = cost_1 - float(data_trade[y]['total']) * (1 - maker)  # 卖出则动态成本减少
            # 只要满足订单累计成本为正，且订单累计数量与目前的持仓数量近似
            if cost_1 > 0 and abs(round(b_num[m], 4) - round(b_trade_amount, 4)) <= 0.001:  # 精度降低为3位，防红包
                cost_last = cost_1 / b_trade_amount
                b_trade_cost.append(round(cost_last, 4))  # 添加持仓成本到数组
                break
        # 如果循环结束还没找到成本价，那就以最后一个价格为成本价
        else:
            if b_trade_amount != 0:
                cost_last = cost_1 / b_trade_amount
            z = 1
            # 如果持仓成本小于零则进入循环
            while cost_last <= 0:
                if data_trade[y - z]['type'] == 'sell':
                    cost_1 = cost_1 + float(data_trade[y - z]['total']) * (1 - maker)  # 加上上一笔卖的收入
                    b_trade_amount = b_trade_amount + float(data_trade[y - z]['amount'])  # 加上最后一笔卖的数量
                    cost_last = cost_1 / b_trade_amount  # 重新计算持仓成本
                else:
                    cost_1 = cost_1 - float(data_trade[y - z]['total']) * (1 + taker)  # 减去上一笔买的支出
                    b_trade_amount = b_trade_amount - float(data_trade[y - z]['amount'])  # 减去上一笔买的数量
                    cost_last = cost_1 / b_trade_amount  # 重新计算持仓成本
                z = z + 1
            b_trade_cost.append(round(cost_last, 4))  # 添加持仓成本到数组
    return b_trade_cost


def orders_fun():
    """
    # 挂单状态函数
    :return:
    """
    data = gate_query.openOrders()
    data1 = data["orders"]
    order_len = len(data1)  # 获取订单数量
    order_name = []  # 交易对名称
    order_type = []  # 定义数组储存类型
    initial_rate = []  # 下单价格
    initial_amount = []  # 下单数量
    order_total = []  # 订单总价
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
    return order_len, order_name, order_type, initial_rate, initial_amount, order_total, fill_rate, order_status


def creat_html(i, message):
    """
    定义一个函数用于创建html
    :return: 没有返回
    """
    # 路径选择
    html = 'will/{}.html'
    with open(html.format(i), 'w', encoding='utf-8') as f:
        f.write(message)


def fun_will(interval, name, word=''):
    """
    这个函数是用来预测未来涨势的
    :param word: 默认的显示值，默认显示为空
    :param interval: 时间间隔，可以选1D, 4h,1h
    :param name:加密货币名称，可以用交易所：数字货币交易对，也可以直接用数字数字货币交易对
    :return:返回一个网站
    """
    html = """
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5,
             maximum-scale=2.0, user-scalable=yes" /> 
        <title>%s</title>
        <link rel="icon" href="https://www.gateio.co/images/apple-touch-icon-120x120.png"/>
    </head>
    <body>
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <div class="tradingview-widget-copyright"><a href="https://cn.tradingview.com/symbols/%s/technicals/" rel="noopener" target="_blank">
          <span class="blue-text">%s</span></a></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {
          "interval": "%s",
          "width": 425,
          "colorTheme": "light",
          "isTransparent": false,
          "height": 450,
          "symbol": "%s",
          "showIntervalTabs": true,
          "locale": "zh_CN"
          }
          </script>
        </div>
        <!-- TradingView Widget END -->
    </body>
            <script type="text/javascript">
            var phoneWidth =  parseInt(window.screen.width);
            var phoneScale = phoneWidth/640;
            var ua = navigator.userAgent;
            if (/Android (\d+\.\d+)/.test(ua)){
                var version = parseFloat(RegExp.$1);
                if(version>2.3){
                    document.write('<meta name="viewport" content="width=640,
                        minimum-scale = '+phoneScale+', 
                        maximum-scale = '+phoneScale+', 
                        target-densitydpi=device-dpi">');
                }else{
                    document.write('<meta name="viewport" content="width=640, 
                    target-densitydpi=device-dpi">');
                }
            } else {
                document.write('<meta name="viewport" content="width=640, user-scalable=no, 
                target-densitydpi=device-dpi">');
            }
        </script>
</html>
    """ % (word, name, word, interval, name)
    return html
