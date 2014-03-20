#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import Flask,jsonify
from werkzeug import cached_property
from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery

from gevent.monkey import patch_all
patch_all()
from psycogreen.gevent import patch_psycopg
patch_psycopg()


app = Flask(__name__)
app.config.from_pyfile('config.py')


db = SQLAlchemy(app)
db.engine.pool._use_threadlocal = True


class AsyndbQuery(BaseQuery):

    '''Provide all kinds of query functions.'''

    def jsonify(self):
        '''Converted datas into JSON.'''
        for item in self.all():
            yield item.as_dict


class Ayndb(db.Model):
    query_class = AsyndbQuery

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    done = db.Column(db.Boolean)
    priority = db.Column(db.Integer)

    @cached_property
    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done,
            'priority': self.priority
        }


@app.route('/test/postgres/')
def sleep_postgres():
    db.session.execute('SELECT pg_sleep(5)')
    return jsonify(data = list(Ayndb.query.jsonify()))


def create_data():
    """ A helper function to create our tables and some Todo objects.
    """
    db.create_all()
    alldata = []
    for i in range(50):
        item = Ayndb(
            title="test for postgres,this is {0}".format(i),
            done=(i % 2 == 0),
            priority=(i % 5)
        )
        alldata.append(item)
    db.session.add_all(alldata)
    db.session.commit()
    db.session.close()


if __name__ == '__main__':

    if '-c' in sys.argv:
        create_data()
    else:
        #app.run()
        
        from gevent.pywsgi import WSGIServer
        http_server = WSGIServer(('', 8080), app)
        http_server.serve_forever()
        
