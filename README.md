
# 🦷 LesionAI

**LesionAI** est une application Streamlit utilisant l'IA pour détecter des lésions orales à partir d'images, avec génération automatique de rapports PDF.

---

## 🚀 Lancer l'application

### 1. Cloner le projet
```bash
git clone https://github.com/LesionAI/LesionAI/
cd LesionAI
```

### 2. Créer un environnement virtuel (optionnel mais recommandé)
```bash
python3 -m venv lesionai-venv
source lesionai-venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer le fichier `.env`
Crée un fichier `.env` à la racine avec :

```env
ROBOFLOW_API_KEY=ton_api_key_roboflow
```

(Obtiens la clé sur [https://roboflow.com](https://roboflow.com) dans ton espace projet)

---

## 🔐 Utilisateurs

Les identifiants sont définis dans `config.yaml`. Tu peux générer de nouveaux mots de passe avec :

```bash
python gen_password.py
```

Et ajouter les utilisateurs dans le fichier YAML.

---

## 🧠 Lancer l'application

Utilise le fichier de lancement principal :

```bash
streamlit run LesionAI_run.py
```

Cela te redirigera vers l'interface de login, puis chargera automatiquement l'application `app.py`.

---

## 📂 Structure

- `app.py` : logique principale de l'application
- `LesionAI_run.py` : point d'entrée avec authentification
- `config.yaml` : configuration utilisateurs
- `dossiers_patients/` : dossiers enregistrés par utilisateur
- `.env` : contient ta clé API

---

## 🧼 Auteurs

- Victor DELBOS
