from flask import Blueprint, render_template

bp = Blueprint('user', __name__, url_prefix='/result')

@bp.route('/', methods=['POST','GET'])
def index():
    return render_template('result.html')
