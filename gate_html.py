from user_input import user_info, other_info
import time
import datetime
import random
import pytz
from gate_api import GateIO
from my_fun import fun_all_bitcoin, vip_fun, get_total_money, func_base_b, trade_cost_query, hold_cost
from my_fun import orders_fun
# 获取用户信息
(api_key, secret_key, btc_address, query_url, trade_url) = user_info()
(user_name, free_b, locked_type, loced_num, vip_level, refresh_time, base_b) = other_info()

# 创建连接
gate_query = GateIO(query_url, api_key, secret_key)  # 查询连接
# 获取vip等级
maker, taker = vip_fun(vip_level)

# 开始循环，生成Html文件--------------------------
while True:
    try:
        # 从订单表中查询总支出、总支出含手续费
        print("首次运行比较慢，请耐心等待几十秒")
        (cost, cost_qc) = trade_cost_query()
        print('准备写入Html,已准备10%')
        time.sleep(1)  # 等1秒
        # 计算持仓成本
        b_trade_cost = hold_cost()
        # 定义一个for循环，用于实时更新数据
        for i in range(30):
            # 查询所有货币
            b_name, b_num = fun_all_bitcoin()
            print('准备写入Html,已准备20%')
            time.sleep(random.random())
            # 查询钱包，总美金，转人民币，币种最近价格,总持仓
            total_money, total_cny, b_price_last, b_hold = get_total_money()
            print('准备写入Html,已准备30%')
            time.sleep(random.random())
            # 持仓订单数，交易对名称，类型，单价，数量，总价，成交率，挂单状态
            (order_len, order_name, order_type, initial_rate, initial_amount, order_total, fill_rate,
             order_status) = orders_fun()
            print('准备写入Html,已准备50%')
            time.sleep(random.randint(1, 2))  # 等1-2秒
            # 查询基础货币
            print('准备写入Html,已准备60%')
            base_b_num, base_b_mum_available, point_num, btc_num = func_base_b()
            # 总利润=商品折算后的总金额-商品订单总成本(不考虑手续费)=总金额 - 基础代币- 订单总成本 + 比特币数量
            profit = total_money - base_b_num
            time.sleep(random.randint(1, 2))  # 等1-2秒
            profit_qc = total_money - base_b_num - cost_qc
            time.sleep(random.randint(1, 2))  # 等1-2秒
            profit_qz = profit - float(gate_query.ticker("gt_usdt")['last']) * free_b
            print('准备写入Html,已准备80%')
            time.sleep(random.randint(1, 2))  # 等1-2秒
            profit_qc_qz = profit_qc - float(gate_query.ticker("gt_usdt")['last']) * free_b
            print('准备写入Html,已准备100%')
            # 开始生成html文件--------------------------------------------------
            print("开始写入html,进度0%")
            GEN_HTML = "index.html"  # 路径准备
            # 获取刷新时间(以北京时间为准)
            fmt = '%Y-%m-%d %H:%M:%S %Z'
            d = datetime.datetime.now(pytz.timezone("Asia/Shanghai"))
            str_time = d.strftime(fmt)
            # 打开文件，准备写入
            f = open(GEN_HTML, 'w', encoding="utf-8")

            # 定义表头信息
            message = """
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5,
             maximum-scale=2.0, user-scalable=yes" /> 
        <title>我的钱包 </title>
        <link rel="icon" href="https://www.gateio.co/images/apple-touch-icon-120x120.png"/>
    </head>
    <body>
        <p>数据来源：<a target="_blank" href="https://www.gateio.org">Gateio交易所</a></p>
        <p>数据刷新时间:%s</p>
        <p>用户名：%s &#9||&#9 VIP等级：<font color="red">VIP%d</font></p>
        <p>费率：Maker：%.3f%% &#9||&#9 Taker：%.3f%%</p>
        <h3>持币情况</h3>
        <table border="1" cellspacing="0">
              <tr>
                <th width="62"; style="text-align: center">币种</th>  
            """ % (str_time, user_name, vip_level, round(100*maker, 3), round(100*taker, 3))
            # 写入持有币种类别信息，不包括点卡和USDT
            for x in range(len(b_name)):
                message1 = """
                <td width="80"; style="text-align: center"><a target="_blank" href="https://www.gateio.org/trade/%s_%s">%s</a></td>    
                """ % (b_name[x], base_b, b_name[x])
                message = message + message1
            # 写入币种数量信息
            message2 = """
            </tr>
            <tr>
                <th width="62"; style="text-align: center">数量</th>
            """
            message = message + message2
            # 写入币种数量
            for y in range(len(b_name)):
                message3 = """
                <td width="80"; style="text-align: center">%.4f</td>    
                """ % float(b_num[y])
                message = message + message3
            # 写入持仓成本价
            message4 = """
            </tr>
            <tr>
                <th width="62"; style="text-align: center">成本价</th>
            """
            message = message + message4
            print("正在写入html,进度20%")
            # 写入持仓成本价格
            for m in range(len(b_trade_cost)):
                message5 = """
                <td width="80"; style="text-align: center">%.5f</td>    
                """ % (b_trade_cost[m])
                message = message + message5

            # 写入最新动态价格
            message6 = """
            </tr>
            <tr>
                <th width="62"; style="text-align: center">最新价</th>
            """
            message = message + message6
            print("正在写入html,进度40%")
            # 写入最新动态价格
            for n in range(len(b_name)):
                message7 = """
                <td width="80"; style="text-align: center">%.5f</td>    
                """ % (b_price_last[n])
                message = message + message7
            # 写入最新总持仓
            message6_2 = """
                        </tr>
                        <tr>
                            <th width="62"; style="text-align: center">总持仓</th>
                        """
            message = message + message6_2
            # 写入最新动态持仓
            for n in range(len(b_name)):
                message7_2 = """
                            <td width="80"; style="text-align: center">%.5f</td>    
                            """ % (b_hold[n])
                message = message + message7_2
            print("正在写入html,进度60%")
            # 写入最新动态收益
            message8 = """
            </tr>
            <tr>
                <th width="62"; style="text-align: center">收益</th>
            """
            message = message + message8
            # 写入最新动态收益
            for ii in range(len(b_trade_cost)):
                if b_price_last[ii]-b_trade_cost[ii] < 0:
                    message9 = """
                <td width="80"; style="text-align: center"><font color="red">%.4f</font></td>    
                """ % ((b_price_last[ii]-b_trade_cost[ii])*b_num[ii])
                else:
                    message9 = """
                <td width="80"; style="text-align: center">%.5f</td>    
                """ % ((b_price_last[ii] - b_trade_cost[ii]) * b_num[ii])
                message = message + message9
            # 写入动态收益率
            message10 = """
            </tr>
            <tr>
                <th width="62"; style="text-align: center">收益率</th>
                """
            message = message + message10
            # 写入最新动态收益
            for xx in range(len(b_trade_cost)):
                if b_trade_cost[xx] == 0:
                    message11 = """
                <td width="80"; style="text-align: center"><font color="red">/</font></td>    
                    """
                    continue
                elif ((b_price_last[xx] / b_trade_cost[xx])-1) < 0:
                    message11 = """
                <td width="80"; style="text-align: center"><font color="red">%.2f%%</font></td>    
                """ % (((b_price_last[xx] / b_trade_cost[xx])-1)*100)
                else:
                    message11 = """
                <td width="80"; style="text-align: center">%.2f%%</td>    
                """ % (((b_price_last[xx] / b_trade_cost[xx]) - 1) * 100)

                message = message + message11
            print("正在写入html,进度80%")
            # 写入挂单情况
            if order_len != 0:  # 如果当前存在挂单
                message11_2 = """
                </tr>
            </table>
                <h3>挂单情况</h3>
            <table border="1" cellspacing="0">
                <tr>"""
                message = message + message11_2
                # 写入挂单情况
                message11_3 = """
                    <th width="90" style="text-align: center">交易对</th>
                    <th width="50" style="text-align: center">类型</th>
                    <th width="60" style="text-align: center">单价</th>
                    <th width="60" style="text-align: center">数量</th>
                    <th width="60" style="text-align: center">总价</th>
                    <th width="60" style="text-align: center">成交率</th>
                    <th width="70" style="text-align: center">状态</th>
                """
                message = message + message11_3
                for xx in range(order_len):
                    message11_4 = """
                </tr>
                <tr>
                    <td style="text-align: center"><a target="_blank" href="https://www.gateio.org/trade/%s">%s</a></td>
                    <td style="text-align: center">%s</td>
                    <td style="text-align: center">%s</td>
                    <td style="text-align: center">%s</td>
                    <td style="text-align: center">%s</td>
                    <td style="text-align: center">%.2f%%</td>
                    <td style="text-align: center">%s</td>
                """ % (order_name[xx], order_name[xx], order_type[xx], str(initial_rate[xx]), str(initial_amount[xx]),
                       str(order_total[xx]), fill_rate[xx]*100, order_status[xx])
                    message = message + message11_4
            # 写入情况信息
            message12 = """
            </tr>
        </table>
        <p>目前钱包总额为：<strong>%.2f</strong>(美元折算) &#9||&#9 <strong>%.2f</strong>(人民币折算)</p>
        <p>比特币数量：<strong>%.4f</strong></p>
        <p>点卡数量: <strong>%.2f</strong></p>
        <p>总的%s数量：<strong>%.2f</strong>&#9||&#9可用%s数量：<strong>%.2f</strong></p>
        <h3>技术分析</h3>
        <p>**<a target="_blank" href="will/index.html">货币预测</a>**<--分割线-->**<a target="_blank" href="will/index2.html">股票预测</a>**</p>
        """ % (total_money, total_cny, btc_num, point_num, base_b, base_b_num, base_b, base_b_mum_available)
            message = message + message12
            # 开始计算累计收益
            message13 = """
        <h3>累计收益</h3>
        <table border="1" cellspacing="0">
            <tr>
                <td colspan="4"; style="text-align: center">总收益(单位：美元)</td>
            </tr>
            <tr>
                <td colspan="2"; style="text-align: center">不考虑手续费</td>
                <td colspan="2"; style="text-align: center">含手续费</td>
            </tr>
            <tr>
                <td width="80"; style="text-align: center">含赠币</td>
                <td width="80"; style="text-align: center">不含赠币</td>
                <td width="80"; style="text-align: center">含赠币</td>
                <td width="80"; style="text-align: center">不含赠币</td>
            </tr>
            <tr>
                <td width="80"; style="text-align: center">%.4f</td>
                <td width="80"; style="text-align: center">%.4f</td>
                <td width="80"; style="text-align: center">%.4f</td>
                <td width="80"; style="text-align: center">%.4f</td>
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
            message = message + message13
            # 写入Html的最后部分，加入手机端自适应大小
            message_foot = """
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
"""
            message = message + message_foot
            f.write(message)
            f.close()
            print("写入html完毕,进度100%")
            time.sleep(refresh_time)
    except Exception as err:
        print(err)
# 循环结束-----------------------------------------
