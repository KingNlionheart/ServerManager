from . import web
from app.libs.server_scan import scan
# 测试数据暂时存放
datas = {
    'hostnames':[],
    'hosts':{}
}


@web.route('/update_data/', methods=['POST'])
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



@web.route('/get_hostname/', methods=['GET'])
def get_hostname():
    # 没有指定id则返回全部
    return jsonify(datas['hostnames'])


@web.route('/get_data/', methods=['GET'])
def get_data():
    if not request.args or 'hostname' not in request.args:
        # 没有指定id则返回全部
        return jsonify(datas['hosts'])
    else:
        host=datas['hosts'].get(request.args['hostname'])
        return jsonify(host) if host else jsonify({'result': 'not found'})
