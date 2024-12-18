from flask import Flask, render_template, request, redirect, url_for, jsonify
import openpyxl

app = Flask(__name__, template_folder='.')

# Route pour afficher la page d'accueil (index.html)
@app.route('/')
def home():
    return render_template('index.html')

# Route pour afficher la page d'ajout (ajout.html)
@app.route('/add_etudiant')
def add_etudiant_form():
    return render_template('ajout.html')

# Route pour afficher la page "Our Team" (ourteam.html)
@app.route('/ourteam')
def our_team():
    return render_template('ourteam.html')

@app.route('/list_etudiants') 
def list_etudiants(): 
    workbook = openpyxl.load_workbook('etudiants.xlsx') 
    sheet = workbook.active 
    students = [] 
    for row in sheet.iter_rows(min_row=2, values_only=True):    
         students.append(row) 
    return render_template('tables.html',students=students)

# Route pour ajouter un étudiant depuis le formulaire dans ajout.html
@app.route('/add_etudiant', methods=['POST'])
def add_etudiant():
    if request.is_json:
        data = request.get_json()
        nom = data['nom']
        prenom = data['prenom']
        age = data['age']
        email = data['email']
        gouvernorat = data['gouvernorat']
        specialite = data['specialite']
        moyenne = data['moyenne']
        

        # Ouvrir ou créer le fichier Excel
        try:
            workbook = openpyxl.load_workbook('etudiants.xlsx')
            sheet = workbook.active
        except FileNotFoundError:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(["Nom", "Prenom", "Age", "Email", "Gouvernorat", "Specialité", "Moyenne"])  # En-têtes

        # Ajouter les données dans le fichier Excel
        sheet.append([nom, prenom, age, email, gouvernorat, specialite, moyenne])
        workbook.save('etudiants.xlsx')

        return jsonify({"message": "Étudiant ajouté avec succès."}), 200
    else:
        return jsonify({"message": "Format de données non supporté."}), 400

if __name__ == '__main__':
    app.run(debug=True)
