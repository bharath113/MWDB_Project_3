from .cache import *
from .lsh import LocalitySensitiveHashing
from .input_output import *

def task4(input_folder, feature_model, num_layers, num_hashes_per_layer, query_image_path, num_similar_images_to_retrieve,
          output_folder_path = 'lsh_output'):
    images_with_attributes, image_features  = get_images_with_attributes_and_features(input_folder, feature_model)
    image_objects = get_image_objects_from_dict(images_with_attributes, image_features)
    print('Initializing Locality Sensitive Hashing index structure')
    lsh_obj = LocalitySensitiveHashing(num_layers, num_hashes_per_layer, image_objects)

    query_image_obj = get_image_object_from_file(query_image_path)
    query_image_obj.set_features(get_flattened_features_for_a_single_image(query_image_obj.image_arr, feature_model))

    result_images = lsh_obj.get_similar_objects(query_image_obj, num_similar_images_to_retrieve)
    image_file_name_tuple_list = []
    image_file_name_tuple_list.append((query_image_obj.image_arr, f'0_query_{query_image_obj.filename}'))
    for i in range(len(result_images)):
        image_obj = result_images[i]
        file_name = f'{i+1}_{image_obj.filename}'
        image_file_name_tuple_list.append((image_obj.image_arr, file_name))
    save_images_by_clearing_folder(image_file_name_tuple_list, output_folder_path)
    # for i in range(int(len(result_images)/5), len(result_images)):
    #     image_obj = result_images[i]
    #     file_name = f'{i + 1}_{image_obj.filename}'
    #     image_file_name_tuple_list.append((image_obj.image_arr, file_name))
    print(f'LSH result images are saved in {output_folder_path}')
    lsh_obj.print_index_structure_stats()
    return result_images



