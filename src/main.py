from flask import Flask, request, jsonify
from ingest import ing
est_data


@app.route('/ingest', methods=['POST'])
def ingest_endpoint():
    app.run(debug=True)
    """ """
