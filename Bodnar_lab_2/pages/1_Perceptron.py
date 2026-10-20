import streamlit as st
from PIL import Image
import utils

st.set_page_config("Perceptron")
st.title("Perceptron")


umpload_photo = utils.umplodet_photo()

if umpload_photo is not None:
    utils.draw_line(umpload_photo)

    vector, norm_vactor = utils.create_vector_and_nor_vector(Image.open(umpload_photo).convert("L"))



    # створення ключів сесії
    if "zsuv" not in st.session_state:
        zsuv_t, vagi_t = utils.initilizator(len(vector))
    
        st.session_state.zsuv = zsuv_t
        st.session_state.vagi = vagi_t
        
    
    p = utils.prohid(norm_vactor, st.session_state.vagi, st.session_state.zsuv)
 
 
    if p == 1:
        st.title("Мережа вважає, що це Клас 1")
        
    else:
        st.title("Мережа вважає, що це Клас 2")
    
    # кнопкни правильо чи ні
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Правильно", use_container_width=True):
            st.success("Результат підтверджено!")

    with col2:
        if st.button("Не правильно (Змінити клас)", use_container_width=True):
            target_d = -p
            st.session_state.vagi = utils.train_perceptron(
                st.session_state.vagi, 
                norm_vactor, 
                d=target_d, 
                y=p
            )
            st.rerun()  
        
        
    # Вивід інформаціїї
    with st.expander("Інформація"):
        st.write("Нормальний вектор:", *norm_vactor)
        st.write("Зсув:", st.session_state.zsuv)
        st.write("Список:", *st.session_state.vagi)
        st.write("Вектор:", *vector)
