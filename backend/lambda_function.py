import json
import boto3
from boto3.dynamodb.conditions import Key

# Inicializar cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UsersTable')  # Reemplaza con el nombre de tu tabla

def lambda_handler(event, context):
    # Headers CORS
    headers = {
        'Access-Control-Allow-Origin': '*',  # O tu dominio de CloudFront
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Manejar preflight OPTIONS request
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'CORS preflight'})
        }
    
    try:
        # Obtener userId de los query parameters
        user_id = event.get('queryStringParameters', {}).get('userId')
        
        if not user_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'userId is required'})
            }
        
        # Consultar DynamoDB
        response = table.get_item(Key={'userId': user_id})
        
        if 'Item' in response:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'User not found'})
            }
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Internal server error'})
        }