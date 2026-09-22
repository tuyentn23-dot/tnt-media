"""TNT Media Web Server - Serves Dashboard + API"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_cors import CORS

from core.orchestrator import TNTMediaOrchestrator
from core.service_registry import ServiceRegistry
from utils.config import config
from utils.logger import logger

app = Flask(__name__, 
            static_folder='web/static',
            template_folder='web/templates')
CORS(app)

# Initialize components
orchestrator = TNTMediaOrchestrator()
service_registry = ServiceRegistry()
service_registry.scan_services()


@app.route('/')
def index():
    """Serve dashboard HTML"""
    template_path = Path(__file__).parent / 'web' / 'templates' / 'index.html'
    if template_path.exists():
        return template_path.read_text(encoding='utf-8')
    return "<h1>TNT Media Dashboard</h1><p>Dashboard template not found</p>"


@app.route('/api/status')
def get_status():
    """Get full system status"""
    return jsonify({
        'success': True,
        'active': orchestrator.current_workflow is not None,
        'workflow': orchestrator.get_status(),
        'services': {
            'total': len(service_registry.services),
            'loaded': service_registry.get_loaded_count(),
            'failed': service_registry.get_failed_count()
        },
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/services')
def get_services():
    """List all services"""
    return jsonify({
        'success': True,
        'services': service_registry.list_services()
    })


@app.route('/api/workflows')
def get_workflows():
    """List all workflows"""
    workflows = []
    if orchestrator.current_workflow:
        workflows.append(orchestrator.current_workflow.to_dict())
    workflows.extend([w.to_dict() for w in orchestrator.workflow_history])
    
    return jsonify({
        'success': True,
        'workflows': workflows,
        'count': len(workflows)
    })


@app.route('/api/workflow/start', methods=['POST'])
def start_workflow():
    """Start a new workflow"""
    data = request.get_json()
    if not data or 'type' not in data:
        return jsonify({'success': False, 'error': 'Workflow type required'}), 400
    
    workflow_id = orchestrator.start_workflow(
        data['type'],
        data.get('params', {})
    )
    
    return jsonify({
        'success': True,
        'workflow_id': workflow_id,
        'message': f'Workflow {workflow_id} started'
    })


@app.route('/api/workflow/<workflow_id>/approve', methods=['POST'])
def approve_workflow(workflow_id):
    """Approve workflow for publishing"""
    if orchestrator.current_workflow and orchestrator.current_workflow.id == workflow_id:
        orchestrator.update_state(orchestrator.current_workflow.state, "Reviewing for approval")
        if orchestrator.approve_publish():
            return jsonify({'success': True, 'message': 'Workflow approved'})
    
    return jsonify({'success': False, 'error': 'Workflow not found or cannot approve'}), 400


@app.route('/api/workflow/<workflow_id>/cancel', methods=['POST'])
def cancel_workflow(workflow_id):
    """Cancel a workflow"""
    if orchestrator.current_workflow and orchestrator.current_workflow.id == workflow_id:
        orchestrator.fail_workflow('Cancelled by user')
        return jsonify({'success': True, 'message': 'Workflow cancelled'})
    
    return jsonify({'success': False, 'error': 'Workflow not found'}), 404


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'healthy': True,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/backup', methods=['POST'])
def create_backup():
    """Create system backup"""
    try:
        from utils.database import DatabaseManager
        db = DatabaseManager()
        backup_path = db.backup_database()
        return jsonify({
            'success': True,
            'backup_path': backup_path,
            'message': 'Backup created successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    host = config.get('env.API_HOST', '0.0.0.0')
    port = config.get('env.API_PORT', 8000)
    debug = config.get('env.API_DEBUG', True)
    
    print("\n" + "="*60)
    print("  TNT Media Dashboard")
    print("  http://localhost:8000")
    print("="*60 + "\n")
    
    app.run(host=host, port=port, debug=debug)
