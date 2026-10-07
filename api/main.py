import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class VerifyRequest(BaseModel):
    code: str

# 1. Pagina Web per attivazione dispositivo (QR Code)
@app.get("/", response_class=HTMLResponse)
def get_web_setup():
    return """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Attivazione Dispositivo - Cedacri</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background-color: #f4f6f9; margin: 0; }
            .card { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); text-align: center; max-width: 400px; }
            h1 { color: #1a237e; margin-top: 0; font-style: italic; font-weight: 900;}
            h2 { color: #333; font-size: 18px; }
            #qrcode { margin: 30px auto; display: flex; justify-content: center; padding: 15px; background: white; border: 2px solid #eee; border-radius: 8px;}
            .footer-text { color: #666; font-size: 14px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>CEDACRI</h1>
            <h2>Attivazione Dispositivo Mobile</h2>
            <p class="footer-text">1. Apri Authenticator sul tuo smartphone.<br>2. Seleziona "Aggiungi account" e inquadra il QR code.</p>
            <div id="qrcode"></div>
            <p class="footer-text">3. Apri l'App Cedacri e inserisci il codice a 6 cifre.</p>
        </div>
        <script>
            fetch('/api/auth/setup')
                .then(response => response.json())
                .then(data => {
                    new QRCode(document.getElementById("qrcode"), {
                        text: data.qr_uri,
                        width: 200, height: 200,
                        colorDark : "#1a237e", colorLight : "#ffffff",
                        correctLevel : QRCode.CorrectLevel.H
                    });
                });
        </script>
    </body>
    </html>
    """

# 2. Generazione QR (Simulata per la demo)
@app.get("/api/auth/setup")
def setup_auth():
    return {
        "qr_uri": "otpauth://totp/AppAziendale:Demo_Capo?secret=SO7UDQM2ZA6CEJ6DHFUDGYW4RJP6CLAB&issuer=AppAziendale",
        "secret": "SO7UDQM2ZA6CEJ6DHFUDGYW4RJP6CLAB"
    }

# 3. Verifica OTP
@app.post("/api/auth/verify")
def verify_auth(req: VerifyRequest):
    if len(req.code) == 6:
        return {"token": "jwt-token-simulato-123"}
    raise HTTPException(status_code=400, detail="Codice errato")

# 4. Dati Dashboard (Grafici a doppia linea)
@app.get("/api/dashboard")
def get_dashboard_data(token: str = "", banca: str = "tutte"):
    multiplier = 1.0 if banca == "tutte" else random.uniform(0.1, 0.4)
    
    def generate_double_series(base, variance):
        blue = [int(random.uniform(base - variance, base + variance) * multiplier) for _ in range(12)]
        red = [int(b * random.uniform(0.9, 1.1)) for b in blue]
        return {"blue": blue, "red": red}

    return {
        "incidenti_del_giorno": random.randint(0, 3) if banca == "tutte" else random.randint(0, 1),
        "ticket_aperti": int(random.randint(1200, 1500) * multiplier),
        "charts": {
            "dbx_corporate_login": generate_double_series(5000, 2000),
            "dbx_bonifici": generate_double_series(400, 200),
            "next_gen_login": generate_double_series(8000, 3000),
            "atm_versamenti": generate_double_series(300, 150),
            "sportello_casse": generate_double_series(10000, 2000),
            "firma_elettronica": generate_double_series(20000, 10000),
        }
    }

# 5. Dati Bacheca Servizi (Drill-down)
@app.get("/api/bacheca")
def get_bacheca(token: str = ""):
    tipologie = ["Informativa", "Anomalia", "Informativa R."]
    services = ["OPM Nuove Gestioni Patrimoniali", "Servizi telematici", "Bonifici Europei", "Antiriciclaggio", "Multifondo", "-"]
    stati = ["Chiuso", "Aperto", "In Lavorazione"]
    
    data = []
    for i in range(25):
        data.append({
            "incident": f"INC00000{random.randint(100000, 999999)}",
            "tipo": random.choice(tipologie),
            "service": random.choice(services),
            "service_business": "Full Outsourcing",
            "urgency": random.choice(["Alta", "Media", "Bassa", "-"]),
            "stato": random.choice(stati),
            "customers": random.randint(1, 65)
        })
    return data

@app.on_event("startup")
def show_routes():
    print("--- ROTTE DISPONIBILI NEL BACKEND ---")
    for route in app.routes:
        methods = getattr(route, "methods", None)
        print(f"Path: {route.path} | Methods: {methods}")
    print("-------------------------------------")