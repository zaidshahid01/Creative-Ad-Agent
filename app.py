import streamlit as st
from image_store import ImageStore

st.set_page_config(page_title="Creative Ad Agent", page_icon="🎨", layout="centered")

# Initialize the image store in session state (persists across reruns, dies with session)
if "image_store" not in st.session_state:
    st.session_state.image_store = ImageStore()

store: ImageStore = st.session_state.image_store

st.title("Product Images")
st.caption("Upload product images to get started")

# --- Upload ---
uploaded_files = st.file_uploader(
    "Drag & drop images here, or click to browse",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True,
)

if uploaded_files:
    for file in uploaded_files:
        # Skip duplicates (same name already in store)
        if file.name in store:
            st.warning(f"⚠️ `{file.name}` is already in the store — skipping duplicate.")
            continue
        data = file.read()
        store.add(name=file.name, data=data, content_type=file.type)
    st.success(f"✅ {len(uploaded_files)} image(s) uploaded successfully!")

# --- Stats bar ---
if not store.is_empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Images", len(store))
    col2.metric("Total Size", f"{store.total_size / 1024:.1f} KB")
    col3.metric("Status", "In Memory 🧠")

# --- Preview grid ---
if not store.is_empty:
    st.divider()
    st.subheader("Stored Images")

    cols = st.columns(3)
    for i, img in enumerate(store.list_all()):
        with cols[i % 3]:
            st.image(img.data, caption=img.name, use_container_width=True)
            if st.button(f"Remove", key=f"remove_{img.name}", use_container_width=True):
                store.remove(img.name)
                st.rerun()

    # Clear all button
    st.divider()
    if st.button("🗑️ Clear All Images", type="secondary", use_container_width=True):
        store.clear()
        st.rerun()
else:
    st.info("No images stored yet — upload some above!")
