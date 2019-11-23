from my_fun import fun_all_bitcoin, fun_will, creat_html
import datetime
import pytz
import time
while True:
    try:
        # 获取持有币种和数量
        b_name, b_num = fun_all_bitcoin()
        print(b_name)

        # 计算币种未来并且写入html
        n = len(b_name)
        for i in range(1, n+1):
            if b_name[i-1] in ('QKC', 'MDA'):
                exch_name = b_name[i-1]+'USD'  # 定义交易对名称
            elif b_name[i-1] in ('FTI',):
                exch_name = b_name[i-1]  # 定义交易对名称
            else:
                exch_name = b_name[i - 1] + 'USDT'  # 定义交易对名称
            print(exch_name)
            html = fun_will('1D', exch_name)
            creat_html(i, html)

        # 将所有币种集成在一个页面上
        # 开始生成html文件--------------------------------------------------
        GEN_HTML = "will/index.html"  # 路径准备
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
                <title>货币预测 </title>
                <link rel="icon" href="https://www.gateio.co/images/apple-touch-icon-120x120.png"/>
            </head>
            <body>"""
        f.write(message)
        f.close()
        # 将所有页面放到一个框架
        for x in range(1, n+1):
            f = open(GEN_HTML, 'a', encoding="utf-8")
            message2 ="""
            <iframe src="{}.html" width="450" height="470"  frameborder="0" ></iframe>
            """.format(x)
            f.write(message2)
            f.close()
        # 打印页面尾部
        f = open(GEN_HTML, 'a', encoding="utf-8")
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
        f.write(message_foot)
        f.close()
    except Exception as err:
        print(err)
    time.sleep(3600)

