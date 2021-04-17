from flask import Flask, abort, request, jsonify
from server_test import scan
app = Flask(__name__)

# 测试数据暂时存放
datas = {
    'hostnames':[],
    'hosts':{}
}


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>APIs</h1>'


@app.route('/update_data/', methods=['POST'])
def update_data():
    if not request.json or 'hostname' not in request.json or request.json.get('hostname') not in request.json:
        abort(400)
    #print(request.json)
    hostname = request.json['hostname']
    if hostname not in datas['hostnames']:
        datas['hostnames'].append(hostname)
        datas['hosts'][hostname]=request.json[hostname]
    datas['hosts'][hostname].update(request.json[hostname])
    #用server.py扫描主机
    if request.json[hostname].get('host_ip') :
        datas['hosts'][hostname].update(hosts=scan(request.json[hostname]['host_ip']))
    return jsonify({'result': 'success'})



@app.route('/get_hostname/', methods=['GET'])
def get_hostname():
    # 没有指定id则返回全部
    return jsonify(datas['hostnames'])


@app.route('/get_data/', methods=['GET'])
def get_data():
    if not request.args or 'hostname' not in request.args:
        # 没有指定id则返回全部
        return jsonify(datas['hosts'])
    else:
        host=datas['hosts'].get(request.args['hostname'])
        return jsonify(host) if host else jsonify({'result': 'not found'})


if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", port=5000, debug=True)