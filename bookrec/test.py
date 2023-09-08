import pickle

# stands for: Item-Item & User-User; Item-Item & ALS, User-User & ALS, User-User & Item-Item, ALS & Item-Item, ALS & User-User
# only needed for initialisation
#rotation_list = ['IIUU', 'IIALS', 'UUALS', 'UUII', 'ALSII', 'ALSUU']


def main():

    # created recommended list by different algorithms
    book_list = ['ii_list', 'uu_list', 'als_list']

    # open pickle to receive current rotation state
    with open('rotator_pickle.pk', 'rb') as fi:
        current_rotation_list = pickle.load(fi)
        rotation_state = current_rotation_list[0]

    # search current rotation state and create content dictionary accordingly
    # also call the function to initiate the rotation of the state list
    if rotation_state == 'IIUU':
        context_dict = {'rotation_state': rotation_state, 'books_a': book_list[0], 'books_b': book_list[1]}
        rotate_content_list()
        return context_dict
    elif rotation_state == 'IIALS':
        context_dict = {'rotation_state': rotation_state, 'books_a': book_list[0], 'books_b': book_list[2]}
        rotate_content_list()
        return context_dict
    elif rotation_state == 'UUALS':
        context_dict = {'rotation_state': rotation_state, 'books_a': book_list[1], 'books_b': book_list[2]}
        rotate_content_list()
        return context_dict
    elif rotation_state == 'UUII':
        context_dict = {'rotation_state': rotation_state, 'books_a': book_list[1], 'books_b': book_list[0]}
        rotate_content_list()
        return context_dict
    elif rotation_state == 'ALSII':
        context_dict = {'rotation_state': rotation_state, 'books_a': book_list[2], 'books_b': book_list[0]}
        rotate_content_list()
        return context_dict
    elif rotation_state == 'ALSUU':
        context_dict = {'rotation_state': rotation_state, 'books_a': book_list[2], 'books_b': book_list[1]}
        rotate_content_list()
        return context_dict


def rotate_content_list():
    with open('rotator_pickle.pk', 'rb') as fi:
        current_rotation_list = pickle.load(fi)
    current_rotation_list.append(current_rotation_list[0])
    del current_rotation_list[0]
    with open('rotator_pickle.pk', 'wb') as fi:
        pickle.dump(current_rotation_list, fi)


if __name__ == '__main__':
    main()
