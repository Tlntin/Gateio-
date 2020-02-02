from user_input import user_info, other_info
from gate_api import GateIO
import time
import os
import pandas as pd
import numpy as np
import random
# 获取用户信息
(api_key, secret_key, btc_address, query_url, trade_url) = user_info()
(user_name, free_b, locked_type, locked_num, vip_level, refresh_time, base_b) = other_info()

# 创建连接
gate_query = GateIO(query_url, api_key, secret_key)  # 查询连接
gate_trade = GateIO(trade_url, api_key, secret_key)  # 交易连接


def func_basic():
    """
    创建一个基础查询函数
    :return: 返回总的货币数量，可用货币数量，总的货币名称
    """
    for i in range(4):
        try:
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
            my_dict = {}
            my_dict['货币名称'] = money_key_available
            my_dict['货币总量'] = money_num_all
            my_dict['可用数量'] = money_num_available
            df = pd.DataFrame({'货币名称': money_key_available, '货币数量': money_num_all, '可交易数量': money_num_available})
            df.to_csv('./data/买过的货币.csv', encoding='utf-8', index=None)
            break
        except Exception as err:
            print(err)
            time.sleep(10)


def fun_all_bitcoin():
    """
    定义一个计算所有持仓币种的函数
    :return: 持仓币种名称，持仓币种数量，总基础货币，可用基础货币
    """
    df = pd.read_csv('./data/买过的货币.csv', encoding='utf-8')
    aa = df[df['货币名称'].isin(['POINT', 'USDT'])].index.values  # 删除点卡和USDT
    df.drop(aa, inplace=True)
    bb = df[df['货币数量'] < 0.001].index.values  # 删除货币数量小于0.001的币种
    df.drop(bb, inplace=True)
    df.to_csv('./data/当前可用货币.csv', encoding='utf-8-sig', index=None)


def func_base_b():
    """
    定义一个函数用于查询基础货币余额的
    :return:返回总的基础币，可用基础币
    """
    df = pd.read_csv('./data/买过的货币.csv', encoding='utf-8')
    base_b_num = df[df['货币名称'] == base_b]['货币数量'].values[0]
    base_b_mum_available = df[df['货币名称'] == base_b]['可交易数量'].values[0]
    point_num = df[df['货币名称'] == 'POINT']['货币数量'].values[0]
    btc_num = df[df['货币名称'] == 'BTC']['货币数量'].values[0]
    return base_b_num, base_b_mum_available, point_num, btc_num


def query_price():
    """
    此函数用于查询币种价格，并且储存
    :return:
    """
    df = pd.read_csv('./data/当前可用货币.csv', encoding='utf-8')
    b_name_list = df['货币名称'].values.tolist()
    b_name_price_list = []
    for b_name in b_name_list:
        b_name_price = 0
        for i in range(5):  # 循环5次，防止出错
            try:
                b_name_price = float(gate_query.ticker(b_name + '_' + base_b)['last'])
                time.sleep(random.random()/3 + 0.2)
                break
            except Exception as err:
                print(err)
                time.sleep(5)
        b_name_price_list.append(b_name_price)
        print('已查询{}的最新价格:{:.4f}'.format(b_name, b_name_price))
    df['货币价格'] = b_name_price_list
    df.to_csv('./data/当前可用货币.csv', encoding='utf-8-sig', index=None)


def get_total_money():
    """
    用于计算钱包总额,以及币种最近价格
    这个函数也比较消耗资源，建议不要长期使用
    :return: 返回钱包总额(美元)，钱包总额（人民币）
    """
    df = pd.read_csv('./data/当前可用货币.csv', encoding='utf-8')
    df2 = pd.read_csv('./data/买过的货币.csv', encoding='utf-8')
    total_money = (df['货币数量'] * df['货币价格']).sum()
    base_b_num = df2[df2['货币名称'] == base_b]['货币数量'].values[0]
    free_b_price = df[df['货币名称'] == 'GT']['货币价格'].values[0]
    total_cny = 0
    # 计算完后还需要加上基础货币(USDT)的数量---------------------------------
    total_money = round(total_money + base_b_num, 2)  # 计算总资产
    # 转换为人民币----------------------------------------------------------
    for i in range(4):
        try:
            price_cny = gate_query.ticker(base_b + '_CNY')['last']
            total_cny = round(float(price_cny) * total_money, 2)
            print('总的美金{}，总的人民币{}'.format(total_money, total_cny))
            break
        except Exception as err:
            print(err)
            time.sleep(5)
            get_total_money()
    return total_money, total_cny, free_b_price


def get_one_cost(bit_name, bit_amount):
    """
    计算单个币种的总成本，成本价格
    :param bit_name: 币种名称
    :param bit_amount: 币的数量
    :return: 币种总成本，币种成本价
    """
    aa = os.getcwd()
    bb = aa + '/持仓价格'
    if not os.path.exists(bb):
        os.mkdir(bb)
    b_total_cost, b_cost_price = 1, 1
    for i in range(4):
        try:
            data_trade = gate_trade.mytradeHistory(bit_name + "_" + base_b, '')['trades']  # 提取交易信息
            trade_list = [[trade['amount'], trade['type'],
                           trade['total'], trade['point_fee'], trade['date']] for trade in data_trade]
            df2 = pd.DataFrame(trade_list, columns=['amount', 'type', 'total', 'point_fee', 'date'], dtype='float')
            df2['type'] = df2['type'].map({'sell': -1, 'buy': 1})
            df2['amount_cumsum'] = (df2['type'] * df2['amount']).cumsum()  # 累计求和
            df2['compare'] = df2['amount_cumsum'] - bit_amount
            min_compare = abs(df2['compare']).min()
            min_compare_index = np.where(abs(df2['compare']) == min_compare)
            index = min_compare_index[0][0]
            # df2.to_csv('./持仓价格/' + bit_name + '持仓成本.csv', index=None, encoding='utf-8') # 导出文件，建议不用导出
            b_total_cost = (
                        df2.iloc[:index + 1]['total'] * df2.iloc[:index + 1]['type'] + df2.iloc[:index + 1]['point_fee']).sum()
            b_cost_price = b_total_cost / bit_amount
            print('{}的成本价为：{:.4f}'.format(bit_name, b_cost_price))
            break
        except Exception as err:
            print(err)
            time.sleep(5)
    return b_total_cost, b_cost_price


def get_hold_cost():
    """
    计算所有币种的持仓成本，后期可能会拆分
    :return:
    """
    df = pd.read_csv('./data/当前可用货币.csv', encoding='utf-8')
    b_name_list = df['货币名称'].values.tolist()
    b_amount_list = df['货币数量'].values.tolist()
    total_cost_list = []  # 总成本
    cost_price_list = []  # 成本价
    for b_name, b_amount in zip(b_name_list, b_amount_list):
        try:
            b_total_cost, b_cost_price = get_one_cost(b_name, b_amount)
            time.sleep(random.random()/3 + 0.2)
            total_cost_list.append(b_total_cost)
            cost_price_list.append(b_cost_price)
        except Exception as err:
            print(err)
            time.sleep(5)
            get_hold_cost()
    df['持仓成本'] = total_cost_list
    df['持仓成本价'] = cost_price_list
    df.to_csv('./data/当前可用货币.csv', encoding='utf-8', index=None)


def get_profit():
    """
    用于计算当前收益率
    :return:
    """
    df = pd.read_csv('./data/当前可用货币.csv', encoding='utf-8')
    df['收益'] = (df['货币价格'] - df['持仓成本价']) * df['货币数量']
    df['收益率'] = round((df['收益'] / df['持仓成本']), 4)
    df['收益率'] = df['收益率'].apply(lambda x: format(x, '.2%'))
    df.to_csv('./data/基础数据.csv', encoding='utf-8-sig', index=None)


def orders_fun():
    """
    # 挂单状态函数
    :return:
    """
    order_len, order_name, order_type, initial_rate, initial_amount, order_total, fill_rate,\
    order_status = ('', '', '', '', '', '', '', '')
    for i in range(4):
        try:
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
                break
        except Exception as err:
            print(err)
            time.sleep(10)
    return order_len, order_name, order_type, initial_rate, initial_amount, order_total, fill_rate, order_status


def creat_html(i, message):
    """
    定义一个函数用于创建html
    :return: 没有返回
    """
    # 路径选择
    # html = 'will/{}.html'
    html = '//www/wwwroot/www.vbahome.cn/gate/will/{}.html'
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


if __name__ == '__main__':
    a = os.getcwd()  # 获取当前路径
    b = a + '/' + 'data'
    if not os.path.exists(b):
        os.mkdir(b)
    # func_basic()
    # fun_all_bitcoin()
    # func_base_b()
    # trade_cost_query()
    # trade_cost_query()
    # query_price()
    # get_total_money()
    # get_hold_cost()
    get_profit()
