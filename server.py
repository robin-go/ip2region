from flask import Flask, jsonify
from ip2Region import Ip2Region

app = Flask(__name__)
searcher = Ip2Region('data/ip2region.db')


@app.route('/ip2region/<ip>')
def query(ip):
    if not searcher.isip(ip):
        return jsonify({'error_code': 4000, 'desc': '[Error]: Invalid ip address.'})

    data = searcher.btreeSearch(ip)
    if isinstance(data, dict):
        region_list = data['region'].decode('utf8').split('|')
        data = {
            'country': region_list[0],
            'province': region_list[2],
            'city': region_list[3],
        }
        return jsonify(data)
    else:
        return jsonify({'error_code': 4001, 'desc': '[Error]: Query failed.'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
