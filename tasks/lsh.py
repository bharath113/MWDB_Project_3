import numpy as np
from scipy.spatial import distance

class LocalitySensitiveHashing:

    def __init__(self, num_layers, num_hashes_per_layer, image_objects):
        self.num_layers = num_layers
        self.num_hashes_per_layer = num_hashes_per_layer
        self.image_objects = image_objects
        number_of_features = len(image_objects[0].features)
        self.random_planes = [np.random.randn(self.num_hashes_per_layer, number_of_features)
                              for i in range(self.num_layers)]
        self.hash_buckets_per_layer = [{} for i in range(self.num_layers)]
        self.create_index_structure_with_input_vectors()

    def create_index_structure_with_input_vectors(self):
        hash_buckets_per_layer = self.hash_buckets_per_layer
        for idx, image_obj in enumerate(self.image_objects):
            input_vector = image_obj.features
            hash_codes = self.get_hash_codes_for_object(input_vector)
            for i in range(self.num_layers):
                buckets_dict = hash_buckets_per_layer[i]
                hash_code = hash_codes[i]
                if hash_code not in buckets_dict:
                    buckets_dict[hash_code] = []
                buckets_dict[hash_code].append(idx)

    def get_hash_codes_for_object(self, input_vector):
        hash_codes = []
        for layer_no in range(self.num_layers):
            hash_code = ""
            for plane in self.random_planes[layer_no]:
                dot_product = input_vector.dot(plane)
                if dot_product < 0:
                    hash_code += '0'
                else:
                    hash_code += '1'
            hash_codes.append(hash_code)
        return hash_codes

    def retrieve_objects_in_bucket(self, layer_num, hashcode):
        object_indices = self.hash_buckets_per_layer[layer_num][hashcode]
        return [self.image_objects[index] for index in object_indices]

    def get_hash_buckets_per_layer(self):
        return self.hash_buckets_per_layer

    def compute_distance(self, query_image_features, hash_bucket_image_features):
        return distance.euclidean(query_image_features, query_image_features)

    def get_similar_objects(self, query_image_obj, num_similar_images_to_retrieve):
        hash_codes = self.get_hash_codes_for_object(query_image_obj.features)
        image_set = set()
        for idx, hash_code in enumerate(hash_codes):
            images = self.retrieve_objects_in_bucket(idx, hash_code)
            image_set.update(images)


