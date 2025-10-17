import os.path
import requests

endpoint_url = "http://127.0.0.1:5000/upload"

def validate(image_path):
    with open(image_path, 'rb') as f:
        form = {'action': 'validate'}
        files = {'image': (image_path, f, 'image/jpeg')}

        response = requests.post(endpoint_url, data=form, files=files)
        print(f"[{response.status_code}] {response.text}")

def register(image_path, name, type):
    with open(image_path, 'rb') as f:
        form = {
            'action': 'register',
            'nome': name,
            'tipo': type,
        }
        files = {'image': (image_path, f, 'image/jpeg')}

        response = requests.post(endpoint_url, data=form, files=files)
        print(f"[{response.status_code}] {response.text}")

def main():
    while (action := input("Escolha a ação: (V)alidar / (R)egistrar\n").upper()) not in ["V", "R"]:
        print("Ação inválida. Tente Novamente.")

    while not os.path.isfile(image_path := input("Digite o caminho da imagem:\n").strip()):
        print("Arquivo não encontrado. Tente Novamente.")

    if action == "V":
        validate(image_path)
    elif action == "R":
        while not len(nome := input("Digite o nome do usuário:\n")) > 0:
            print("Nome não pode estar vazio. Tente Novamente.")

        tipos = {"C":"Conservador", "M": "Moderado", "A":"Agressivo"}
        while not (letra := input("Digite o tipo de investidor do usuário: (C)onservador / (M)oderado / (A)gressivo\n").upper()) in tipos:
            print("Tipo inválido. Tente Novamente.")
        
        register(image_path, nome, tipos[letra])       

if __name__ == "__main__":
    main()
