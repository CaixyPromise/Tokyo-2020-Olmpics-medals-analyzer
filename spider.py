# 爬取2020年东京奥运会奖牌榜数据，并且存入sqlite数据库内
import requests
import re
import sqlite3

# 央视CCTV 5奖牌榜页面的奖牌数据接口
url = r'https://api.cntv.cn/olympic/getOlyMedals?serviceId=pcocean&itemcode=GEN-------------------------------&t=jsonp&cb=banomedals'
# 模拟请求
response = requests.get(url)
# 数据被banomedals(奖牌数据)包裹起来，这里可以用正则表达式匹配出来
text = re.findall('banomedals(.*);', response.text)
# 匹配出来就是一个字典形式，用eval转换成py可以转化的类型
medals_dict = eval(text[0])
# 提取出排行榜
medals_List = medals_dict['data']['medalsList']
#
# # 链接数据库
# conn = sqlite3.connect("medalsDB")
# # 创建操作器
# cursor = conn.cursor()
# # 创建数据库表单
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS medal_rank (
#         id INTEGER PRIMARY KEY,
#         rank INTEGER,
#         countryname TEXT,
#         countryid TEXT,
#         gold INTEGER,
#         silver INTEGER,
#         bronze INTEGER,
#         count INTEGER
#     )
# ''')
# # 插入数据
# for entry in medals_List:
#     cursor.execute('''
#         INSERT INTO medal_rank (rank, countryname, countryid, gold, silver, bronze, count)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#     ''', (
#         int(entry['rank']),
#         entry['countryname'],
#         entry['countryid'],
#         int(entry['gold']),
#         int(entry['silver']),
#         int(entry['bronze']),
#         int(entry['count'])
#     ))
# # 提交更改并关闭连接
# conn.commit()
# conn.close()

# 每一个国家获奖的项目
# https://api.cntv.cn/Olympic/getOlyMedalList?t=jsonp&cb=OM&serviceId=pcocean&countryid=USA
country_code = [i.get('countryid') for i in medals_List]

def remote_underline(val_dict):
    subitemcode = val_dict['subitemcode']
    subitemcode = subitemcode.replace('-', '')
    itemcode = val_dict['itemcode']
    itemcode = itemcode.replace('-', '')
    playname = val_dict['playname']
    playname = playname.replace(r'\\/', '·')
    playname = playname.replace(r'\/', '·')

    val_dict['subitemcode'] = subitemcode
    val_dict['itemcode'] = itemcode
    val_dict['playname'] = playname
    return val_dict


def monitor_process(queue, event, size, lock):
    condition = True
    conn = sqlite3.connect("medalsDB")
    # 创建操作器
    cursor = conn.cursor()

    sql_insert = '''
        INSERT INTO country_awards (
            playid, itemcodename, subitemname, subitemcode,
            medaltype, itemcode, startdatecn, countryname,
            playname, medal, totalurl, countryid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    while True:
        with lock:
            if queue.empty() and event.is_set():
                break
            val = queue.get()

        values = [(entry['playid'], entry['itemcodename'], entry['subitemname'],
                   entry['subitemcode'], entry['medaltype'], entry['itemcode'],
                   entry['startdatecn'], entry['countryname'], entry['playname'],
                   entry['medal'], entry['totalurl'], entry['countryid']) for entry in val]

        with lock:
            cursor.executemany(sql_insert, values)
            conn.commit()
            size.value += 1
    conn.close()
    print('监控进程退出')

def request_html(msg_q, contry_list):
    item_url = 'https://api.cntv.cn/Olympic/getOlyMedalList?t=jsonp&cb=OM&serviceId=pcocean&countryid={country}'
    for target_id in contry_list:
        item_response = requests.get(item_url.format(country = target_id))

        data = re.findall('OM(.*);', item_response.text)
        data = eval(data[0])
        data = data['data']
        medalList = data['medalList']

        result_list = list(map(remote_underline, medalList))
        msg_q.put(result_list)


from multiprocessing import Process, Manager
import requests


if __name__ == "__main__":
    with Manager() as manager:

        msg_q = manager.Queue()
        event = manager.Event()
        size = manager.Value('size', 0)
        lock = manager.Lock()
        processes = []
        batch_size = 10
        # 创建并启动进程
        monitor = Process(target = monitor_process, args = (msg_q, event, size, lock))
        monitor.start()
        print(f'创建并启动[监控]进程: {monitor.pid}')

        for i in range(0, len(country_code), batch_size):

            batch = country_code[i : i + batch_size]
            process = Process(target = request_html, args = (msg_q, batch))
            processes.append(process)
            process.start()
            print(f'创建并启动[任务]进程: {process.pid}')

        # 等待所有进程完成
        print('爬取完成，现在回收任务进程...')
        for process in processes:
            process.join()
        else:
            print('回收任务进程完成')
        print('正在等待上传工作')
        event.set()
        monitor.join(timeout = 5)
        print('监控进程退出')
        print(msg_q.empty(), event.is_set())
        msg_q.task_done()
        exit(0)
        print(f'最后获取到了: {size.value} 条数据')

