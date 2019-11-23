## Gate.io辅助交易系统使用说明
### 1.需要的东西
1. apikey和私钥一个，点击[官网](https://www.gateio.life)申请我跳转
2. 只支持Gate.io
3. python3环境一个
### 2.如何运行
1. 先修改User_input.py，改成自己的信息
2. 运行gate_html.py即可生成html文档
3. 运行gate_will.py即可生成币种预测信息
4. 运行stock.py即可生成股票预测信息，股票内容可以自行修改
### 3.作者说明
1. 此代码无任何后门，api自行保管好，发生被盗与作者无关
2. 此代码参考了官方api示范，并对其进行了一定修改。具体请看gate_api.py文档
### 4.支持的功能
1. 持仓币种、数量查询
2. 持仓成本价计算（可能不准，仅供参考）
3. 币种最新价查询
4. 持仓币种的折算价值
5. 目前的持仓动态收益
6. 目前的动态收益率
7. 目前的钱包总额（美元or人民币）
8. 比特币数量
9. 点卡数量
10. 可用USDT和总的USDT
11. 货币走势预测和股票预测
12. 累计收益
13. 根据走势自动交易（这个不开源，自行完善）
### 5.效果图
![](https://github.com/Tlntin/Gateio-/blob/master/png/001.png)
![](https://github.com/Tlntin/Gateio-/blob/master/png/002.png)  
![](https://github.com/Tlntin/Gateio-/blob/master/png/003.png) 