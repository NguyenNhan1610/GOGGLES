import os

import torch

from goggles.constants import *
from goggles.models.semantic_ae import SemanticAutoencoder
from goggles.train import load_datasets
from goggles.utils.vis import save_prototype_patch_visualization


input_image_size = 128
filter_species_ids = [14, 90]
patch_size = 1


def test_load_model():
    _, train_dataset_deterministic, _ = load_datasets(input_image_size, CUB_DATA_DIR, filter_species_ids)

    model = SemanticAutoencoder(
        input_image_size, patch_size,
        train_dataset_deterministic.num_attributes)
    model.load_state_dict(torch.load(os.path.join(MODEL_DIR, 'model.pt')).state_dict())

    if torch.cuda.is_available():
        model.cuda()

    return model


def test_prototype_vis():
    _, train_dataset_deterministic, _ = load_datasets(input_image_size, CUB_DATA_DIR, filter_species_ids)

    model = SemanticAutoencoder(
        input_image_size, patch_size,
        train_dataset_deterministic.num_attributes)
    model.load_state_dict(torch.load(os.path.join(MODEL_DIR, 'model.pt')).state_dict())
    if torch.cuda.is_available():
        model.cuda()

    nearest_patches_for_prototypes = \
        model.get_nearest_patches_for_prototypes(
            train_dataset_deterministic)

    save_prototype_patch_visualization(
        model, train_dataset_deterministic, nearest_patches_for_prototypes, '../out/prototypes/')


if __name__ == '__main__':
    test_load_model()
