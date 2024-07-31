from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from bson import ObjectId
from flask import send_file
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['interventions_db']
collection = db['interventions']
users_collection = db['users']

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({'_id': user_id})
    if user:
        return User(user_id)
    return None

class RegistrationForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('S’inscrire')

class LoginForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Ancien mot de passe', validators=[DataRequired()])
    new_password = PasswordField('Nouveau mot de passe', validators=[DataRequired()])
    submit = SubmitField('Changer mot de passe')


def generer_pdf(demande):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Ajoutez le contenu au PDF
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, f"Date d'émission: {demande['date_emission']}")
    p.drawString(100, 730, f"Émetteur: {demande['emetteur']}")
    p.drawString(100, 710, f"Département/Service: {demande['department']}")
    p.drawString(100, 690, f"Anomalie détectée: {demande['anomalie_detectee']}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer
@app.route('/telecharger_pdf/<demande_id>')
@login_required
def telecharger_pdf(demande_id):
    try:
        obj_id = ObjectId(demande_id)
        demande = collection.find_one({'_id': obj_id})
        if not demande:
            flash('Aucune demande trouvée pour cet ID.', 'warning')
            return redirect(url_for('index'))
        
        pdf_buffer = generer_pdf(demande)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='demande_intervention.pdf'
        )
    except Exception as e:
        flash(f'Erreur lors de la génération du PDF : {str(e)}', 'error')
        return redirect(url_for('index'))
    
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        data = {
            'date_emission': request.form.get('date_emission', ''),
            'emetteur': request.form.get('emetteur', ''),
            'department': request.form.get('department', ''),
            'anomalie_detectee': request.form.get('anomalie_detectee', ''),
        }
        try:
            result = collection.insert_one(data)
            demande_id = result.inserted_id
            return redirect(url_for('results', demande_id=str(demande_id)))
        except Exception as e:
            flash(f'Erreur lors de l\'insertion des données : {str(e)}', 'error')
            return render_template('index.html')
    return render_template('index.html')

@app.route('/results')
@login_required
def results():
    demande_id = request.args.get('demande_id')
    if demande_id:
        try:
            obj_id = ObjectId(demande_id)
            demande = collection.find_one({'_id': obj_id})
            if not demande:
                flash('Aucune demande trouvée pour cet ID.', 'warning')
                return redirect(url_for('index'))
            # Ajoutez cette ligne pour inclure l'ID de la demande dans le contexte
            demande['_id'] = str(demande['_id'])
        except Exception as e:
            flash(f'Erreur lors de la récupération de la demande : {str(e)}', 'error')
            demande = None
    else:
        flash('Aucun ID de demande fourni.', 'warning')
        demande = None
    return render_template('results.html', demande=demande)

@app.route('/search', methods=['GET'])
@login_required
def search():
    emetteur = request.args.get('search_emetteur', '')
    if emetteur:
        try:
            demandes = list(collection.find({'emetteur': emetteur}))
        except Exception as e:
            flash(f'Erreur lors de la recherche : {str(e)}', 'error')
            demandes = []
    else:
        demandes = []
    return render_template('results1.html', demandes=demandes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        
        # Vérifier si l'utilisateur existe déjà
        if users_collection.find_one({'_id': username}):
            flash('Nom d’utilisateur déjà pris. Essayez un autre.', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        try:
            users_collection.insert_one({'_id': username, 'password': hashed_password})
            flash('Vous vous êtes inscrit avec succès !', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Erreur lors de l\'inscription : {str(e)}', 'error')
    
    # Afficher les erreurs de validation du formulaire
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{form[field].label.text} : {error}', 'error')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = users_collection.find_one({'_id': username})
        if user and check_password_hash(user['password'], password):
            login_user(User(user['_id']))
            return redirect(url_for('index'))
        else:
            flash('Nom d’utilisateur ou mot de passe incorrect.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        username = current_user.id
        old_password = form.old_password.data
        new_password = form.new_password.data
        
        user = users_collection.find_one({'_id': username})
        
        if user and check_password_hash(user['password'], old_password):
            hashed_new_password = generate_password_hash(new_password)
            users_collection.update_one({'_id': username}, {'$set': {'password': hashed_new_password}})
            flash('Votre mot de passe a été modifié avec succès.', 'success')
            return redirect(url_for('change_password'))
        else:
            flash('Mot de passe actuel incorrect.', 'error')
    
    return render_template('change_password.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
