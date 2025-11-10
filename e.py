import streamlit as st
import os

# ---------- PAGE SETTINGS ----------
st.set_page_config(page_title="E-Commerce Store", page_icon="🛍️", layout="wide")

# ---------- HEADER ----------
st.title("🛍️ Welcome to FS Mart")
st.write("Your one-stop online store!")

st.divider()

# ---------- SESSION STATE SETUP ----------
# Used to store cart data between reruns
if "cart" not in st.session_state:
    st.session_state.cart = {}

# ---------- SIDEBAR ----------
st.sidebar.header("Filter Products")
category = st.sidebar.selectbox("Choose a category", ["All", "Electronics", "Fashion", "Home Decor"])
price_range = st.sidebar.slider("Select Price Range", 100, 5000, (500, 3000))
st.sidebar.write(f"Showing items between ₹{price_range[0]} - ₹{price_range[1]}")
st.sidebar.divider()
st.sidebar.write("Made with ❤️ ")

# ---------- PRODUCT DATA ----------
products = [
    {
        "name": "Wireless Headphones",
        "price": 1299,
        "image": "images/OIP.jpeg",
        "category": "Electronics",
        "description": "High-quality sound with noise cancellation and long battery life."
    },
    {
        "name": "Smart Watch",
        "price": 2499,
        "image": "images/watch.jpg",
        "category": "Electronics",
        "description": "Track your fitness and notifications with this stylish smartwatch."
    },
    {
        "name": "Home Decor Lamp",
        "price": 1799,
        "image": "images/lamp.jpg",
        "category": "Home Decor",
        "description": "Elegant table lamp to brighten up your living space."
    }
]

# ---------- DISPLAY PRODUCTS ----------
cols = st.columns(2)

for i, product in enumerate(products):
    if (category == "All" or product["category"] == category) and price_range[0] <= product["price"] <= price_range[1]:
        col = cols[i % 2]
        with col:
            st.subheader(product["name"])

            # Handle image safely
            image_path = os.path.join(os.getcwd(), product["image"])
            if os.path.exists(image_path):
                st.image(image_path, use_container_width=True)
            else:
                st.warning(f"Image not found for {product['name']}")

            st.write(product["description"])
            st.metric(label="Price", value=f"₹{product['price']}")

            # Add to cart button
            if st.button(f"🛒 Add to Cart", key=product["name"]):
                if product["name"] in st.session_state.cart:
                    st.session_state.cart[product["name"]]["quantity"] += 1
                else:
                    st.session_state.cart[product["name"]] = {
                        "price": product["price"],
                        "quantity": 1
                    }
                st.success(f"✅ Added {product['name']} to cart!")

st.divider()

# ---------- CART & BILLING AREA ----------
st.header("🧾 Your Cart & Billing")

if not st.session_state.cart:
    st.info("🛒 Your cart is empty. Add some products to see them here!")
else:
    total = 0
    for item, details in st.session_state.cart.items():
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.write(f"**{item}**")
        with col2:
            st.write(f"₹{details['price']}")
        with col3:
            st.write(f"Qty: {details['quantity']}")
        with col4:
            if st.button("❌ Remove", key=f"remove_{item}"):
                st.session_state.cart.pop(item)
                st.rerun()

        total += details['price'] * details['quantity']

    st.divider()
    st.subheader(f"💰 Total Amount: ₹{total}")

    # Checkout button
    if st.button("✅ Proceed to Checkout"):
        st.success("🎉 Order placed successfully! Thank you for shopping with us.")
        st.session_state.cart.clear()

st.divider()
st.write("© 2025 FS mart - All Rights Reserved")
