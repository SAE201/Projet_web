# app.py
from flask import Flask, render_template, jsonify
from models import (
    get_all_departements,
    get_communes_by_dept,
    get_reseaux_by_commune,
    get_infos_reseau
)

app = Flask(__name__)

# Route principale : rend la page HTML
@app.route("/reseau")
def reseau():
    departements = get_all_departements()
    return render_template("reseau.html", departements=departements)

# AJAX : Liste des communes d’un département
@app.route("/communes/<code_dept>")
def communes(code_dept):
    communes = get_communes_by_dept(code_dept)
    return jsonify(communes)

# AJAX : Liste des réseaux d’une commune
@app.route("/reseaux/<code_commune>")
def reseaux(code_commune):
    reseaux = get_reseaux_by_commune(code_commune)
    return jsonify(reseaux)

# AJAX : Infos d’un réseau
@app.route("/infos/<code_reseau>")
def infos_reseau(code_reseau):
    infos = get_infos_reseau(code_reseau)
    return jsonify(infos)

# Lancer le serveur
if __name__ == "__main__":
    app.run(debug=True)
