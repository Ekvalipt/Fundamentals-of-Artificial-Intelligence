import streamlit as st
from PIL import Image 
import utils

st.set_page_config("Hopfield")
st.title("Мережа Хопфілда")

st.subheader("1. Запам'ятовування еталонів")
umpload_photo = utils.hop_umplodet_photo()

if umpload_photo is not None:
    vectors = []
    norm_vectors = []
    binar_vectors = []
    
    for img in umpload_photo:
        img_opened = Image.open(img).convert("L")
        v_temp, n_v_temp = utils.create_vector_and_nor_vector(img_opened)
        bi_temp = utils.binarization(n_v_temp)
        
        vectors.append(v_temp)
        norm_vectors.append(n_v_temp)
        binar_vectors.append(bi_temp)
        

    st.session_state.W = utils.mateix_w(binar_vectors)
    st.session_state.binar_vectors = binar_vectors
        
    with st.expander("Детальна інформація"):
        for idx, bv in enumerate(binar_vectors):
            st.write(f"Еталон Класу {idx+1}:", bv)
        st.write("Побудова матриці ваг W:")
        st.dataframe(st.session_state.W)

    st.divider()


    st.subheader("2. Розпізнавання невідомого фото")
    unknown_photo = st.file_uploader(
        label="Завантажте 1 фото для перевірки",
        type=['png', "jpeg", "jpg"]
    )

    if unknown_photo is not None:
        img_unk = Image.open(unknown_photo).convert("L")
        v_unk, n_v_unk = utils.create_vector_and_nor_vector(img_unk)
        bi_unk = utils.binarization(n_v_unk)
        
        st.write("Вхідний бінарний вектор:", *bi_unk)
        
        recovered_vector = utils.predict_hopfield(bi_unk, st.session_state.W)
        st.write("Відновлений вектор:", *recovered_vector)
        
        recognized_class = None
        for idx, etalon in enumerate(st.session_state.binar_vectors):
            if recovered_vector == etalon:
                recognized_class = idx + 1
                break
                
        if recognized_class:
            st.success(f"Мережа розпізнала Клас {recognized_class}!")
        else:
            st.error("Мережа не змогла розпізнати образ")
