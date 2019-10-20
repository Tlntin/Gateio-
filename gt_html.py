#!/usr/bin/python3
from gateAPI import GateIO
import time
import datetime
import pytz
from User_input import user_info
from User_input import other_info
from my_fun import vip_fun, trade_cost_query, total_money_query, basic_query_fun, orders_fun

# 获取用户信息
(apiKey, secretKey, btcAddress, API_QUERY_URL, API_TRADE_URL) = user_info()
(UserName, free_b, loced_type, loced_num, Vip_level, refresh_time, base_b) = other_info()

# 创建连接
gate_query = GateIO(API_QUERY_URL, apiKey, secretKey)  # 查询连接
gate_trade = GateIO(API_TRADE_URL, apiKey, secretKey)  # 交易连接

# 查询挂单吃单费率
(Maker, Taker) = vip_fun(Vip_level)


# 开始循环，生成Html文件--------------------------
while True:
    try:
        # 从订单表中查询总支出、总支出含手续费
        (cost, cost_qc) = trade_cost_query()
        time.sleep(1)  # 等1秒
        # 查询基础信息
        # 可用货币名称、数量、点卡、基础币数量、各类币种持仓成本
        (b_name, b_num, point_num, base_b_num, b_trade_cost) = basic_query_fun()
        (order_len, order_name, order_type, initial_rate, initial_amount, order_total, deal_rate, fill_rate,
         order_status) = orders_fun()
        time.sleep(1)  # 等1秒
        # 定义一个for循环，用于实时更新数据
        for i in range(10):
            # 返回钱包总额(美元)，钱包总额（人民币），币种最近价格,可用基础货币
            (total_money, total_cny, b_price_last, base_b_mum_available) = total_money_query()

            # 总利润=商品折算后的总金额-商品订单总成本(不考虑手续费)=总金额 - 基础代币- 订单总成本
            profit = total_money - base_b_num - cost
            profit_qc = total_money - base_b_num - cost_qc
            profit_qz = profit - float(gate_query.ticker("gt_usdt")['last']) * free_b
            profit_qc_qz = profit_qc - float(gate_query.ticker("gt_usdt")['last']) * free_b
            # 开始生成html文件--------------------------------------------------
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
        <p>数据来源：<a target="_blank" href="https://www.gateio.co">Gateio交易所</a></p>
        <p>数据刷新时间:%s</p>
        <p>用户名：%s &#9||&#9 VIP等级：<font color="red">VIP%d</font></p>
        <p>费率：Maker：%.3f%% &#9||&#9 Taker：%.3f%%</p>
        <h3>持币情况</h3>
        <table border="1" cellspacing="0">
              <tr>
                <th width="100"; style="text-align: center">持有币种</th>  
            """ % (str_time, UserName, Vip_level, round(100*Maker, 3), round(100*Taker, 3))
            # 写入持有币种类别信息，不包括点卡和USDT
            for x in range(len(b_name)):
                message1 = """
                <th width="80"; style="text-align: center">%s</th>    
                """ % (b_name[x])
                message = message + message1
            # 写入币种数量信息
            message2 = """
            </tr>
            <tr>
                <td width="100"; style="text-align: center">持有数量</td>
            """
            message = message + message2
            # 写入币种数量
            for y in range(len(b_name)):
                message3 = """
                <td width="80"; style="text-align: center">%s</td>    
                """ % (b_num[y])
                message = message + message3
            # 写入持仓成本价
            message4 = """
            </tr>
            <tr>
                <td width="100"; style="text-align: center">持仓成本价</td>
            """
            message = message + message4
            print(b_trade_cost)
            # 写入持仓成本价格
            for m in range(len(b_name)):
                message5 = """
                <td width="80"; style="text-align: center">%.4f</td>    
                """ % (b_trade_cost[m])
                message = message + message5

            # 写入最新动态价格
            message6 = """
            </tr>
            <tr>
                <td width="100"; style="text-align: center">最新动态价</td>
            """
            message = message + message6
            # 写入最新动态价格
            for n in range(len(b_name)):
                message7 = """
                <td width="80"; style="text-align: center">%.4f</td>    
                """ % (b_price_last[n])
                message = message + message7
            # 写入最新动态收益
            message8 = """
            </tr>
            <tr>
                <td width="100"; style="text-align: center">动态收益</td>
            """
            message = message + message8
            # 写入最新动态收益
            for ii in range(len(b_name)):
                message9 = """
                <td width="80"; style="text-align: center">%.4f</td>    
                """ % ((b_price_last[ii]-b_trade_cost[ii])*b_num[ii])
                message = message + message9
            # 写入动态收益率
            message10 = """
            </tr>
            <tr>
                <td width="100"; style="text-align: center">动态收益率</td>
                """
            message = message + message10
            # 写入最新动态收益
            for xx in range(len(b_name)):
                message11 = """
                <td width="80"; style="text-align: center">%.2f%%</td>    
                """ % (((b_price_last[xx] / b_trade_cost[xx])-1)*100)
                message = message + message11
            # 写入挂单情况
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
                <th width="60" style="text-align: center">成交价</th>
                <th width="60" style="text-align: center">成交率</th>
                <th width="70" style="text-align: center">订单状态</th>
            </tr>
            <tr>
            """
            message = message + message11_3
            for xx in range(order_len):
                message11_4 = """
                <td style="text-align: center">%s</td>
                <td style="text-align: center">%s</td>
                <td style="text-align: center">%s</td>
                <td style="text-align: center">%s</td>
                <td style="text-align: center">%s</td>
                <td style="text-align: center">%s</td>
                <td style="text-align: center">%.2f%%</td>
                <td style="text-align: center">%s</td>
            """ % (order_name[xx], order_type[xx], str(initial_rate[xx]), str(initial_amount[xx]), str(order_total[xx]),
                   str(deal_rate[xx]), fill_rate[xx]*100, order_status[xx])
                message = message + message11_4
            # 写入情况信息
            message12 = """
            </tr>
        </table>
        <p>目前钱包总额为：<strong>%.2f</strong>(美元折算) &#9||&#9 <strong>%.2f</strong>(人民币折算)</p>
        <p>点卡数量: <strong>%.2f</strong></p>
        <p>总的%s数量：<strong>%.2f</strong>&#9||&#9可用%s数量：<strong>%.2f</strong></p>
        """ % (total_money, total_cny, point_num, base_b, base_b_num, base_b,base_b_mum_available)
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
            print("写入html完毕")
            time.sleep(refresh_time)
    except IOError:
        print(IOError)
# 循环结束-----------------------------------------
