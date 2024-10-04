from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_connection
import generic_helper

app = FastAPI()

inprogress_orders = {}

@app.post("/")
async def handle_request(request: Request):
    # Parse the request from Dialogflow
    payload = await request.json()

    # Extract necessary fields
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])

    # Check for specific intent and respond accordingly
    intent_handling_dic = {
        'complete.order context:ongoing-order': complete_order,
        'add.order context: ongoing-order': add_to_order,
        'remove.order context: ongoing-order': remove_from_order,
        'track.order context: ongoing-order': track_order
    }

    return intent_handling_dic[intent](parameters, session_id)





def add_to_order(parameters: dict, session_id: str):
    food_items = parameters['food-item']
    quantities = parameters['number']

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry, I did not understand the order, please specify the food item along with the quantity clearly."
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        order_str = generic_helper.get_str_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far, you have {order_str}, Do you want to add anything else?"

        print(inprogress_orders)

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        })
    
    food_items = parameters["food-item"]
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f'Removed {",".join(removed_items)} from your order!'

    if len(no_such_items) > 0:
        fulfillment_text = f' Your current order does not have {",".join(no_such_items)}'

    if len(current_order.keys()) == 0:
        fulfillment_text += " Your order is empty!. Order something from the menu"
    else:
        order_str = generic_helper.get_str_food_dict(current_order)
        fulfillment_text +=  f" Here is what is left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)
        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to a backend error. " \
                               "Please place a new order again"
        else:
            order_total = db_connection.get_total_order_price(order_id)

            fulfillment_text = f"Awesome. We have placed your order. " \
                           f"Here is your order id # {order_id}. " \
                           f"Your order total is {order_total} which you can pay at the time of delivery!"

        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def save_to_db(order: dict):

    next_order_id = db_connection.get_next_order_id()

    for food_item, quantity in order.items():
        rcode = db_connection.insert_order(
            food_item,
            quantity,
            next_order_id
        )
    
        if rcode == -1:
            return -1
        
    db_connection.insert_order_tracking(next_order_id, "in progress")
    
    return next_order_id


def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['number'])
    order_status = db_connection.get_order_status(order_id=order_id)

    if order_status:
        fulfillment_text = f"The status of the order id: {order_id} is: {order_status}."
    else:
        fulfillment_text = f"No order found with the order id: {order_id}."

    # Respond with fulfillment text
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })