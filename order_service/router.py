import json
from fastapi import APIRouter, Depends, HTTPException, Request
import requests
import pika
from datetime import datetime
from order_service.dependencies import get_current_user
from order_service.dao import OrderDAO
from order_service.schemas import SOrder
from order_service.config import settings


router = APIRouter(prefix="/orders", tags=['Заказы'])

@router.post('/')
async def create_order(order: SOrder, request: Request):
    """
    Создание нового заказа
    """
    access_token = request.cookies.get("flower_access_token")
    headers = {'accept': 'application/json', 'token': access_token}
    response = requests.get('http://127.0.0.1:8000/auth/me', headers=headers, timeout=10)
    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Not authorized")
    user_id = response.json()['id']

    total_price = 0
    for item in order.cart:
        cart_response = requests.get(f'http://127.0.0.1:8002/cart/{item.id}',
                                     headers=headers, timeout=10)
        cart_data = cart_response.json()
        print(cart_data)
        flower_response = requests.get(f'http://127.0.0.1:8001/flowers/{cart_data['bouquet_id']}',
                                       headers=headers, timeout=10)
        flower_data = flower_response.json()
        item_price = flower_data['price'] * cart_data['quantity']
        total_price += item_price

    order_id = await OrderDAO.add(user_id=user_id,
                       order_date=datetime.now(),
                       total_cost=total_price,
                       order_status="Создан",
                       payment_method="Наличные",
                       shipping_method=order.shipping_method,
                       is_delivered=False,
                       address=order.address)
    # Подключаемся к брокеру
    connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST))
    channel = connection.channel()
    # Подготовка сообщения для RabbitMQ
    message = {
        "status": "created",
        "order_id": order_id,
        "total_cost": total_price,
        "email": response.json()['email']
    }
    # Отправляем сообщение в RabbitMQ
    channel.basic_publish(exchange='', routing_key=settings.QUEUE_NAME, body=json.dumps(message))
    connection.close()

    return {"message": "Заказ успешно создан"}

@router.get('/')
async def get_orders(current_user = Depends(get_current_user)):
    """
    Получение списка всех заказов
    """
    return await OrderDAO.find_all(user_id=current_user['id'])


@router.get('/{order_id}')
async def get_order(order_id: int, current_user = Depends(get_current_user)):
    """
    Получение заказa по его ID.
    """
    order = await OrderDAO.find_one_or_none(id=order_id, user_id=current_user['id'])
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@router.put('/{order_id}')
async def update_order(order_id: int, new_status: str, current_user = Depends(get_current_user)):
    """
    Обновление статуса заказа
    """
    if current_user['role'] != "admin":
        raise HTTPException(status_code=403, detail="Недостаточно прав для изменения заказа")
    order = await OrderDAO.find_one_or_none(id=order_id, user_id=current_user['id'])
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    await OrderDAO.update(order_id=order_id, user_id=current_user['id'], order_status=new_status, is_delivered=True)
    # Подключаемся к брокеру
    connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST))
    channel = connection.channel()
    # Подготовка сообщения для RabbitMQ
    message = {
        "status": "done",
        "order_id": order_id,
        "total_cost": order.total_cost,
        "email": current_user['email']
    }
    # Отправляем сообщение в RabbitMQ
    channel.basic_publish(exchange='', routing_key=settings.DONE_QUEUE_NAME, body=json.dumps(message))
    connection.close()

    return {"message": "Заказ успешно изменен"}
