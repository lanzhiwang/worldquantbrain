import os
from time import sleep
import requests
# import json
# from os.path import expanduser
from requests.auth import HTTPBasicAuth


def sign_in():
    # Load credentials # 加载凭证
    # with open(expanduser('brain_credentials.txt')) as f:
    #     credentials = json.load(f)

    # Extract username and password from the list # 从列表中提取用户名和密码
    # username, password = credentials
    username = os.getenv('username')
    password = os.getenv('password')
    print("username:", username)
    print("password:", password)

    # Create a session object # 创建会话对象
    sess = requests.Session()

    # Set up basic authentication # 设置基本身份验证
    sess.auth = HTTPBasicAuth(username, password)

    # Send a POST request to the API for authentication # 向API发送POST请求进行身份验证
    response = sess.post('https://api.worldquantbrain.com/authentication')

    # Print response status and content for debugging # 打印响应状态和内容以调试
    print("response.status_code:", response.status_code)
    print("response.json:", response.json())
    return sess


sess = sign_in()

# 获取数据集ID为fundamental6（Company Fundamental Data for Equity）下的所有数据字段
### Get Data_fields like Data Explorer 获取所有满足条件的数据字段及其ID
def get_datafields(sess, searchScope, dataset_id: str = '', search: str = ''):
    import pandas as pd

    instrument_type = searchScope['instrumentType']
    region = searchScope['region']
    delay = searchScope['delay']
    universe = searchScope['universe']

    if len(search) == 0:
        url_template = "https://api.worldquantbrain.com/data-fields?" + \
                       f"&instrumentType={instrument_type}" + \
                       f"&region={region}&delay={str(delay)}&universe={universe}&dataset.id={dataset_id}&limit=50" + \
                       "&offset={x}"
        # print("url_template:", url_template)
        # url_template: https://api.worldquantbrain.com/data-fields?&instrumentType=EQUITY&region=USA&delay=1&universe=TOP3000&dataset.id=fundamental6&limit=50&offset={x}

        # print("url_template.format(x=0):", url_template.format(x=0))
        # url_template.format(x=0): https://api.worldquantbrain.com/data-fields?&instrumentType=EQUITY&region=USA&delay=1&universe=TOP3000&dataset.id=fundamental6&limit=50&offset=0

        data = sess.get(url_template.format(x=0)).json()
        # print("data1:", data)
        count = data['count']
    else:
        url_template = "https://api.worldquantbrain.com/data-fields?" + \
                       f"&instrumentType={instrument_type}" + \
                       f"&region={region}&delay={str(delay)}&universe={universe}&limit=50" + \
                       f"&search={search}" + \
                       "&offset={x}"
        count = 100

    # print("count:", count)

    datafields_list = []
    for x in range(0, count, 50):
        datafields = sess.get(url_template.format(x=x))
        # print("data2:", datafields.json())

        datafields_list.append(datafields.json()['results'])

    # print("datafields_list:", datafields_list)
    datafields_list_flat = [item for sublist in datafields_list for item in sublist]
    # print("datafields_list_flat:", datafields_list_flat)

    datafields_df = pd.DataFrame(datafields_list_flat)
    return datafields_df

# 爬取id
searchScope = {'region': 'USA', 'delay': '1', 'universe': 'TOP3000', 'instrumentType': 'EQUITY'}
fundamental6 = get_datafields(sess=sess, searchScope=searchScope, dataset_id='fundamental6') # id设置

# 筛选（这里是type的MATRIX）
fundamental6 = fundamental6[fundamental6['type'] == "MATRIX"]
fundamental6.head()

datafields_list_fundamental6 = fundamental6['id'].values
print("datafields_list_fundamental6:", datafields_list_fundamental6)
print("len(datafields_list_fundamental6):", len(datafields_list_fundamental6))


# 将datafield替换到Alpha模板(框架)中group_rank({fundamental model data}/cap,subindustry)批量生成Alpha
alpha_list = []

for index, datafield in enumerate(datafields_list_fundamental6, start=1):
    alpha_expression = f'group_rank(({datafield})/cap, subindustry)'
    # print(f"正在循环第 {index} 个元素,组装alpha表达式: {alpha_expression}")
    simulation_data = {
        "type": "REGULAR",
        "settings": {
            "instrumentType": "EQUITY",
            "region": "USA",
            "universe": "TOP3000",
            "delay": 1,
            "decay": 6,
            "neutralization": "SUBINDUSTRY",
            "truncation": 0.08,
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": "ON",
            "language": "FASTEXPR",
            "visualization": False,
        },
        "regular": alpha_expression
    }
    alpha_list.append(simulation_data)

# print(f"there are {len(alpha_list)} Alphas to simulate")
# print(alpha_list[0])
# there are 574 Alphas to simulate
# {
#     'type': 'REGULAR',
#     'settings': {
#         'instrumentType': 'EQUITY',
#         'region': 'USA',
#         'universe': 'TOP3000',
#         'delay': 1,
#         'decay': 6,
#         'neutralization': 'SUBINDUSTRY',
#         'truncation': 0.08,
#         'pasteurization': 'ON',
#         'unitHandling': 'VERIFY',
#         'nanHandling': 'ON',
#         'language': 'FASTEXPR',
#         'visualization': False
#     },
#     'regular': 'group_rank((assets)/cap, subindustry)'
# }

# 将Alpha一个一个发送至服务器进行回测,并检查是否断线, 如断线则重连, 并继续发送
for index, alpha in enumerate(alpha_list, start=1):
    # print("index:", index)
    # print("alpha:", alpha['regular'])
    if index < 1:   #如果中断重跑, 可以修改1从指定位置重跑, 即可跳过已经模拟过的Alpha
        continue
    if index % 100 == 0:
        sess = sign_in()
        # print(f"重新登录, 当前index为{index}")

    sim_resp = sess.post(
        'https://api.worldquantbrain.com/simulations',
        json=alpha,
    )
    # print("sim_resp.status_code:", sim_resp.status_code)

    try:
        sim_progress_url = sim_resp.headers['Location']
        while True:
            sim_progress_resp = sess.get(sim_progress_url)
            retry_after_sec = float(sim_progress_resp.headers.get("Retry-After", 0))
            if retry_after_sec == 0:  # simulation done!模拟完成!
                break
            sleep(retry_after_sec)
        alpha_id = sim_progress_resp.json()["alpha"]  # the final simulation result.# 最终模拟结果
        # print(f"{index}: {alpha_id}: {alpha['regular']}")
        print(alpha_id)
    except:
        # print("no location, sleep for 10 seconds and try next alpha.“没有位置, 睡10秒然后尝试下一个字母。”")
        sleep(10)
