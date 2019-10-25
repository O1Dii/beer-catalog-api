def beer_deserializer(beer):
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


def method_deserializer(beer):
    return {
        'twist': beer['method']['twist'],
    }


def mash_deserializer(mash):
    return {
        'duration': mash['duration'],
        'value': mash['temp']['value'],
        'unit': mash['temp']['unit'],
    }


def fermentation_deserializer(beer):
    fermentation = beer['method']['fermentation']

    return {
        'value': fermentation['temp']['value'],
        'unit': fermentation['temp']['unit'],
    }


def hops_deserializer(hops):
    return {
        'name': hops['name'],
        'value': hops['amount']['value'],
        'unit': hops['amount']['unit'],
        'add': hops['add'],
    }


def malt_deserializer(malt):
    return {
        'name': malt['name'],
        'value': malt['amount']['value'],
        'unit': malt['amount']['unit'],
    }


def yeast_deserializer(beer):
    return {
        'name': beer['ingredients']['yeast'],
    }
