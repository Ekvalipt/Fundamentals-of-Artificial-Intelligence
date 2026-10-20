import streamlit as st
from PIL import Image 
import utils

st.set_page_config("Hamming")
st.title("Мережа Хеммінга")

st.subheader("1. Завантаження 3 еталонів")
upload_photos = utils.hop_umplodet_photo()  

if upload_photos is not None:
    vectors = []
    norm_vectors = []
    binar_vectors = []
    
    for img in upload_photos:
        img_opened = Image.open(img).convert("L")
        v_temp, n_v_temp = utils.create_vector_and_nor_vector(img_opened)
        bi_temp = utils.binarization(n_v_temp)
        
        vectors.append(v_temp)
        norm_vectors.append(n_v_temp)
        binar_vectors.append(bi_temp)
        
        

    W1, B1 = utils.init_hamming_weights(binar_vectors)
    st.session_state.W1 = W1
    st.session_state.B1 = B1
    st.session_state.binar_vectors = binar_vectors
        
    with st.expander("Інформація"):
        for idx, bv in enumerate(binar_vectors):
            st.write(f"Еталон Класу {idx+1}:", bv)
        st.write("Матриця ваг першого шару W1 (3 x 20):")
        st.dataframe(st.session_state.W1)
        st.write("Вектор порогів B1:", st.session_state.B1)

    st.divider()


    st.subheader("2. Розпізнавання невідомого фото")
    unknown_photo = st.file_uploader(
        label="Завантажте 1 фото для розпізнавання",
        type=['png', "jpeg", "jpg"]
    )

    if unknown_photo is not None:
        img_unk = Image.open(unknown_photo).convert("L")
        v_unk, n_v_unk = utils.create_vector_and_nor_vector(img_unk)
        bi_unk = utils.binarization(n_v_unk)
        
        st.write("Вхідний бінарний вектор:", *bi_unk)
        
        winner, y1_vals, y2_vals = utils.predict_hamming(
            bi_unk, 
            st.session_state.W1, 
            st.session_state.B1
        )
        
        st.write("Початкова схожість:", *y1_vals)
        st.write("Виходи 2-го шару:", *y2_vals)
        
        st.success(f"Клас {winner}!")
