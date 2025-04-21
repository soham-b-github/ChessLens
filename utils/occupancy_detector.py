import cv2
import numpy as np

def is_occupied(square_img, std_thresh=40, edge_thresh=100):
    std_dev = np.std(square_img)
    edges = cv2.Canny(square_img, 50, 150)
    edge_density = np.sum(edges > 0) / square_img.size
    print(f"Std_dev = {std_dev}")
    print(f"edge_density = {edge_density}")
    # return std_dev > std_thresh and edge_density > 0.02
    return edge_density > 0.02


# def is_occupied_cnn(square_img, model):
#     img = cv2.resize(square_img, (64, 64))
#     img = img / 255.0
#     img = img.reshape(1, 64, 64, 1)
#     pred_prob = model.predict(img)[0][0]
#     return pred_prob > 0.5