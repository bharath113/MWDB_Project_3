from tasks.input_output import *
from tasks.features import *
from tasks.dim_red import perform_dim_red
import numpy as np
from tasks.PPRClassifier import PersonalizedPageRankClassifier

def supply_inputs_to_ppr(input_folder_path = 'Dataset', test_folder_path = 'Dataset', feature_model = 'elbp', k = 100,
						 label_name = 'type', dim_red_technique = 'svd', output_folder='output',
						 latent_semantics_file_name='task1_latent_semantics.csv'):
	images_with_attributes = get_images_and_attributes_from_folder(input_folder_path)
	images = get_image_arr_from_dict(images_with_attributes)
	#labels = get_label_arr_from_dict(images_with_attributes, label_name = label_name)
	image_features = get_flattened_features_for_images(images, feature_model)

	dim_red_technique = dim_red_technique.lower()
	left_factor_matrix, right_factor_matrix = perform_dim_red(dim_red_technique, image_features, k)

	image_objects = get_image_objects_from_dict(images_with_attributes)
	for i in range(len(image_objects)):
		image_obj = image_objects[i]
		img_latent_features = left_factor_matrix[i]
		image_obj.set_latent_features(img_latent_features)

	test_image_objects = get_image_objects_from_folder(test_folder_path)

	for image_object in test_image_objects:
		image = image_object.image_arr
		features = get_flattened_features_for_a_single_image(image,feature_model)
		latent_features = np.matmul(features, np.matrix.transpose(right_factor_matrix))
		image_object.set_latent_features(latent_features)

	test(image_objects, test_image_objects)

def test(image_objects, test_image_objects):
	ppr_classifier = PersonalizedPageRankClassifier(input_image_objects = image_objects,
										 test_image_objects = test_image_objects,
										 classification_label = 'type',
										num_nodes_to_consider_for_classifying = 15,
										num_similar_nodes_to_form_graph = 15)
	type_labels = ppr_classifier.get_classified_labels()
	print('Type Labels:')
	print(type_labels)
	ppr_classifier = PersonalizedPageRankClassifier(input_image_objects=image_objects,
													test_image_objects=test_image_objects,
													classification_label='subject_id',
													num_nodes_to_consider_for_classifying=45,
													num_similar_nodes_to_form_graph=45)
	subject_labels = ppr_classifier.get_classified_labels()
	print('Subject Labels:')
	print(subject_labels)
	ppr_classifier = PersonalizedPageRankClassifier(input_image_objects=image_objects,
													test_image_objects=test_image_objects,
													classification_label='image_id',
													num_nodes_to_consider_for_classifying=12,
													num_similar_nodes_to_form_graph=12)
	image_sample_labels = ppr_classifier.get_classified_labels()
	print('Image Sample Labels:')
	print(image_sample_labels)


supply_inputs_to_ppr(input_folder_path='Dataset_100', test_folder_path='Sample_Dataset', feature_model='elbp', k=100,
						 label_name='type',
						 dim_red_technique='svd')

