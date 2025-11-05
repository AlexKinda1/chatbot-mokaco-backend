from flask import Flask, request, jsonify
from ingest import ingest_data

@app.route('/ingest', methods=['POST'])
def ingest_endpoint():
    """ """