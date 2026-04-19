from flask import  Blueprint,request, jsonify
from services.category_service import CategoryService

log_bp = Blueprint('log_bp', __name__)


@log_bp.route('/logs', methods=['GET'])
def get_logs():
    level = request.args.get('level')
    logs = LogService.get_logs(level=level)
    
    for log in logs:
        log['_id'] = str(log['_id'])
        
    return jsonify({"logs": logs}), 200