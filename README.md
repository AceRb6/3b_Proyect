# Sistema de Inventario - Django + PostgreSQL

Sistema de gestión de inventario con base de datos normalizada.

## Quick Start

### Prerrequisitos
- Docker Desktop
- Git

### 1. Clonar repositorio
```bash
git clone <url>
cd contenedores_docker
```

### 2. Iniciar contenedores
```bash
docker-compose up -d --build
```
### 3. Crear superusuario
```
docker-compose exec backend python manage.py createsuperuser
```
### 4. Acceder
```
API: http://localhost:8000/api/
Admin: http://localhost:8000/admin/
```

### 5. Estructura del Proyecto
```
contenedores_docker/
├── docker-compose.yml      # Configuración de servicios
├── docker/
│   └── init.sql           # Esquema de base de datos
├── backend/
│   ├── Dockerfile         # Imagen de Django
│   ├── requirements.txt   # Dependencias Python
│   ├── manage.py
│   ├── inventario_project/  # Configuración Django
│   └── api/               # App con modelos y API
└── README.md
```


### 6. Comandos Útiles
# Ver logs
```
docker-compose logs -f backend
```
# Entrar al contenedor
```
docker-compose exec backend bash
```
# Migraciones
```
docker-compose exec backend python manage.py migrate
```
# Cargar datos (si tienen CSV)
```
docker-compose exec backend python manage.py load_inventory /app/data.csv
```
# Detener todo
```
docker-compose down
```
# Eliminar volúmenes (borra datos)
```
docker-compose down -v
```
### 7. Configuración
Variables en docker-compose.yml:

DB: PostgreSQL 15

Usuario: admin/admin123

Puerto API: 8000

Puerto DB: 5432

### 8. Colaboración
Crear rama: git checkout -b feature/nueva-funcionalidad

Commit: git commit -m "Descripción clara"

Push: git push origin feature/nueva-funcionalidad

Pull Request en GitHub/GitLab

