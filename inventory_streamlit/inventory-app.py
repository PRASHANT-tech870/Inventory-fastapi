import streamlit as st
import requests

INVENTORY_API = "http://127.0.0.1:8000"

st.title("Inventory Management Dashboard")

# List all products
if st.button("List Products"):
    response = requests.get(f"{INVENTORY_API}/products")
    if response.status_code == 200:
        products = response.json()
        st.write("**Available Products:**")
        for product in products:
            st.write(product)
    else:
        st.error("Failed to fetch products.")

# Fetch product details
product_id = st.text_input("Enter Product ID", "")
if st.button("Get Product Details") and product_id:
    response = requests.get(f"{INVENTORY_API}/products/{product_id}")
    if response.status_code == 200:
        product = response.json()
        st.write(product)
    else:
        st.error("Product not found.")

# Create a new product
with st.form("create_product_form"):
    st.write("Create New Product")
    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    submitted = st.form_submit_button("Create Product")

    if submitted:
        payload = {"name": name, "price": price, "quantity": quantity}
        response = requests.post(f"{INVENTORY_API}/products", json=payload)
        if response.status_code in [200, 201]:
            st.success("Product created successfully!")
        else:
            st.error(f"Failed to create product. Error: {response.text}")

# Delete a product
delete_product_id = st.text_input("Enter Product ID to Delete", "")
if st.button("Delete Product") and delete_product_id:
    response = requests.delete(f"{INVENTORY_API}/products/{delete_product_id}")
    if response.status_code == 200:
        st.success("Product deleted successfully!")
    else:
        st.error(f"Failed to delete product. Error: {response.text}")
