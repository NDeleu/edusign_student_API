```markdown
# Guide d'installation et de configuration du projet

Ce guide vous expliquera comment installer Python, configurer un environnement virtuel et exécuter un projet Python Django à partir d'un référentiel GitHub. Assurez-vous de suivre ces étapes pour mettre en place votre environnement de développement.

## Étapes de base

### 1. Installer Python

Si vous n'avez pas encore Python installé, suivez ces étapes pour l'installer :

- Téléchargez la dernière version de Python depuis le [site officiel de Python](https://www.python.org/downloads/).
- Pendant l'installation, assurez-vous de cocher la case "Ajouter Python x.x au PATH" (x.x représente la version que vous installez). Cela permettra d'accéder à Python depuis n'importe quel endroit dans l'invite de commande.

### 2. Installer Visual Studio Code (VS Code)

Si vous n'avez pas encore VS Code installé, téléchargez et installez-le à partir du [site officiel de Visual Studio Code](https://code.visualstudio.com/).

### 3. Fork et clone du projet GitHub

- Fork le projet GitHub en cliquant sur le bouton "Fork" en haut à droite de la page du référentiel GitHub.
- Clonez votre fork sur votre machine en utilisant la commande `git clone` :

```bash
git clone https://github.com/votre-nom-utilisateur/nom-du-projet.git
```

### 4. Configuration de l'environnement virtuel

Accédez à l'intérieur du repo et ouvrez une ligne de commande depuis ce projet (vous pouvez aussi ouvrir une ligne de commande dans vscode depuis le projet cloné).

- Créez un environnement virtuel en utilisant la commande Python venv (ou venv si vous utilisez Python 3.3+):

```bash
python -m venv venv
```

- Activez l'environnement virtuel :

**Sur Windows (PowerShell) :**

```powershell
.\venv\Scripts\Activate
```

**Sur macOS et Linux (Bash) :**

```bash
source venv/bin/activate
```

### 5. Installation des dépendances

- Installez les dépendances du projet en utilisant pip et le fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

### 6. Exécution du projet Django

- Accédez au répertoire du projet Django :

```bash
cd edusign_student_API
```

- Appliquez les migrations Django :

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

- Lancez le serveur de développement Django :

```bash
python manage.py runserver
```

Le serveur de développement devrait maintenant être en cours d'exécution à l'adresse `http://127.0.0.1:8000/`. Vous pouvez accéder à votre projet en ouvrant un navigateur web et en visitant cette adresse.

C'est tout ! Vous avez maintenant configuré et exécuté votre projet Python Django localement.
```