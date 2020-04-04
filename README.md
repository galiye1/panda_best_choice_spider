# panda_best_choice_spider
爬取电商平台熊猫优选所有男装的详细信息

#爬取步骤：
        1.使用selenium请求需要访问的网页，对于下拉动态显示的数据，也用selenium来加载
        2.通过xpath抽取网页需要的内容
        3.在项目setting中配置redis所需的参数
        4.在项目根目录下使用pip freeze > requirements.txt命令打包项目所需的包
        5.在服务器上配置redis的redis-windows.conf文件，使用redis-server redis.windows.conf启动redis服务
        6.使用redis-cli命令连接服务器
        7.进入爬虫代码目录下，使用scrapy runspider 我的爬虫文件.py 命令启动爬虫监听
        8.在redis-cli客户端使用命令lpush (redis-key) (被爬取url)向爬虫推入被爬网址，爬虫开始爬取网页
        
#遇到的问题:
        1.商品详细信息无法在源码中爬取到url
        解决：通过selenium模拟点击，进入商品详情页面
        2.商品是通过滚动条下拉动态获取的，并且没有底线
        解决：通过一个while循环，selenium模拟下拉，实现无限爬取
        3.网页下拉后有的元素获取不到
        解决：让下拉的速度比获取元素的速度快
        4.scrapy中间件只能修改一个request,但商品详细信息只能通过selenium进入,然后要立刻处理（考虑过协程，但是架构不支持），所以无法将selenium放在中间件中处理request
        解决：将请求和处理都放在爬虫部分
