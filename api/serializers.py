from marshmallow import EXCLUDE, fields, post_dump, pre_load

from api import ma
from api.models import Beer, Fermentation, Hops, Malt, Mash, Method, Yeast
from api.utils import unwrap_data, wrap_data


class MashSchema(ma.ModelSchema):
    class Meta:
        model = Mash
        fields = ['value', 'unit', 'duration']
        unknown = EXCLUDE

    @post_dump
    def add_missing_layers(self, data, **kwargs):
        return wrap_data(data, 'temp', ['value', 'unit'])

    @pre_load
    def remove_layers(self, data, **kwargs):
        return unwrap_data(data, 'temp')


class FermentationSchema(ma.ModelSchema):
    class Meta:
        model = Fermentation
        fields = ['value', 'unit']
        unknown = EXCLUDE

    @post_dump
    def add_missing_layers(self, data, **kwargs):
        return wrap_data(data, 'temp', ['value', 'unit'])

    @pre_load
    def remove_layers(self, data, **kwargs):
        return unwrap_data(data, 'temp')


class MethodSchema(ma.ModelSchema):
    class Meta:
        model = Method
        fields = ['fermentation', 'mash_temp', 'twist']
        unknown = EXCLUDE

    mash_temp = ma.Nested('MashSchema', many=True)
    fermentation = ma.Nested('FermentationSchema')


class MaltSchema(ma.ModelSchema):
    class Meta:
        model = Malt
        fields = ['name', 'unit', 'value']
        unknown = EXCLUDE

    @post_dump
    def add_missing_layers(self, data, **kwargs):
        return wrap_data(data, 'amount', ['unit', 'value'])

    @pre_load
    def remove_layers(self, data, **kwargs):
        return unwrap_data(data, 'amount')


class HopsSchema(ma.ModelSchema):
    class Meta:
        model = Hops
        fields = ['name', 'value', 'unit', 'add']
        unknown = EXCLUDE

    @post_dump
    def add_missing_layers(self, data, **kwargs):
        return wrap_data(data, 'amount', ['unit', 'value'])

    @pre_load
    def remove_layers(self, data, **kwargs):
        return unwrap_data(data, 'amount')


class YeastSchema(ma.ModelSchema):
    class Meta:
        model = Yeast
        fields = ['name']
        unknown = EXCLUDE

    @post_dump
    def convert_to_string(self, data, **kwargs):
        return data['name']

    @pre_load
    def convert_to_dict(self, data, **kwargs):
        return {'name': data}


class BeerSchema(ma.ModelSchema):
    class Meta:
        model = Beer
        unknown = EXCLUDE

    malt = fields.Nested('MaltSchema', many=True)
    hops = fields.Nested('HopsSchema', many=True)
    yeast = fields.Nested('YeastSchema')
    method = fields.Nested('MethodSchema')

    @post_dump(pass_many=True)
    def add_missing_layers(self, data, many, **kwargs):
        if many:
            result = []

            for each in data:
                result.append(wrap_data(each, 'ingredients', ['malt', 'hops', 'yeast']))

            return result

        return wrap_data(data, 'ingredients', ['malt', 'hops', 'yeast'])

    @pre_load(pass_many=True)
    def remove_layers(self, data, many, **kwargs):
        if many:
            result = []

            for each in data:
                result.append(unwrap_data(each, 'ingredients'))

            return result

        return unwrap_data(data, 'ingredients')


schema = BeerSchema()
