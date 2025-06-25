from flask import Flask, render_template, request
import pickle
from skfuzzy import control as ctrl


with open("fuzzy_model.pkl", "rb") as f:
    sistema_ctrl = pickle.load(f)

app = Flask(__name__)

def clasificar_cafe(ph_val, cafeina_val, humedad_val, aroma_val):
    sim = ctrl.ControlSystemSimulation(sistema_ctrl)
    sim.input["pH"]       = ph_val
    sim.input["Cafeina"]  = cafeina_val
    sim.input["Humedad"]  = humedad_val
    sim.input["Aroma"]    = aroma_val
    sim.compute()

    salida = sim.output["Calidad"]

    if salida < 3.5:
        return "Baja"
    elif salida < 6.5:
        return "Media"
    else:
        return "Alta"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/clasificar", methods=["POST"])
def clasificar():
    ph       = float(request.form["ph"])
    cafeina  = float(request.form["cafeina"])
    humedad  = float(request.form["humedad"])
    aroma    = float(request.form["aroma"])

    resultado = clasificar_cafe(ph, cafeina, humedad, aroma)
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)