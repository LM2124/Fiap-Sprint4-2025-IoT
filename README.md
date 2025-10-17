# 🧠 Reconhecimento Facial com Flask e Dlib

Este projeto é uma aplicação em **Python** que utiliza **Flask**, **OpenCV**, **Dlib** e **Pillow** para realizar **reconhecimento facial**.  
O sistema permite **registrar** e **validar** usuários com base em suas imagens faciais, associando cada rosto a um **perfil de investidor** (Conservador, Moderado ou Agressivo).

## 🚀 Funcionalidades

- Registro facial com nome e tipo de investidor  
- Validação facial para reconhecer usuários já cadastrados  
- Banco de dados local utilizando arquivo `db.pkl`  
- Processamento e reconhecimento facial com **Dlib**  
- API REST simples com **Flask**

## ▶️ Como Executar o Projeto

- **Clone o repositório**

  ```bash
  git clone https://github.com/LM2124/Fiap-Sprint4-2025-IoT.git
  ```

- **Instale as dependências**

  ```bash
  pip install -r requirements.txt
  ```

- **Execute o servidor Flask**

  ```bash
  python main.py
  ```

  **O servidor será iniciado em:** `http://127.0.0.1:5000`

- **Teste os endpoints (Opcional):**

  ```bash
  python test_endpoint.py
  ```

### Exemplo de Registro

```bash
curl -X POST http://127.0.0.1:5000/upload \
  -F "image=@foto1.jpg" \
  -F "action=register" \
  -F "nome=nome" \
  -F "tipo=Agressivo"
```

### Exemplo de Validação

```bash
curl -X POST http://127.0.0.1:5000/upload \
  -F "image=@foto2.jpg" \
  -F "action=validate"
```
