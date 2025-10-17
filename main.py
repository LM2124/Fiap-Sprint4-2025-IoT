import cv2, dlib, numpy as np, pickle, os
from flask import Flask, request
from PIL import Image

DB_FILE = "db.pkl"
PREDICTOR = "shape_predictor_5_face_landmarks.dat"
RECOG = "dlib_face_recognition_resnet_model_v1.dat"
THRESH = 0.4

db = pickle.load(open(DB_FILE,"rb")) if os.path.exists(DB_FILE) else {}
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(PREDICTOR)
rec = dlib.face_recognition_model_v1(RECOG)

def get_face_vec_from_image(img: Image):
    frame = np.array(img)
    rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    rects = detector(rgb, 1)
    if len(rects) == 0:
        return False
    shape = sp(rgb, rects[0])
    chip = dlib.get_face_chip(rgb, shape)
    vec = np.array(rec.compute_face_descriptor(chip), dtype=np.float32)
    return vec

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "Imagem não encontrada", 400

    file = request.files['image']
    action = request.form.get('action') # 'register' ou 'validate'
    try:
        img = Image.open(file).convert('RGB')
        vec = get_face_vec_from_image(img)
        if vec is False:
            return "Nenhum rosto detectado.", 400

        if action == 'register':
            nome = request.form.get('nome', None)
            tipo = request.form.get('tipo', None)
            return registrar(vec, nome, tipo)
        elif action == 'validate':
            return validar(vec)
        else:
            return "Ação inválida", 400

    except Exception as e:
        return f"Erro ao processar a imagem: {str(e)}", 400


tiposInvestidor = {
    "Conservador": "Bem-vindo, investidor conservador! Focamos em investimentos de baixo risco para garantir sua segurança financeira.",
    "Moderado": "Bem-vindo, investidor moderado! Vamos buscar um equilíbrio entre risco e retorno para alcançar bons resultados.",
    "Agressivo": "Bem-vindo, investidor agressivo! Prepare-se para explorar oportunidades de alto risco com grandes potenciais de retorno!",
}

def registrar(vec, nome, tipo):
    if not nome or not tipo or tipo not in tiposInvestidor:
        return "Nome ou Tipo de investidor inválido.", 400
    db[nome] = [vec, tipo]
    pickle.dump(db, open(DB_FILE,"wb"))
    return f"Usuário cadastrado com sucesso: {nome} ({tipo})", 200

def validar(vec):
    nomeVal, bestDist = None, 999
    for nome, dbItem in db.items():
        vec, tipo = dbItem
        dist = np.linalg.norm(vec - vec)
        if dist < bestDist:
            nomeVal, tipo, bestDist = nome, tipo, dist

    if bestDist > THRESH or nomeVal is None:
        return "Usuário não reconhecido.", 400
    return f"Bem vindo, {nomeVal}! ({tiposInvestidor.get(tipo, tipo)})", 200

if __name__ == '__main__':
    app.run()
