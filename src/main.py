from flask import Flask, jsonify, request
from http import HTTPStatus

from block_exception import BlockError
import block_manager

app = Flask(__name__)


@app.route('/discovery/', methods=['GET'])
def discovery():
    """
    Returns a list of all registered blocks.
    """
    result = dict()
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


@app.route('/<block_name>/info/', methods=['GET'])
def get_block_info(block_name):
    """
    Returns info about block, including description, input parameters, and output.
    """
    try:
        block = block_manager.blocks[block_name]
    except KeyError:
        return 'No block with that name exists.', HTTPStatus.NOT_FOUND

    return jsonify(block.get_info())


@app.route('/<block_name>', methods=['POST'], strict_slashes=False)
@app.route('/<block_name>/resume', methods=['POST'], strict_slashes=False)
def execute_block(block_name):
    body = request.get_json()
    is_resuming = request.path.endswith(('/resume', '/resume/'))

    if body is None:
        return 'Body must be a JSON object', HTTPStatus.BAD_REQUEST

    try:
        block = block_manager.blocks[block_name]
    except KeyError:
        return 'No block with that name exists.', HTTPStatus.NOT_FOUND

    if is_resuming and 'state' not in body:
        return 'State must be provided when resuming', HTTPStatus.BAD_REQUEST

    # Create new dictionary that will only contain parameters included in block specification
    cleaned_params = dict()

    if is_resuming and 'requested_params' in body['state']:
        requested_params = body['state']['requested_params']
    elif not is_resuming:
        requested_params = block.get_info()['params']
    else:
        requested_params = dict()

    if 'params' not in body and len(requested_params):
        return 'No parameters sent', HTTPStatus.BAD_REQUEST

    for name, param in requested_params.items():
        if name not in body['params']:
            return 'Missing parameter ' + name + ".", HTTPStatus.BAD_REQUEST

        if type(body['params'][name]) != block_manager.type_map[param['type']]:
            return 'Invalid type for parameter ' + name + "; expected " + param['type'] + ".", HTTPStatus.BAD_REQUEST

        cleaned_params[name] = body['params'][name]

    if is_resuming and 'state' not in body:
        return 'State must be sent when resuming', HTTPStatus.BAD_REQUEST

    try:
        if is_resuming:
            result = block.resume(body['state'], cleaned_params)
        else:
            result = block.execute(cleaned_params)
    except BlockError as e:
        return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

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
        return 'Workflow block returned invalid data.', HTTPStatus.INTERNAL_SERVER_ERROR

    return jsonify(response)


# Only for testing purposes - should use WSGI server in production
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
