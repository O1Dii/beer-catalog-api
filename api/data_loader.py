import requests

from api import base_url
from api.models import Beer, Fermentation, Hops, Malt, Mash, Method, Yeast, db
from api.utils.deserializers import (beer_deserializer, fermentation_deserializer, hops_deserializer, malt_deserializer,
                                     mash_deserializer, method_deserializer, yeast_deserializer)


class DataLoader:
    @classmethod
    def __add_collection_to_db(cls, collection, model, deserializer_function):
        result = []

        for item in collection:
            arguments = deserializer_function(item)

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

    @classmethod
    def __process_beers_dict(cls, beers):
        for beer_dict in beers:
            beer_arguments = beer_deserializer(beer_dict)
            beer = Beer(**beer_arguments)

            method_arguments = method_deserializer(beer_dict)
            method = Method(**method_arguments)

            beer.method = method

            yeast_arguments = yeast_deserializer(beer_dict)
            yeast = cls.__create_and_add_to_db(Yeast, yeast_arguments)

            beer.yeast = yeast

            fermentation_arguments = fermentation_deserializer(beer_dict)
            fermentation = cls.__create_and_add_to_db(Fermentation, fermentation_arguments)

            method.fermentation = fermentation

            mashes = cls.__add_collection_to_db(beer_dict['method']['mash_temp'], Mash, mash_deserializer)
            cls.__add_relations(mashes, method.mash_temp)

            hops = cls.__add_collection_to_db(beer_dict['ingredients']['hops'], Hops, hops_deserializer)
            cls.__add_relations(hops, beer.hops)

            malts = cls.__add_collection_to_db(beer_dict['ingredients']['malt'], Malt, malt_deserializer)
            cls.__add_relations(malts, beer.malt)

    @classmethod
    def load_data(cls, pages=1):
        try:
            for page in range(1, int(pages) + 1):
                beers = requests.get(base_url, {'page': page}).json()

                cls.__process_beers_dict(beers)

            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
