import requests
from flask import Flask, request, jsonify
from flask.views import MethodView
from db import Advertising, Session
from errors import HttpError
from scheama import validate_create_advertising
from sqlalchemy.exc import IntegrityError

app = Flask("server")

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({"status": "error", "description": error.message})
    http_response.status_code = error.status_code
    return http_response

def get_advertising(advertising_id: int, session: Session):
    advertising = session.query(Advertising).get(advertising_id)
    if advertising is None:
        raise HttpError(404, "advertising not found")
    return advertising

class advertisingView(MethodView):

    def get(self, header_id: int):
        with Session() as session:
            advertising = get_advertising(header_id, session)
            return jsonify(
                {
                    "id": advertising.id,
                    "header": advertising.header,
                    "description": advertising.description,
                    "creation_time": advertising.creation_time.isoformat(),
                    "user": advertising.user
                }
            )

    def post(self):
        json_data = validate_create_advertising(request.json)
        with Session() as session:
            new_advertising = Advertising(**json_data)
            session.add(new_advertising)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "header already exists")
            return jsonify(
                {
                    "id": new_advertising.id,
                    "creation_time": int(new_advertising.creation_time.timestamp())
                }
            )

    def patch(self, header_id: int):
        json_data = request.json
        with Session() as session:
            advertising = get_advertising(header_id, session)
            for field, value in json_data.items():
               setattr(advertising, field, value)
            session.add(advertising)
            session.commit()
        return jsonify({"Status": "ok"})

    def delete(self, header_id: int):
        with Session() as session:
            advertising = get_advertising(header_id, session)
            session.delete(advertising)
            session.commit()
            return jsonify({"Status": "ok"})

app.add_url_rule('/advertising/<int:header_id>', view_func=advertisingView.as_view('adv_with_id'), methods=["GET", "PATCH", "DELETE"])
app.add_url_rule('/advertising', view_func=advertisingView.as_view('adv'), methods=["POST"])
app.run(port=5000)