import requests

from api import base_url
from api.models import Beer, Fermentation, Hops, Malt, Mash, Method, Yeast, db


class Data:
    @classmethod
    def __add_collection_to_db(cls, collection, model, get_arguments_function):
        result = []

        for item in collection:
            arguments = get_arguments_function(item)

            current_object = cls.__create_and_add_to_db(model, arguments)

            result.append(current_object)

        return result

    @staticmethod
    def __add_relations(collection, container_collection):
        for item in collection:
            container_collection.append(item)

    @staticmethod
    def __create_and_add_to_db(model, item_arguments):
        result = model.query.filter_by(**item_arguments).first()

        if not result:
            result = model(**item_arguments)
            db.session.add(result)

        return result

    @staticmethod
    def __get_beer_arguments(beer):
        return {
            'id': beer['id'],
            'name': beer['name'],
            'tagline': beer['tagline'],
            'description': beer['description'],
            'image_url': beer['image_url'],
            'abv': beer['abv'],
            'ibu': beer['ibu'],
            'ebc': beer['ebc'],
            'food_pairing': beer['food_pairing'],
            'brewers_tips': beer['brewers_tips'],
        }

    @staticmethod
    def __get_method_arguments(beer):
        return {
            'twist': beer['method']['twist'],
        }

    @staticmethod
    def __get_mash_arguments(mash):
        return {
            'duration': mash['duration'],
            'value': mash['temp']['value'],
            'unit': mash['temp']['unit'],
        }

    @staticmethod
    def __get_fermentation_arguments(beer):
        fermentation = beer['method']['fermentation']

        return {
            'value': fermentation['temp']['value'],
            'unit': fermentation['temp']['unit'],
        }

    @staticmethod
    def __get_hops_arguments(hops):
        return {
            'name': hops['name'],
            'amount_value': hops['amount']['value'],
            'amount_unit': hops['amount']['unit'],
            'add': hops['add'],
        }

    @staticmethod
    def __get_malt_arguments(malt):
        return {
            'name': malt['name'],
            'amount_value': malt['amount']['value'],
            'amount_unit': malt['amount']['unit'],
        }

    @staticmethod
    def __get_yeast_arguments(beer):
        return {
            'name': beer['ingredients']['yeast'],
        }

    @classmethod
    def __process_beers_dict(cls, beers):
        for beer_dict in beers:
            beer_arguments = cls.__get_beer_arguments(beer_dict)
            beer = Beer(**beer_arguments)

            method_arguments = cls.__get_method_arguments(beer_dict)
            method = Method(**method_arguments)

            beer.method = method

            yeast_arguments = cls.__get_yeast_arguments(beer_dict)
            yeast = cls.__create_and_add_to_db(Yeast, yeast_arguments)

            beer.yeast = yeast

            fermentation_arguments = cls.__get_fermentation_arguments(beer_dict)
            fermentation = cls.__create_and_add_to_db(Fermentation, fermentation_arguments)

            method.fermentation = fermentation

            mashes = cls.__add_collection_to_db(beer_dict['method']['mash_temp'], Mash, cls.__get_mash_arguments)

            cls.__add_relations(mashes, method.mashes)

            hops = cls.__add_collection_to_db(beer_dict['ingredients']['hops'], Hops, cls.__get_hops_arguments)

            cls.__add_relations(hops, beer.hops)

            malts = cls.__add_collection_to_db(beer_dict['ingredients']['malt'], Malt, cls.__get_malt_arguments)

            cls.__add_relations(malts, beer.malts)

    @classmethod
    def load_data(cls, pages=1):
        db.drop_all()
        db.create_all()

        try:
            for page in range(1, pages + 1):
                beers = requests.get(base_url, {'page': page}).json()

                cls.__process_beers_dict(beers)

            db.session.commit()
        except Exception as e:
            print('exception', e)
            db.session.rollback()
