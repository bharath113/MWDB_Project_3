
class LocalitySensitiveHashing:

    def __init__(self, num_layers, num_hashes_per_layer, input_vectors):
        self.num_layers = num_layers
        self.num_hashes_per_layer = num_hashes_per_layer
        self.input_vectors = input_vectors
        number_of_features = len(input_vectors[0])
        self.random_planes = [np.random.randn(self.num_hashes_per_layer, number_of_features)
                              for i in range(self.num_layers)]

    def get_hash_code_for_object(self, input_vector):
        hash_codes = []
        for layer_no in range(self.num_layers):
            hash_code = ""
            for plane in self.random_planes:
                dot_product = input_vector.dot(plane)
                if dot_product < 0:
                    hash_code += '0'
                else:
                    hash_code += '1'
            hash_codes.append(hash_code)
        return hash_codes
