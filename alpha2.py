import os
import requests
from requests.auth import HTTPBasicAuth

# # 加载凭据文件
# with open(expanduser('brain_credentials.txt')) as f:
#     credentials = json.load(f)

# 从列表中提取用户名和密码
# username, password = credentials
username = os.getenv("username")
password = os.getenv("password")
print("username:", username)
print("password:", password)

# 创建会话对象
sess = requests.Session()

# 设置基本身份验证
sess.auth = HTTPBasicAuth(username, password)

# 向API发送POST请求进行身份验证
response = sess.post("https://api.worldquantbrain.com/authentication")

# 打印响应状态和内容以调试
print("response.status_code:", response.status_code)
print("response.json:", response.json())


sim_resp = sess.get(
    "https://api.worldquantbrain.com/users/self/alphas?limit=100&offset=500&status=UNSUBMITTED"
)

print("sim_resp.status_code:", sim_resp.status_code)
# print("sim_resp.json:", sim_resp.json())
# {
#     'count': 571,
#     'next': 'http://api.worldquantbrain.com:443/users/self/alphas?limit=50&offset=50&status=UNSUBMITTED',
#     'previous': None,
#     'results': [
#         {'id': 'xVWpJpp', 'type': 'REGULAR', 'author': 'ZH14406', 'settings': {'instrumentType': 'EQUITY', 'region': 'USA', 'universe': 'TOP3000', 'delay': 1, 'decay': 6, 'neutralization': 'SUBINDUSTRY', 'truncation': 0.01, 'pasteurization': 'ON', 'unitHandling': 'VERIFY', 'nanHandling': 'ON', 'maxTrade': 'OFF', 'language': 'FASTEXPR', 'visualization': False}, 'regular': {'code': 'group_neutralize(ts_rank(rank(debt_st)/rank(enterprise_value), 10), industry)', 'description': None, 'operatorCount': 5}, 'dateCreated': '2025-06-05T04:10:29-04:00', 'dateSubmitted': None, 'dateModified': '2025-06-05T04:10:30-04:00', 'name': None, 'favorite': False, 'hidden': False, 'color': None, 'category': None, 'tags': [], 'classifications': [{'id': 'DATA_USAGE:SINGLE_DATA_SET', 'name': 'Single Data Set Alpha'}], 'grade': 'INFERIOR', 'stage': 'IS', 'status': 'UNSUBMITTED', 'is': {'pnl': 4532492, 'bookSize': 20000000, 'longCount': 1053, 'shortCount': 1058, 'turnover': 0.3298, 'returns': 0.0916, 'drawdown': 0.0853, 'margin': 0.000555, 'sharpe': 1.16, 'fitness': 0.61, 'startDate': '2018-01-20', 'checks': [{'name': 'LOW_SHARPE', 'result': 'FAIL', 'limit': 1.25, 'value': 1.16}, {'name': 'LOW_FITNESS', 'result': 'FAIL', 'limit': 1.0, 'value': 0.61}, {'name': 'LOW_TURNOVER', 'result': 'PASS', 'limit': 0.01, 'value': 0.3298}, {'name': 'HIGH_TURNOVER', 'result': 'PASS', 'limit': 0.7, 'value': 0.3298}, {'name': 'CONCENTRATED_WEIGHT', 'result': 'PASS'}, {'name': 'LOW_SUB_UNIVERSE_SHARPE', 'result': 'PASS', 'limit': 0.5, 'value': 0.78}, {'name': 'SELF_CORRELATION', 'result': 'PENDING'}, {'name': 'MATCHES_COMPETITION', 'result': 'PASS', 'competitions': [{'id': 'challenge', 'name': 'Challenge'}]}]}, 'os': None, 'train': None, 'test': None, 'prod': None, 'competitions': None, 'themes': None, 'pyramids': None, 'pyramidThemes': None, 'team': None},
#         {'id': 'gXdVnrJ', 'type': 'REGULAR', 'author': 'ZH14406', 'settings': {'instrumentType': 'EQUITY', 'region': 'USA', 'universe': 'TOP3000', 'delay': 1, 'decay': 6, 'neutralization': 'SUBINDUSTRY', 'truncation': 0.08, 'pasteurization': 'ON', 'unitHandling': 'VERIFY', 'nanHandling': 'ON', 'maxTrade': 'OFF', 'language': 'FASTEXPR', 'visualization': False}, 'regular': {'code': 'group_rank((fnd6_pnrsho)/cap, subindustry)', 'description': None, 'operatorCount': 2}, 'dateCreated': '2025-06-05T04:10:27-04:00', 'dateSubmitted': None, 'dateModified': '2025-06-05T04:10:27-04:00', 'name': None, 'favorite': False, 'hidden': False, 'color': None, 'category': None, 'tags': [], 'classifications': [], 'grade': 'AVERAGE', 'stage': 'IS', 'status': 'UNSUBMITTED', 'is': {'pnl': 3351787, 'bookSize': 20000000, 'longCount': 1361, 'shortCount': 1514, 'turnover': 0.0203, 'returns': 0.0677, 'drawdown': 0.0405, 'margin': 0.006678, 'sharpe': 1.64, 'fitness': 1.21, 'startDate': '2018-01-20', 'checks': [{'name': 'LOW_SHARPE', 'result': 'PASS', 'limit': 1.25, 'value': 1.64}, {'name': 'LOW_FITNESS', 'result': 'PASS', 'limit': 1.0, 'value': 1.21}, {'name': 'LOW_TURNOVER', 'result': 'PASS', 'limit': 0.01, 'value': 0.0203}, {'name': 'HIGH_TURNOVER', 'result': 'PASS', 'limit': 0.7, 'value': 0.0203}, {'name': 'CONCENTRATED_WEIGHT', 'result': 'PASS'}, {'name': 'LOW_SUB_UNIVERSE_SHARPE', 'result': 'FAIL', 'limit': 0.71, 'value': -0.12}, {'name': 'SELF_CORRELATION', 'result': 'PENDING'}, {'name': 'MATCHES_COMPETITION', 'result': 'PASS', 'competitions': [{'id': 'challenge', 'name': 'Challenge'}]}]}, 'os': None, 'train': None, 'test': None, 'prod': None, 'competitions': None, 'themes': None, 'pyramids': None, 'pyramidThemes': None, 'team': None},
#         ...
#         {'id': '31GdoJ0', 'type': 'REGULAR', 'author': 'ZH14406', 'settings': {'instrumentType': 'EQUITY', 'region': 'USA', 'universe': 'TOP3000', 'delay': 1, 'decay': 6, 'neutralization': 'SUBINDUSTRY', 'truncation': 0.08, 'pasteurization': 'ON', 'unitHandling': 'VERIFY', 'nanHandling': 'ON', 'maxTrade': 'OFF', 'language': 'FASTEXPR', 'visualization': False}, 'regular': {'code': 'group_rank((fnd6_newa2v1300_txach)/cap, subindustry)', 'description': None, 'operatorCount': 2}, 'dateCreated': '2025-06-03T17:02:26-04:00', 'dateSubmitted': None, 'dateModified': '2025-06-03T17:02:26-04:00', 'name': None, 'favorite': False, 'hidden': False, 'color': None, 'category': None, 'tags': [], 'classifications': [], 'grade': 'INFERIOR', 'stage': 'IS', 'status': 'UNSUBMITTED', 'is': {'pnl': -353342, 'bookSize': 20000000, 'longCount': 1409, 'shortCount': 1610, 'turnover': 0.0153, 'returns': -0.0071, 'drawdown': 0.1253, 'margin': -0.000933, 'sharpe': -0.2, 'fitness': -0.05, 'startDate': '2018-01-20', 'checks': [{'name': 'LOW_SHARPE', 'result': 'FAIL', 'limit': 1.25, 'value': -0.2}, {'name': 'LOW_FITNESS', 'result': 'FAIL', 'limit': 1.0, 'value': -0.05}, {'name': 'LOW_TURNOVER', 'result': 'PASS', 'limit': 0.01, 'value': 0.0153}, {'name': 'HIGH_TURNOVER', 'result': 'PASS', 'limit': 0.7, 'value': 0.0153}, {'name': 'CONCENTRATED_WEIGHT', 'result': 'PASS'}, {'name': 'LOW_SUB_UNIVERSE_SHARPE', 'result': 'FAIL', 'limit': -0.09, 'value': -0.51}, {'name': 'SELF_CORRELATION', 'result': 'PENDING'}, {'name': 'MATCHES_COMPETITION', 'result': 'PASS', 'competitions': [{'id': 'challenge', 'name': 'Challenge'}]}]}, 'os': None, 'train': None, 'test': None, 'prod': None, 'competitions': None, 'themes': None, 'pyramids': None, 'pyramidThemes': None, 'team': None},
#         {'id': 'bJxp99N', 'type': 'REGULAR', 'author': 'ZH14406', 'settings': {'instrumentType': 'EQUITY', 'region': 'USA', 'universe': 'TOP3000', 'delay': 1, 'decay': 6, 'neutralization': 'SUBINDUSTRY', 'truncation': 0.08, 'pasteurization': 'ON', 'unitHandling': 'VERIFY', 'nanHandling': 'ON', 'maxTrade': 'OFF', 'language': 'FASTEXPR', 'visualization': False}, 'regular': {'code': 'group_rank((fnd6_newa2v1300_tstkn)/cap, subindustry)', 'description': None, 'operatorCount': 2}, 'dateCreated': '2025-06-03T17:00:03-04:00', 'dateSubmitted': None, 'dateModified': '2025-06-03T17:00:03-04:00', 'name': None, 'favorite': False, 'hidden': False, 'color': None, 'category': None, 'tags': [], 'classifications': [], 'grade': 'INFERIOR', 'stage': 'IS', 'status': 'UNSUBMITTED', 'is': {'pnl': 3072925, 'bookSize': 20000000, 'longCount': 1174, 'shortCount': 1868, 'turnover': 0.0176, 'returns': 0.0621, 'drawdown': 0.0658, 'margin': 0.007038, 'sharpe': 1.23, 'fitness': 0.87, 'startDate': '2018-01-20', 'checks': [{'name': 'LOW_SHARPE', 'result': 'FAIL', 'limit': 1.25, 'value': 1.23}, {'name': 'LOW_FITNESS', 'result': 'FAIL', 'limit': 1.0, 'value': 0.87}, {'name': 'LOW_TURNOVER', 'result': 'PASS', 'limit': 0.01, 'value': 0.0176}, {'name': 'HIGH_TURNOVER', 'result': 'PASS', 'limit': 0.7, 'value': 0.0176}, {'name': 'CONCENTRATED_WEIGHT', 'result': 'PASS'}, {'name': 'LOW_SUB_UNIVERSE_SHARPE', 'result': 'PASS', 'limit': 0.53, 'value': 0.65}, {'name': 'SELF_CORRELATION', 'result': 'PENDING'}, {'name': 'MATCHES_COMPETITION', 'result': 'PASS', 'competitions': [{'id': 'challenge', 'name': 'Challenge'}]}]}, 'os': None, 'train': None, 'test': None, 'prod': None, 'competitions': None, 'themes': None, 'pyramids': None, 'pyramidThemes': None, 'team': None}
#     ]
# }

alphas = sim_resp.json()["results"]
print(len(alphas))
for alpha in alphas:
    success = 1
    for check in alpha["is"]["checks"]:
        if check["result"] == "FAIL":
            success = 0
            break
    if success == 1:
        print(alpha["id"])
