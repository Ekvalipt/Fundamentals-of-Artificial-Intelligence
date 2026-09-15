import streamlit as st
from PIL import Image, ImageDraw
import json
import os

# відображення фото


def show_photo(uploded_photo):

    try:
        st.image(uploded_photo)
        st.success("Photo Uploader")
    except:
        st.error("error")


def get_distance_mechi(vec1, vec2):
    x = lambda a: abs(a[0] - a[1])
    lst_two = zip(vec1, vec2)

    return sum(map(x, lst_two))


def get_efklid_distance(vec1, vec2):
    x = lambda a: (a[0] - a[1]) ** 2
    lst_two = zip(vec1, vec2)

    return sum(map(x, lst_two)) ** 0.5


def get_distance_chebish(vec1, vec2):
    x = lambda a: abs(a[0] - a[1])
    lst_two = zip(vec1, vec2)

    return max(map(x, lst_two))


def get_cluster_center(vectors):
    return [sum(col) / len(col) for col in zip(*vectors)]


def create_vector_and_nor_vector(img):
    vector = []

    w, h = img.size

    col = 4
    row = 5

    coll_w = w // col
    coll_h = h // row

    for r in range(row):
        for c in range(col):

            left = c * coll_w
            upper = r * coll_h
            rigth = left + coll_w
            lower = upper + coll_h

            cell = img.crop((left, upper, rigth, lower))

            pixel = list(cell.getdata())

            black_pixel_count = sum(1 for p in pixel if p < 128)

            vector.append(black_pixel_count)
    try:
        max_num = max(vector)
        norm_vector = [i / max_num for i in vector]
    except ZeroDivisionError:
        st.error("NO WHITE PHOTO!")
    return vector, norm_vector


# назва або заговолок хз

st.title("Streamlit Image Uploader")

# вибираємо метод відображення

uploader_metod = st.radio("Select", ("Study", "Recognition"))
uploded_photo = None

if uploader_metod == "Recognition":
    uploded_photo = st.file_uploader(
        "Select photo on pc", type=["jpg", "jpeg", "png", "webp"]
    )
# обробляіємо

if uploded_photo is not None:

    option = st.selectbox("Select way:", ("Evklid", "Chebish", "Manhnetska"))

    if option == "Evklid":
        fun_for_distance = get_efklid_distance
    elif option == "Chebish":
        fun_for_distance = get_distance_chebish
    elif option == "Manhnetska":
        fun_for_distance = get_distance_mechi
        
    img = Image.open(uploded_photo).convert("L")
    img_copy = img.copy().convert("RGB")
    draw = ImageDraw.Draw(img_copy)

    w, h = img.size

    col = 4
    row = 5

    coll_w = w // col
    coll_h = h // row

    for c in range(1, col):
        x = c * coll_w
        draw.line([(x, 0), (x, h)], fill="red", width=2)
    for r in range(1, row):
        y = r * coll_h
        draw.line([(0, y), (w, y)], fill="red", width=2)
    
    show_photo(img_copy)

    # main fun for vector and norm vector

    vector, norm_vector = create_vector_and_nor_vector(img)

    file_name = "model.json"
    with open(file_name, "r", encoding="utf-8") as f:
        etalons = json.load(f)
    d_num = {}

    for key in etalons:
        d_num[key] = fun_for_distance(etalons[key], norm_vector)
    
    min_distance = min(d_num, key=d_num.get)
    st.success(min_distance)

    with st.expander("Additional (information)"):
        st.write("Нормальний вектор:", *norm_vector)
        st.write("Абсолютний вектор:", *vector)
        st.write("Method: ", option, ", min distance: ", d_num[min_distance])

elif uploader_metod == "Study":
    num = st.selectbox("Select num", ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"))
    img_uploder = st.file_uploader(
        "Select photo on pc",
        accept_multiple_files=True,
        type=["jpg", "jpeg", "png", "webp"],
    )

    if img_uploder:
        if st.button(f"Save num {num}"):

            imgs = [Image.open(img).convert("L") for img in img_uploder]
            all_norm_vectors = []

            for img in imgs:

                vec, norm_vector = create_vector_and_nor_vector(img)
                all_norm_vectors.append(norm_vector)
            file_name = "model.json"
            if os.path.exists(file_name):
                with open(file_name, "r", encoding="utf-8") as f:
                    data = json.load(f)
            
            key_name = f"Цифра {num}"
            one_etalon_num = data[key_name]
            all_norm_vectors.append(one_etalon_num)
            centr_vector = get_cluster_center(all_norm_vectors)
            data[key_name] = centr_vector

            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            st.success("Now data upptade!")

            with st.expander("View file contents"):
                st.write(data)
