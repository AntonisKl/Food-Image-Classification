from pathlib import Path
from typing import List, Set

import pandas

INPUT_DATASET = './dataset/train_set'  # Path to a folder that contains all training images
PATH_LABELS = './dataset/train_labels.csv'  # Path to CSV file containing training labels
PATH_DESTINATION = './dataset/train_set_labelled'  # Where new folder will be created with dataset organised in folders by label


def move_files_to_class_folders() -> None:
    # Get a dict mapping file name to its label
    # Example: {'train_1.jpg': 21}
    file_label_dict = pandas.read_csv(PATH_LABELS).set_index('img_name').to_dict()['label']
    for file in Path(INPUT_DATASET).iterdir():
        label = file_label_dict[file.name]
        dest_path = Path(PATH_DESTINATION) / str(label)
        # Create missing directories if necessary
        dest_path.mkdir(parents=True, exist_ok=True)
        # Copy the file to the folder with a correct label
        file.rename(dest_path / file.name)


def rename_labels_to_characters():
    for folder in Path('dataset/train_set_labelled_az').iterdir():
        new_filename = ''
        for char in folder.name:
            new_filename += chr(int(char) + 65)
        new_filename = new_filename.rjust(3, 'A')
        folder.rename(new_filename)


def get_nonsense_examples(path: str) -> Set[str]:
    nonsense_examples = set()
    with open(path, mode='r') as file:
        for name in file.readlines():
            nonsense_examples.add(name.strip() + '.jpg')
    return nonsense_examples


def remove_nonsense_examples(dataset_path: str, copy_to: str, nonsense_files: Set[str]) -> None:
    Path(copy_to).mkdir(exist_ok=True)
    for file in Path(dataset_path).rglob('*.*'):
        if file.name in nonsense_files:
            file.rename(Path(copy_to, file.name))


if __name__ == '__main__':
    remove_nonsense_examples(dataset_path='dataset/train_set_labelled_az',
                             copy_to='nonsense_examples',
                             nonsense_files=get_nonsense_examples('nonsense_examples.txt'))
