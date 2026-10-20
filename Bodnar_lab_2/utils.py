import streamlit as st
from PIL import Image, ImageDraw
import random

# навігація
def navigation():
    perceptron = st.Page("pages/1_Perceptron.py", title="Perceptron", )
    hopfield = st.Page("pages/2_Hopfield.py", title="Hopfield", )
    hamming = st.Page("pages/3_Hamming.py", title="Hamming", )

    pg = st.navigation({
        "main":[perceptron, hopfield, hamming]
    })

    pg.run()
  
# завантаження фото
def umplodet_photo():
    
    uploded_foto = st.file_uploader(
        label="Вибірить фото",
        type=['png', "jpeg", "jpg"],
        )
    
    return uploded_foto
  
# відобрадення вото на сторінці
def show_photo(img):
    if img is not None:
        
        try:
            st.image(img)
            st.success("Фото завантажено")
        except:
            st.error("Помилка")
            
         
            
# малюємо лінії і ділемо фото на 20 прямокутників + відобраєамо фото
def draw_line(umploded_photo):
    img = Image.open(umploded_photo).convert("RGB")
    draw = ImageDraw.Draw(img)
    
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
        
    show_photo(img)
    
    
# рахкємо вектор і нормальний ветор
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
        if max_num == 0: # Защита от абсолютно пустого листа
            return vector, [0.0] * len(vector)
        norm_vector = [i / max_num for i in vector]
    except ZeroDivisionError:
        st.error("NO WHITE PHOTO!")
        norm_vector = [0.0] * len(vector) # Страховка, чтобы код не упал
        
    return vector, norm_vector

#==================================
# !!! Тут логіка для Perceptron !!!
#==================================


# Створуємо зсув і 20 числ в списку 
fun_1 = lambda x: x[0] * x[1]

def initilizator(len_lst):
    zsuv = random.uniform(0, 1)
    vagi = [random.uniform(0, 1) for _ in range(len_lst)]

    return zsuv, vagi


def prohid(norm_vector, vagi, zsuv):
    suma = sum(x * w for x, w in zip(norm_vector, vagi)) - zsuv
    return 1 if suma > 0 else -1


# тренування 
def train_perceptron(w, x, d, y, r=0.1):

    error = d - y
    
    if error == 0:
        return w
        
    
    return [w_i + r * error * x_i for w_i, x_i in zip(w, x)]

#==================================
# !!! Тут логіка для Hopfield !!!
#==================================

def hop_umplodet_photo():
    
    uploded_foto = st.file_uploader(
        label="Вибірить 3 фото ",
        type=['png', "jpeg", "jpg"],
        accept_multiple_files=True,
        )
    
    if len(uploded_foto) == 3:           
        return uploded_foto

    else:
        st.error("Вибкріть рівно 3 фото")
        

def binarization(lst):
    return [1 if i >= 0.5 else -1 for i in lst]

def mateix_w(binar_vectors):
    w = [[0 for _ in range(20)] for _ in range(20)]
    
    for binar_vector in binar_vectors:
        for i in range(20):
            for j in range(20):

                if i == j:
                    continue
                else:
                    w[i][j] += binar_vector[i] * binar_vector[j] 
    
    return w


def predict_hopfield(unknown_vector, weights_matrix):
    y = unknown_vector.copy() 
    

    for iteration in range(15):
        y_old = y.copy()
        
        for j in range(20):  
            sum_val = 0
            for i in range(20):  #
                sum_val += weights_matrix[j][i] * y[i]
                
            if sum_val > 0:
                y[j] = 1
            elif sum_val < 0:
                y[j] = -1
        
        if y == y_old:
            break  
            
    return y

#==================================
# !!! Тут логіка для Hamming !!!
#==================================
def init_hamming_weights(binar_vectors):

    m = len(binar_vectors)      
    n = len(binar_vectors[0])   
    
    W1 = []
    for k in range(m):
        w_k = [binar_vectors[k][i] / 2.0 for i in range(n)]
        W1.append(w_k)
        
    B1 = [n / 2.0 for _ in range(m)]
    
    return W1, B1


def predict_hamming(unknown_vector, W1, B1, eps=0.1):

    m = len(W1)
    n = len(unknown_vector)
    
    y1 = []
    for k in range(m):
        s1 = sum(W1[k][i] * unknown_vector[i] for i in range(n)) + B1[k]
        y1.append(s1)
        
    y2 = y1.copy()
    
    for step in range(50):
        y2_old = y2.copy()
        y2_next = []
        
        for j in range(m):
            inhibition = sum(y2_old[k] for k in range(m) if k != j)
            s2 = y2_old[j] - eps * inhibition
            y2_next.append(max(0.0, s2))
            
        y2 = y2_next
        
        active_count = sum(1 for val in y2 if val > 0)
        if active_count <= 1 or y2 == y2_old:
            break
            
    winner_class = y2.index(max(y2)) + 1
    return winner_class, y1, y2