import streamlit as st
import pandas as pd
import requests

# --- Function Definitions ---
def display_image(view):
    """
    Display a placeholder image for the selected view.
    """
    image_url = f"https://picsum.photos/390/975?random={view}"
    try:
        response = requests.get(image_url, timeout=5)
        if response.status_code == 200:
            st.image(image_url, caption=f"Screenshot for Subcluster {view}", use_container_width=True)
        else:
            st.image("https://via.placeholder.com/390x975?text=No+Image", caption="No Image Available", use_container_width=True)
    except Exception:
        st.image("https://via.placeholder.com/390x975?text=No+Image", caption="No Image Available", use_container_width=True)

# --- Page Configuration ---
st.set_page_config(page_title="Data Analysis Interface", layout="wide")

# --- Session State Initialization ---
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "Product One 1.1"

if "css_selectors" not in st.session_state:
    st.session_state["css_selectors"] = {}

if "extract_methods" not in st.session_state:
    st.session_state["extract_methods"] = {}

# --- Data Setup ---
parameters = [
    {"name": "Name", "key": "name"},
    {"name": "Price", "key": "price"},
    {"name": "SKU", "key": "sku"},
    {"name": "Currency", "key": "currency"},
    {"name": "Product URL", "key": "product_url"},
    {"name": "Availability", "key": "availability"},
    {"name": "Image URL", "key": "image_url"},
    {"name": "Image Gallery", "key": "image_gallery"},
    {"name": "Description", "key": "description"},
    {"name": "Category", "key": "category"},
    {"name": "Purchasable", "key": "purchasable"},
]

expected_values = {
    "name": "Product XYZ",
    "price": "29.99",
    "sku": "SKU123456",
    "currency": "USD",
    "product_url": "https://example.com/product-xyz",
    "availability": "In Stock",
    "image_url": "https://example.com/images/product-xyz.jpg",
    "image_gallery": "https://example.com/images/gallery1.jpg, https://example.com/images/gallery2.jpg",
    "description": "A fantastic product with amazing features",
    "category": "Electronics",
    "purchasable": "true",
}

actual_values = {
    "name": "Product XYZ",
    "price": "29.99",
    "sku": "SKU123456",
    "currency": "USD",
    "product_url": "https://example.com/xyz",
    "availability": "Available",
    "image_url": "https://example.com/images/xyz.jpg",
    "image_gallery": "https://example.com/images/gallery1.jpg, https://example.com/images/gallery2.jpg",
    "description": "A fantastic product with amazing features",
    "category": "Electronics",
    "purchasable": "true",
}

# Initialize default CSS selectors and extract methods if not present
for param in parameters:
    if param["key"] not in st.session_state["css_selectors"]:
        st.session_state["css_selectors"][param["key"]] = ""
    if param["key"] not in st.session_state["extract_methods"]:
        st.session_state["extract_methods"][param["key"]] = ""

# --- Cluster and Subcluster Buttons ---
st.write("### Select a Subcluster")
clusters = {
    "Cluster 1": ["Product One 1.1", "Product One 1.2", "Product One 1.3", "Product One 1.4"],
    "Cluster 2": ["Product One 2.1", "Product One 2.2", "Product One 2.3", "Product One 2.4"],
    "Cluster 3": ["Product One 3.1", "Product One 3.2", "Product One 3.3", "Product One 3.4"],
}

# Display subclusters as buttons
cols = st.columns(4)
for cluster, subclusters in clusters.items():
    for idx, subcluster in enumerate(subclusters):
        if cols[idx % 4].button(subcluster):
            st.session_state["current_view"] = subcluster

st.write("---")

# --- Layout: Screenshot and Comparison Table ---
col1, col2 = st.columns([1.5, 2])

# Left Column: Display Image
with col1:
    st.write("### Screenshot")
    display_image(st.session_state["current_view"])

# Right Column: Comparison Table with CSS Selectors and Extract Methods
with col2:
    st.write("### Data & Selectors")

    for param in parameters:
        key = param["key"]

        # Row for Parameter, Expected, and Actual Values
        row_cols = st.columns([1, 2, 2])
        with row_cols[0]:
            st.markdown(f"<h5>{param['name']}</h5>", unsafe_allow_html=True)
        with row_cols[1]:
            st.write(f"**Expected:** {expected_values.get(key, 'N/A')}")
        with row_cols[2]:
            st.write(f"**Actual:** {actual_values.get(key, 'N/A')}")

        # Input fields for CSS Selector and Extract Method
        input_cols = st.columns([2, 1])  # Split the input fields into two
        with input_cols[0]:
            st.text_input(
                "",
                key=f"css_selector_{key}"
            )
        with input_cols[1]:
            st.text_input(
                "",
                key=f"extract_method_{key}"
            )
