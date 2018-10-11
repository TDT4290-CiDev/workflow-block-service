from flask import Flask, jsonify
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
            'description': info['description']
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
        return 404, 'No block with that name exists.'

    return jsonify(block.get_info())


# Only for testing purposes - should use WSGI server in production
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
