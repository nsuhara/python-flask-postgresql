"""app/feedback/views/feedback.py
"""

from flask import Blueprint, jsonify, redirect, request, url_for

from feedback.common.utility import err_response
from feedback.models import db
from feedback.models.feedback import Feedback

feedback = Blueprint('feedback', __name__, url_prefix='/feedback')


@feedback.route('/healthcheck', methods=['GET'])
def healthcheck():
    """healthcheck
    """
    return jsonify({
        'status': 'healthy'
    }), 200


@feedback.route('/records', methods=['GET'])
def read_all():
    """read_all
    """
    records = Feedback.query.all()
    return jsonify([record.to_dict() for record in records]), 200


@feedback.route('/records/', methods=['GET'])
def redirect_read_all():
    """redirect_read_all
    """
    return redirect(url_for('feedback.read_all'))


@feedback.route('/records/<int:record_id>', methods=['GET'])
def read_one(record_id=None):
    """read_one
    """
    record = Feedback.query.filter_by(id=record_id).first()
    return jsonify(record.to_dict()), 200


@feedback.route('/records', methods=['POST'])
def create():
    """create
    """
    payload = request.json
    service = payload.get('service')
    title = payload.get('title')
    detail = payload.get('detail')

    record = Feedback(service=service, title=title, detail=detail)
    db.session.add(record)
    db.session.commit()

    response = jsonify(record.to_dict())
    response.headers['Location'] = '/feedback/records/%d' % record.id

    return response, 201


@feedback.route('/records/<int:record_id>', methods=['PUT'])
def update(record_id=None):
    """update
    """
    record = Feedback.query.filter_by(id=record_id).first()

    payload = request.json
    record.service = payload.get('service')
    record.title = payload.get('title')
    record.detail = payload.get('detail')
    db.session.commit()

    return jsonify(record.to_dict()), 204


@feedback.route('/records/<int:record_id>', methods=['DELETE'])
def delete(record_id=None):
    """delete
    """
    record = Feedback.query.filter_by(id=record_id).first()

    db.session.delete(record)
    db.session.commit()

    return jsonify(None), 204


@feedback.errorhandler(404)
@feedback.errorhandler(500)
def errorhandler(error):
    """errorhandler
    """
    return err_response(error=error), error.code
