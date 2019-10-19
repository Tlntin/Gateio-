def user_info():
    # 填写 apiKey secret
    apiKey = 'you apiKey'
    secretKey = 'you secretKey'
    # 比特币提现地址
    btcAddress = 'your btc address'
    # 地址提供链接，不可修改
    API_QUERY_URL = 'data.gateio.co'
    API_TRADE_URL = 'api.gateio.co'
    return apiKey, secretKey, btcAddress, API_QUERY_URL, API_TRADE_URL


def other_info():
    # 填写其他api获取不了的信息****************
    UserName = "Tlntin"  # 你的用户名
    free_b = 40 # 你的GT赠币个数（如果有其它的自行补充）
    loced_type = "BTC"  # Startup锁仓币种
    loced_num = 0  # 锁仓币种数量,没有就填零
    Vip_level = 1  # vip等级
    refresh_time = 20  # 数据刷新间隔，单位秒
    base_b = "USDT"  # 默认交易对：XX_USDT
    return UserName, free_b, loced_type, loced_num, Vip_level, refresh_time, base_b