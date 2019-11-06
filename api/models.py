from api import db

malt_beer_table = db.Table('malt_beer', db.Column('beer_id', db.Integer, db.ForeignKey('beer.id')),
                           db.Column('malt_id', db.Integer, db.ForeignKey('malt.id')))

hops_beer_table = db.Table('hops_beer', db.Column('beer_id', db.Integer, db.ForeignKey('beer.id')),
                           db.Column('hops_id', db.Integer, db.ForeignKey('hops.id')))

mash_method_table = db.Table('mash_method', db.Column('method_id', db.Integer, db.ForeignKey('method.id')),
                             db.Column('mash_id', db.Integer, db.ForeignKey('mash.id')))


class Mash(db.Model):
    __tablename__ = 'mash'

    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer)
    value = db.Column(db.Integer)
    unit = db.Column(db.String(20))

    def __repr__(self):
        return f'Mash {self.id=} {self.duration=} {self.value=} {self.unit=}'


class Fermentation(db.Model):
    __tablename__ = 'fermentation'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    unit = db.Column(db.String(20))

    def __repr__(self):
        return f'Fermentation {self.id=} {self.value=} {self.unit=}'


class Method(db.Model):
    __tablename__ = 'method'

    id = db.Column(db.Integer, primary_key=True)
    twist = db.Column(db.String(500))

    fermentation_id = db.Column(db.Integer, db.ForeignKey('fermentation.id'))

    mash_temp = db.relationship('Mash', backref='methods', secondary=mash_method_table)
    fermentation = db.relationship('Fermentation', backref='methods')

    def __repr__(self):
        return f'Method {self.id=} {self.twist=} {self.mash_temp=} {self.fermentation=}'


class Hops(db.Model):
    __tablename__ = 'hops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    value = db.Column(db.Float)
    unit = db.Column(db.String(20))
    add = db.Column(db.String(10))


class Malt(db.Model):
    __tablename__ = 'malt'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    value = db.Column(db.Float)
    unit = db.Column(db.String(20))


class Yeast(db.Model):
    __tablename__ = 'yeast'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f'Yeast {self.id=} {self.name=}'


class Beer(db.Model):
    __tablename__ = 'beer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    tagline = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    image_url = db.Column(db.String(100))
    abv = db.Column(db.Float)
    ibu = db.Column(db.Float)
    ebc = db.Column(db.Float)
    food_pairing = db.Column(db.ARRAY(db.String(100), True))
    brewers_tips = db.Column(db.String(300))

    method_id = db.Column(db.Integer, db.ForeignKey('method.id'))
    yeast_id = db.Column(db.Integer, db.ForeignKey('yeast.id'))

    method = db.relationship('Method', backref='beer', uselist=False)
    malt = db.relationship('Malt', backref='beers', secondary=malt_beer_table)
    hops = db.relationship('Hops', backref='beers', secondary=hops_beer_table)
    yeast = db.relationship('Yeast', backref='beers')

    def __repr__(self):
        return f'Beer {self.id=} {self.name=} {self.yeast=} {self.hops=} {self.malt=} {self.method=}'
