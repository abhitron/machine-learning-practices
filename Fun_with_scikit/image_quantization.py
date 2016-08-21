import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
import mahotas as mh



def compress_image(image_location):
    original_image = np.array(mh.imread(image_location),dtype=np.float64)/255
    
    #china = load_sample_image("china.jpg")
    #original_image=np.array(china, dtype=np.float64) / 255
    width,height,depth = original_image.shape
    image_reduced = np.reshape(original_image,(width*height,depth))
    image_array_sample = shuffle(image_reduced,random_state=0)[:1000]
    print("here0")
    estimator = KMeans(n_clusters=64,random_state=0)
    estimator.fit(image_array_sample)
    print("here1")
    cluster_assignments = estimator.predict(image_reduced)
    print("here2")
    compressed_colors = estimator.cluster_centers_
    compressed_image = np.zeros((width,height,depth))
    print("here3")
    index = 0
    for i in range(width):
        for j in range(height):
            compressed_image[i][j]=compressed_colors[cluster_assignments[index]]
            index+=1
    print("here4")
    plt.subplot(122)
    plt.title('Original Image')
    plt.imshow(original_image)
    plt.axis('off')
    plt.subplot(121)
    plt.title('Compressed Image')
    plt.imshow(compressed_image)
    plt.axis('off')
    plt.show()

compress_image("test.jpg")
