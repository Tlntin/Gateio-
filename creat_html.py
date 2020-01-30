import time
import re
import datetime
import pytz
import random
import pandas as pd
from my_fun import *


# 获取用户信息
(api_key, secret_key, btc_address, query_url, trade_url) = user_info()
(user_name, free_b, locked_type, locked_num, vip_level, refresh_time, base_b) = other_info()

if __name__ == '__main__':
    a = os.getcwd()  # 获取当前路径
    b = a + '/' + 'data'
    if not os.path.exists(b):
        os.mkdir(b)
    # 获取vip等级
    maker, taker = vip_fun(vip_level)
    while True:
        func_basic()  # 查询买过的货币
        fun_all_bitcoin()  # 查询当前可用货币
        print('查询当前可用币种成功')
        print('=' * 20)
        print('开始查询币种价格，比较慢')
        query_price()  # 查询币种价格，比较费时
        print('=' * 20)
        print('开始查询币种成本')
        get_hold_cost()  # 计算总成本，比较耗时
        print('查询当前总成本成功')
        get_profit()  # 计算总利润
        # 查询基础货币，可用基础货币，点卡总数，比特币总数
        for i in range(60):
            # 持仓订单数，交易对名称，类型，单价，数量，总价，成交率，挂单状态
            (order_len, order_name, order_type, initial_rate, initial_amount, order_total, fill_rate,
             order_status) = orders_fun()
            base_b_num, base_b_mum_available, point_num, btc_num = func_base_b()
            total_money, total_cny, free_b_price = get_total_money()  # 查询钱包余额，转RMB的价格
            # 计算利润
            # profit, profit_qz, profit_qc, profit_qc_qz
            profit = total_money + point_num - 700  # 考虑点卡,本金700美金
            profit_qz = profit - free_b * free_b_price  # 考虑点卡不考虑赠币
            profit_qc = total_money - 700  # 不考虑点卡
            profit_qc_qz = profit_qc - free_b * free_b_price  # 不考虑点卡不考虑赠币
            print("开始写入html")
            # GEN_HTML = "./data/index.html"  # 路径准备
            GEN_HTML = "/www/wwwroot/www.vbahome.cn/gate/index.html"
            # 获取刷新时间(以北京时间为准)
            fmt = '%Y-%m-%d %H:%M:%S %Z'
            d = datetime.datetime.now(pytz.timezone("Asia/Shanghai"))
            str_time = d.strftime(fmt)
            # 打开文件，准备写入
            f = open(GEN_HTML, 'w', encoding="utf-8")
            f0 = open('./data/html_head.html', 'r')
            message0 = f0.read()
            f.write(message0)  # 写入表头
            # 定义段落信息
            message = """
        <p>数据来源：<a target="_blank" href="https://www.gateio.life">Gateio交易所</a></p>
        <p>数据刷新时间:%s</p>
        <h3>持币情况</h3>
            """ % str_time
            f.write(message)
            df = pd.read_csv('./data/基础数据.csv', encoding='utf-8-sig')
            df.sort_values(by='收益', inplace=True)
            df = round(df, 3)
            df2 = df[['货币名称', '货币数量', '持仓成本', '持仓成本价', '货币价格', '收益率', '收益']]
            df2.to_html('./data/基础表格.html', index=None)
            f2 = open('./data/基础表格.html', 'r', encoding='utf-8')
            message2 = f2.read()
            p = re.compile(r"<td>([A-Z]{2,4})</td>")
            # 增加超链接
            result = p.findall(message2)
            for iii in result:
                message2 = p.sub('<td><a target="_blank" href="https://www.gateio.life/trade/{0}_USDT">{0}</a></td>'\
                                 .format(iii), message2, count=1)
            # 为负数增加红色显示
            p2 = re.compile(r"<td>(-[0-9].{1,8})</td>")
            result2 = p2.findall(message2)
            for mm in result2:
                message2 = p2.sub('<td><span style="color:#FF0000">{}</span></td>'.format(mm), message2, count=1)
            f.write(message2)
            message3 = ''
            # 写入挂单情况
            if order_len != 0:  # 如果当前存在挂单
                message4 = """
                </tr>
            </table>
                <h3>挂单情况</h3>
            <table border="1" cellspacing="0">
                <tr>"""
                message3 = message3 + message4
                # 写入挂单情况
                message5 = """
                    <th>交易对</th>
                    <th>类型</th>
                    <th>单价</th>
                    <th>数量</th>
                    <th>总价</th>
                    <th>成交率</th>
                    <th>状态</th>
                """
                message3 = message3 + message5
                for xx in range(order_len):
                    message6 = """
                </tr>
                <tr>
                    <td><a target="_blank" href="https://www.gateio.life/trade/%s">%s</a></td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%.2f%%</td>
                    <td>%s</td>
                """ % (order_name[xx], order_name[xx], order_type[xx], str(initial_rate[xx]), str(initial_amount[xx]),
                       str(order_total[xx]), fill_rate[xx]*100, order_status[xx])
                    message3 = message3 + message6
                    f.write(message3)
                    message7 = """
                </tr>
            </table>
                    """
                    f.write(message7)
                    print('开始更新币种成本')
                    get_hold_cost()  # 计算总成本，比较耗时
                    print('更新当前总成本成功')
                    get_profit()  # 计算总利润
                    # 写入情况信息
            message8 = """
       <p>目前钱包总额为：<strong>%.2f</strong>(美元折算) &#9||&#9 <strong>%.2f</strong>(人民币折算)</p>
       <p>比特币数量：<strong>%.4f</strong></p>
       <p>点卡数量: <strong>%.2f</strong></p>
       <p>总的%s数量：<strong>%.2f</strong>&#9||&#9可用%s数量：<strong>%.2f</strong></p>
       <h3>技术分析</h3>
       <p>**<a target="_blank" href="will/index.html">货币预测</a>**<--分割线-->**<a target="_blank" href="will/index2.html">股票预测</a>**</p>
           """ % (total_money, total_cny, btc_num, point_num, base_b, base_b_num, base_b, base_b_mum_available)
            f.write(message8)
            # 开始计算累计收益
            message9 = """
        <h3>累计收益</h3>
        <table>
            <tr>
                <th colspan="4">总收益(单位：美元)</th>
            </tr>
            <tr>
                <td colspan="2">考虑点卡</td>
                <td colspan="2">不考虑点卡</td>
            </tr>
            <tr>
                <td>含赠币</td>
                <td>不含赠币</td>
                <td>含赠币</td>
                <td>不含赠币</td>
            </tr>
            <tr>
                <td>%.4f</td>
                <td>%.4f</td>
                <td>%.4f</td>
                <td>%.4f</td>
            </tr>
        </table>
        <!--熊市暂不开启
        <h3><span class="blue-text">加密货币筛选器</span></h3>
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <div class="tradingview-widget-copyright"><a href="https://cn.tradingview.com/crypto-screener/" rel="noopener"
           target="_blank"></a>由Tlntln提供</div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-screener.js" async>
          {
          "width": 1100,
          "height": 512,
          "defaultColumn": "overview",
          "defaultScreen": "general",
          "market": "crypto",
          "showToolbar": true,
          "colorTheme": "light",
          "locale": "zh_CN"
        }
          </script>
        </div>
        -->
        <h3>开源链接</h3>
        <p>跳转<a target="_blank" href="https://github.com/Tlntin/Gateio-">github</a></p>
                            """ % (profit, profit_qz, profit_qc, profit_qc_qz)
            f.write(message9)
            # 写入Html的最后部分，加入手机端自适应大小
            message_foot = """
    </body>
        <script src="001.js" type="text/javascript"></script>
</html>
            """
            f.write(message_foot)
            print('写入html成功', '\n')
            f.close()
            time.sleep(5)
            print('更新币种价格，比较慢，请耐心等待')
            query_price()  # 查询币种价格，比较费时
            time.sleep(random.random() * 2)
            print('更新总利润')
            get_profit()
            time.sleep(random.random() * 2)
