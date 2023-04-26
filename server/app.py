#!/usr/bin/env python3

from flask import Flask, jsonify,  make_response
from flask_migrate import Migrate
from ipdb import set_trace

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)                                       
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  #set up to point to our existing database of app.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        #set to false to avoid buliding up too much unhelpful data in memory while app is running

migrate = Migrate(app, db)          #this creates a Migrate instance that configures thte app and modesl for Flask-Migrate

db.init_app(app)                    #connects our database to our application before it runs

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    # set_trace()
    return f'''
    <ul>ID: {animal.id}</ul>
    <ul>Name: {animal.name}</ul>
    <ul>Species: {animal.species}</ul>
    <ul>Zookeeper: {animal.zookeeper.name}</ul>
    <ul>Enclosure: {animal.enclosure.environment}</ul>

    '''
    

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    animals = zookeeper.animals
    list_of_animals = f''
    for animal in animals:
       list_of_animals += f'<ul>Animal: {animal.name}</ul>\n'
    
    response = f'''
        <ul>ID: {zookeeper.id}</ul>
        <ul>Name: {zookeeper.name}</ul>
        <ul>Birthday: {zookeeper.birthday}</ul>
        {list_of_animals}
        '''
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    animals = enclosure.animals
    list_of_animals = f''
    for animal in animals:
       list_of_animals += f'<ul>Animal: {animal.name}</ul>\n'
    
    response = f'''
        <ul>ID: {enclosure.id}</ul>
        <ul>Environment: {enclosure.environment}</ul>
        <ul>Open to Visitors: {enclosure.open_to_visitors}</ul>
        {list_of_animals}
        '''
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
