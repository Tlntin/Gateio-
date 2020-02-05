def user_info():
    # 填写 apiKey secret
    api_key = 'your apikey'
    secret_key = 'your secret_key'
    # 比特币提现地址
    btc_address = 'your btc address'
    # 地址提供链接，不可修改
    query_url = 'https://data.gateio.life'
    trade_url = 'https://api.gateio.life'
    return api_key, secret_key, btc_address, query_url, trade_url


def other_info():
    # 填写其他api获取不了的信息****************
    user_name = "User_name"  # 你的用户名
    free_b = 40.0  # 你的GT赠币个数（如果有其它的自行补充）
    locked_type = "BTC"  # Startup锁仓币种
    loced_num = 0  # 锁仓币种数量,没有就填零
    vip_level = 1  # vip等级
    refresh_time = 20  # 数据刷新间隔，单位秒
    base_b = "USDT"  # 默认交易对：XX_USDT
    return user_name, free_b, locked_type, loced_num, vip_level, refresh_time, base_b
