import os

from setupDB import create_db
from flask import *
from models import *
from controllers import *


relative_path = os.path.dirname(os.path.realpath(__file__)) + '/db/'

@app.route('/')
def index():
    return render_template('splash.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/characters/null')
@app.route('/species/null')
@app.route('/planets/null')
@app.route('/planets/Unknown')
@app.route('/characters/Unknown')
@app.route('/species/Unknown')
def unknown():
    return render_template('unknown.html')

# ----------
# characters
# ----------

@app.route('/api/characters', methods=['GET'])
def get_characters():
    return json.dumps([i.serialize for i in Character.get_all()], indent=4)

@app.route('/api/characters/<name>')
def get_character_detail(name):
    if not Character.get(name):
        abort(404)
    else: return json.dumps(Character.get(str(name)).serialize, indent=4)

@app.route('/characters')
@app.route('/characters/<character>')
def characters(character=None):

    if character is not None:
        return render_template('character.html', character=Character.get(character))
    else:
        all_characters = Character.get_all()

    return render_template('characters.html', all_characters=all_characters)

# -------
# planets
# -------

@app.route('/api/planets', methods=['GET'])
def get_planets():
    return json.dumps([i.serialize for i in Planet.get_all()], indent=4)
    
@app.route('/api/planets/<name>')
def get_planet_detail(name):
    if not Planet.get(name):
        abort(404) 
    return json.dumps(Planet.get(str(name)).serialize, indent=4)

@app.route('/planets')
@app.route('/planets/<planet>')
def planets(planet=None):

    if planet is not None:
        return render_template('planet.html', planet=Planet.get(planet))
    else:
        all_planets = Planet.get_all()

    return render_template('planets.html', all_planets=all_planets)

# -------
# species
# -------

@app.route('/api/species', methods=['GET'])
def get_species():
    return json.dumps([i.serialize for i in Species.get_all()],indent=4)

@app.route('/api/species/<name>')
def get_species_detail(name):
    if not Species.get(name):
        abort(404)
    else: return json.dumps(Species.get(str(name)).serialize, indent=4)

@app.route('/species')
@app.route('/species/<species>')
def species(species=None):

    if species is not None:
        return render_template('specie.html', species=Species.get(species))
    else:
        all_species = Species.get_all()

    return render_template('species.html', all_species=all_species)

# -------
# League API
# -------

@app.route('/league')
def league():
    all_champions = league_controller()
    return render_template('league.html', all_champions=all_champions)

# ---------
# UnitTests
# ---------

@app.route('/api/tests', methods=['GET'])
def run_tests():
    return render_template('tests.html', result=test_controller())

# -------
# Search
# -------

@app.route('/search/query=<query>')
def search(query=None):
    search_results = search_controller(query)

    if 'single' in search_results:
        return render_template('one_search_term.html', results=search_results)
    else:
        return render_template('multiple_search_terms.html', results=search_results)


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
