#!/usr/bin/python3
from gateAPI import GateIO
from User_input import user_info
from User_input import other_info
from my_fun import trade_star
import time
# 获取用户信息
(apiKey, secretKey, btcAddress, API_QUERY_URL, API_TRADE_URL) = user_info()
(UserName, free_b, loced_type, loced_num, Vip_level, refresh_time, base_b) = other_info()

# 创建连接
gate_query = GateIO(API_QUERY_URL, apiKey, secretKey)  # 查询连接
gate_trade = GateIO(API_TRADE_URL, apiKey, secretKey)  # 交易连接


def test(m):
    # 交易市场详细行情
    data = gate_query.marketlist()
    data2 = data['data']
    n = len(data2)
    all_coin = []  # 查询所有USDT币种
    for i in range(n):
        if data2[i]['curr_b'] == "USDT" and data2[i]['symbol'] != "USDT":
            all_coin.append(data2[i]['symbol'])
    b_name_len = len(all_coin)
    recommend_buy = []  # 推荐买入的币种
    recommend_sell = []  # 推荐卖出的币种
    for i in range(60):  # 查询前60
        data = trade_star(all_coin[i], m)  # 查询分钟行情
        if data == "buy":
            recommend_buy.append(all_coin[i])
        if data == "sell":
            recommend_sell.append(all_coin[i])
    print("输出完成")
    return recommend_buy, recommend_sell


GEN_HTML = "index2.html"  # 路径准备

while True:
    try:
        # 写入推荐
        f = open(GEN_HTML, "w", encoding="utf-8")
        message = """
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5,
                     maximum-scale=2.0, user-scalable=yes" /> 
                <title>我的钱包 </title>
                <link rel="icon" href="https://www.gateio.co/images/apple-touch-icon-120x120.png"/>
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
            </head>
            <body>
        """
        f.write(message)
        f.close()
        time.sleep(1)

        # 写入推荐
        (recommend_buy_15, recommend_sell_15) = test(15)  # 查询15分钟行情
        if len(recommend_buy_15) != 0:
            f = open(GEN_HTML, "a", encoding="utf-8")
            message2 = """
                <h4>15分钟推荐！</h4>
                <p>推荐买入：%s</p>
                <p>推荐卖出：%s</p>
            """ % (recommend_buy_15, recommend_sell_15)
            f.write(message2)
            f.close()

        (recommend_buy_30, recommend_sell_30) = test(30)  # 查询30分钟行情
        if len(recommend_buy_30) != 0:
            # 写入推荐
            f = open(GEN_HTML, "a", encoding="utf-8")
            message3 = """
                <h4>30分钟推荐！</h4>
                <p>推荐买入：%s</p>
                <p>推荐卖出：%s</p>
            """ % (recommend_buy_30, recommend_sell_30)
            f.write(message3)
            f.close()
            time.sleep(1)
        # 写入推荐
        (recommend_buy_60, recommend_sell_60) = test(60)  # 查询60分钟行情
        if len(recommend_buy_60) != 0:
            f = open(GEN_HTML, "a", encoding="utf-8")
            message4 = """
                <h4>60分钟推荐！</h4>
                <p>推荐买入：%s</p>
                <p>推荐卖出: %s</p>
            """ % (recommend_buy_60, recommend_sell_60)
            f.write(message4)
            f.close()
            time.sleep(1)
        message5 = """
            <body>
        </html>
        """
        f = open(GEN_HTML, "a", encoding="utf-8")
        f.write(message5)
        f.close()
    except IOError:
        print(IOError)
