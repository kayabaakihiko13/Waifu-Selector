import streamlit as st
import os
import sys
sys.path.append("../Selector")
from Selector.kuntils import *
model = "../dashbroad/data/saved_model.pkl"
class_label = "../dashbroad/data/class_dictionary.json"
# Buat folder penyimpanan gambar
if not os.path.exists("uploaded_images"):
    os.mkdir("uploaded_images")

st.title("Dashbroad Image Classification Waifu")

# Tampilkan widget untuk mengunggah gambar
uploaded_image = st.file_uploader("Unggah Gambar", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    # Simpan gambar yang diunggah
    image_path = os.path.join("uploaded_images", uploaded_image.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_image.read())
    st.success(f"Gambar berhasil diunggah dan disimpan di {image_path}")

    # Tampilkan gambar yang telah diunggah
    st.image(image_path, caption="Gambar yang diunggah", use_column_width=True)

    # Tampilkan path file
    if st.button("Proses Gambar"):
        image_arr = image_to_array(image_path)
        result = result_waifu_generate(image_arr, model, class_label)[0]
        st.write(f"Hasil pemrosesan gambar: {result}")

    