from flask import Flask, jsonify, request
import block_manager

app = Flask(__name__)


@app.route('/discovery', methods=['GET'])
def discovery():
    """
    Returns a list of all registered blocks.
    """
    result = {}
    result['blocks'] = []

    for name, block in block_manager.blocks.items():
        info = block.get_info()
        result['blocks'].append({
            'name': name,
            'description': info['description'],
            'links': {
                'root': request.script_root + '/' + name,
                'info': request.script_root + '/' + name + '/info',
                'resume': request.script_root + '/' + name + '/resume',
            }
        })

    return jsonify(result)


@app.route('/<block_name>/info', methods=['GET'])
def get_block_info(block_name):
    """
    Returns info about block, including description, input parameters, and output.
    """
    try:
        block = block_manager.blocks[block_name]
    except KeyError:
        return 'No block with that name exists.', 404

    return jsonify(block.get_info())


@app.route('/<block_name>', methods=['POST'])
def execute_block(block_name):
    body = request.get_json()

    try:
        block = block_manager.blocks[block_name]
    except KeyError:
        return 'No block with that name exists.', 404

    # Create new dictionary that will only contain parameters included in block specification
    cleaned_params = {}

    for name, param in block.get_info()['params'].items():
        if name not in body['params']:
            return 'Missing parameter ' + name + ".", 400

        if type(body['params'][name]) != block_manager.type_map[param['type']]:
            return 'Invalid type for parameter ' + name + "; expected " + param['type'] + ".", 400

        cleaned_params[name] = body['params'][name]

    result = block.execute(cleaned_params)

    if type(result) == dict:
        response = {
            'type': 'result',
            'data': result
        }
    elif type(result) == tuple:
        status = result[1]
        if status == 'suspend':
            response = {
                'type': 'suspend',
                'state': result[0]
            }
    else:
        return 'Workflow block returned invalid data.', 500

    return jsonify(response)


# Only for testing purposes - should use WSGI server in production
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
