#!/bin/bash
# Déploiement Django production sur cbs-timer.cbs.site.univ-lorraine.fr
# Usage : ./deploy.sh

# Variables à adapter
PROJECT_DIR="$HOME/Documents/GitHub/exam_manager"
VENV_DIR="$PROJECT_DIR/.venv"
DJANGO_SETTINGS_MODULE="exam_manager.settings"
DOMAIN="cbs-timer.cbs.site.univ-lorraine.fr"
GUNICORN_PORT=8001
STATIC_ROOT="$PROJECT_DIR/staticfiles"
PYTHON="$VENV_DIR/bin/python3"
GUNICORN="$VENV_DIR/bin/gunicorn"

# 1. Activer l'environnement virtuel
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# 2. Installer les dépendances
pip install -r "$PROJECT_DIR/requirements.txt" || pip install django gunicorn pandas xlsxwriter

# 3. Configurer settings.py pour la prod
sed -i "s/^DEBUG = True/DEBUG = False/" "$PROJECT_DIR/exam_manager/settings.py"
sed -i "/^ALLOWED_HOSTS/c\ALLOWED_HOSTS = ['localhost', '$DOMAIN']" "$PROJECT_DIR/exam_manager/settings.py"
grep -q "STATIC_ROOT" "$PROJECT_DIR/exam_manager/settings.py" || echo "STATIC_ROOT = BASE_DIR / 'staticfiles'" >> "$PROJECT_DIR/exam_manager/settings.py"

# 4. Collecte des fichiers statiques
$PYTHON "$PROJECT_DIR/manage.py" collectstatic --noinput

# 5. Migration de la base
$PYTHON "$PROJECT_DIR/manage.py" migrate

# 6. Créer le service systemd pour gunicorn
SERVICE_FILE="$HOME/gunicorn_exam_manager.service"
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=gunicorn daemon for exam_manager
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=$GUNICORN exam_manager.wsgi:application --bind 127.0.0.1:$GUNICORN_PORT --workers 3
Environment="DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE"

[Install]
WantedBy=multi-user.target
EOF

sudo mv "$SERVICE_FILE" /etc/systemd/system/gunicorn_exam_manager.service
sudo systemctl daemon-reload
sudo systemctl enable gunicorn_exam_manager
sudo systemctl restart gunicorn_exam_manager

# 7. Afficher la config nginx à ajouter
cat <<EONGINX

# À ajouter dans /etc/nginx/sites-available/exam_manager
server {
    listen 80;
    server_name $DOMAIN;

    location /static/ {
        alias $STATIC_ROOT/;
    }

    location / {
        proxy_pass http://127.0.0.1:$GUNICORN_PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Puis :
# sudo ln -s /etc/nginx/sites-available/exam_manager /etc/nginx/sites-enabled/
# sudo nginx -t && sudo systemctl reload nginx
EONGINX

echo "Déploiement terminé. Pensez à configurer Nginx et à sécuriser votre SECRET_KEY."
