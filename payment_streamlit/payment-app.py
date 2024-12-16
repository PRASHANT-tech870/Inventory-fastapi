import streamlit as st
import requests

PAYMENT_API = "http://127.0.0.1:8001"

st.title("Order & Payment Management Dashboard")

# Create a new order
with st.form("create_order_form"):
    st.write("Create New Order")
    product_id = st.text_input("Product ID")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    submitted = st.form_submit_button("Create Order")

    if submitted:
        payload = {"id": product_id, "quantity": quantity}
        response = requests.post(f"{PAYMENT_API}/orders", json=payload)
        if response.status_code == 200:
            order = response.json()
            st.success(f"Order created! Order ID: {order['pk']}")
        else:
            st.error("Failed to create order.")

# Get order details
order_id = st.text_input("Enter Order ID", "")
if st.button("Get Order Details") and order_id:
    response = requests.get(f"{PAYMENT_API}/orders/{order_id}")
    if response.status_code == 200:
        order = response.json()
        st.write(order)
    else:
        st.error("Order not found.")

# List orders by status
status = st.selectbox("Select Order Status", ["pending", "completed", "refunded"])
if st.button("List Orders by Status"):
    response = requests.get(f"{PAYMENT_API}/orders?status={status}")
    if response.status_code == 200:
        orders = response.json()
        st.write(f"**Orders with status '{status}':**")
        for order in orders:
            st.write(order)
    else:
        st.error("Failed to fetch orders.")
