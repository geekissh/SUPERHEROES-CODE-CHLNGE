from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/heroes')
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

@app.route('/heroes/<int:id>')
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict_with_powers())
    else:
        return jsonify({'error': 'Hero not found'}), 404

@app.route('/powers')
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def handle_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    
    if request.method == 'GET':
        return jsonify(power.to_dict())

    if request.method == 'PATCH':
        data = request.json
        if 'description' in data:
            description = data['description']
            if len(description) >= 20:
                power.description = description
                db.session.commit()
                return jsonify(power.to_dict())
            else:
                return jsonify({'errors': ['Description must be at least 20 characters']}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    if not all([strength, power_id, hero_id]):
        return jsonify({'errors': ['Missing data']}), 400

    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({'errors': ['Invalid strength']}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return jsonify({'errors': ['Hero or Power not found']}), 404

    hero_power = HeroPower(strength=strength, hero=hero, power=power)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify(hero_power.to_dict()), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
