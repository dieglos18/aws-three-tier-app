# Three-Tier Serverless Web Application on AWS

Aplicación web serverless de tres capas construida con servicios de AWS.

## 🏗️ Arquitectura

### Capa de Presentación
- **Amazon S3**: Almacenamiento de archivos estáticos
- **CloudFront**: CDN para distribución global

### Capa de Lógica
- **AWS Lambda**: Funciones serverless
- **API Gateway**: REST API

### Capa de Datos
- **DynamoDB**: Base de datos NoSQL

## 📋 Prerrequisitos

- Cuenta de AWS activa
- AWS CLI instalado y configurado
- Node.js (opcional, para desarrollo local)

## 🚀 Despliegue

### 1. Configurar DynamoDB
```bash
aws dynamodb create-table \
    --cli-input-json file://infrastructure/dynamodb-setup.json

# Insertar datos de ejemplo
aws dynamodb put-item \
    --table-name UsersTable \
    --item '{"userId": {"S": "1"}, "name": {"S": "Diego Losada"}, "email": {"S": "diego@example.com"}}'
```

### 2. Crear Función Lambda

1. Ve a AWS Lambda Console
2. Crea una nueva función con Python 3.x
3. Copia el código de `backend/lambda_function.py`
4. Añade permisos de DynamoDB a la función

### 3. Configurar API Gateway

1. Crea un REST API en API Gateway
2. Crea un recurso `/users`
3. Añade método GET vinculado a tu Lambda
4. Habilita CORS
5. Despliega a stage "prod"

### 4. Configurar S3 y CloudFront

1. Crea un bucket S3 (sin acceso público)
2. Sube archivos de `frontend/`
3. Crea distribución CloudFront apuntando al bucket
4. Actualiza `script.js` con tu URL de API Gateway

### 5. Actualizar Frontend

Reemplaza en `frontend/script.js`:
```javascript
const API_URL = 'https://tu-api-id.execute-api.region.amazonaws.com/prod/users';
```

## 🧪 Pruebas

Visita tu URL de CloudFront y verifica que los datos del usuario se cargan correctamente.

## 🔧 Solución de Problemas

### Error 403
- Verifica que CloudFront esté actualizado
- Limpia la caché del navegador

### Error CORS
- Confirma headers en Lambda
- Verifica configuración CORS en API Gateway

## 📝 Licencia

MIT License

## 👤 Autor

Diego Losada - NextWork Student