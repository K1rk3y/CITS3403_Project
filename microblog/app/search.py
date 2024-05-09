#Elastic Search (Does not work)
from flask import current_app

def add_order_to_index(order):
    if not current_app.elasticsearch:
        return
    payload = {
        'first_name': order.first_name,
        'last_name': order.last_name,
        'email': order.email,
        'meal': order.meal
    }
    try:
        current_app.elasticsearch.index(index='orders', id=order.id, body=payload)
    except Exception as e:
        current_app.logger.error("Failed to add order to Elasticsearch index: %s", e)


def remove_order_from_index(order):
    if not current_app.elasticsearch:
        return current_app.elasticsearch.delete(index='orders', id=order.id)

def search_orders(query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index='orders',
        query={'multi_match': {'query': query, 'fields': ['first_name', 'last_name', 'meal', 'email']}},
        from_=(page - 1) * per_page,
        size=per_page
    )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
