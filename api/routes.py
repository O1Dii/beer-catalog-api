from flask import jsonify, request

from api import app
from api.models import Beer
from api.serializers import schema


@app.route('/')
def index():
    per_page = request.args.get('per_page') or 25
    page = request.args.get('page') or 1
    ids = request.args.get('ids')
    abv_gt = request.args.get('abv_gt')
    abv_lt = request.args.get('abv_lt')
    ibu_gt = request.args.get('ibu_gt')
    ibu_lt = request.args.get('ibu_lt')
    ebc_gt = request.args.get('ebc_gt')
    ebc_lt = request.args.get('ebc_lt')
    beer_name = request.args.get('beer_name')

    beers = Beer.query

    try:
        if ids:
            ids_list = ids.split('|')
            ids_int_list = map(int, ids_list)

            beers = beers.filter(Beer.id.in_(ids_int_list))

        if beer_name:
            beers = beers.filter(Beer.name.ilike(f'%{beer_name}%'))

        if abv_gt:
            beers = beers.filter(Beer.abv > float(abv_gt))

        if abv_lt:
            beers = beers.filter(Beer.abv < float(abv_lt))

        if ibu_gt:
            beers = beers.filter(Beer.ibu > float(ibu_gt))

        if ibu_lt:
            beers = beers.filter(Beer.ibu < float(ibu_lt))

        if ebc_gt:
            beers = beers.filter(Beer.ebc > float(ebc_gt))

        if ebc_lt:
            beers = beers.filter(Beer.ebc < float(ebc_lt))

        beers = beers.paginate(per_page=int(per_page), page=int(page))
    except ValueError:
        return jsonify(None)

    return schema.jsonify(beers.items, many=True)


@app.route('/<int:beer_id>')
def get_beer(beer_id):
    return schema.jsonify(Beer.query.get(beer_id))
