from flask import Flask

app = Flask(__name__)


@app.route('/discovery', methods=['GET'])
def discovery():
    """
    Returns a list of all registered blocks.
    """
    pass


@app.route('/<block_name>/info', methods=['GET'])
def get_block_info(block_name):
    """
    Returns info about block, including description, input parameters, and output.
    """
    pass


# Only for testing purposes - should use WSGI server in production
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
