def train_val_test_split(dataset, shuffle=True, validation_split=0.1, test_split=0.1, remove=0.5):
    """
    Split image ids into training, validation, and test sets.
    """
    if validation_split < 0.0 or validation_split > 1.0:
        raise ValueError(f"{validation_split} is not a valid validation split ratio.")

    if test_split < 0.0 or test_split > 1.0:
        raise ValueError(f"{test_split} is not a valid test split ratio.")

    image_ids_list = dataset.get_image_ids()
    if shuffle:
        sorted(image_ids_list)
        random.seed(42)
        random.shuffle(image_ids_list)

    split_index = int((1 - (validation_split+test_split+remove)) * len(image_ids_list))
    split_index1 = int((1 - (validation_split+remove)) * len(image_ids_list))
    split_index2 = int((1 - (validation_split+remove) + test_split) * len(image_ids_list))
    train_image_ids = image_ids_list[:split_index]
    valid_image_ids = image_ids_list[split_index:split_index1]
    test_image_ids = image_ids_list[split_index1:split_index2]

    def filter_by_ids(ids, imgs_anns_dict):
        return {x: imgs_anns_dict[x] for x in ids}

    train_dataset = copy.deepcopy(dataset)
    train_dataset.id = dataset.id + "-TRAIN"

    valid_dataset = copy.deepcopy(dataset)
    valid_dataset.id = dataset.id + "-VALID"

    test_dataset = copy.deepcopy(dataset)
    test_dataset.id = dataset.id + "-Test"

    imgs_anns_dict = dataset.imgs_anns_dict

    train_imgs_anns_dict = filter_by_ids(train_image_ids, imgs_anns_dict)
    valid_imgs_anns_dict = filter_by_ids(valid_image_ids, imgs_anns_dict)
    test_imgs_anns_dict = filter_by_ids(test_image_ids,imgs_anns_dict)

    train_dataset.image_ids = train_image_ids
    valid_dataset.image_ids = valid_image_ids
    test_dataset.image_ids = test_image_ids

    train_dataset.imgs_anns_dict = train_imgs_anns_dict
    valid_dataset.imgs_anns_dict = valid_imgs_anns_dict
    test_dataset.imgs_anns_dict = test_imgs_anns_dict

    print(
        "Num of instances for training set: %d, validation set: %d, and test set: %d"
        % (len(train_image_ids), len(valid_image_ids), len(test_image_ids))
    )
    return train_dataset, valid_dataset, test_dataset