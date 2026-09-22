"""TNT Media API Server - Flask-based"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from core.orchestrator import TNTMediaOrchestrator
from utils.config import config
from utils.logger import logger

app = Flask(__name__)
CORS(app)

orchestrator = TNTMediaOrchestrator()


@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'success': True,
        'status': orchestrator.get_status(),
        'version': '5.0.0'
    })


@app.route('/api/workflow/start', methods=['POST'])
def start_workflow():
    data = request.get_json()
    workflow_type = data.get('type')
    params = data.get('params', {})
    
    if not workflow_type:
        return jsonify({'success': False, 'error': 'Missing workflow type'}), 400
    
    workflow_id = orchestrator.start_workflow(workflow_type, params)
    return jsonify({'success': True, 'workflow_id': workflow_id})


@app.route('/api/workflow/current', methods=['GET'])
def get_current_workflow():
    workflow = orchestrator.get_current_workflow()
    if workflow:
        return jsonify({'success': True, 'workflow': workflow.to_dict()})
    return jsonify({'success': True, 'workflow': None})


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'success': True, 'healthy': True})


if __name__ == '__main__':
    host = config.get('env.API_HOST', '0.0.0.0')
    port = config.get('env.API_PORT', 8000)
    debug = config.get('env.API_DEBUG', False)
    
    app.run(host=host, port=port, debug=debug)
