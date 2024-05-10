from app import create_app, db
from app.models import Order
from app.search import add_order_to_index

app = create_app()

''' #does not work since elastic not working
def reindex_all_orders():
    """Function to reindex all orders into Elasticsearch."""
    with app.app_context():
        orders = Order.query.all()
        for order in orders:
            add_order_to_index(order)
        print(f"Indexed {len(orders)} orders into Elasticsearch.")
'''
if __name__ == '__main__':
    # Will uncomment to run reindexing manually
    # reindex_all_orders()
    
    app.run(debug=True)
