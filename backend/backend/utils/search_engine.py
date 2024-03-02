from fuzzywuzzy import process

def create_mapping(a_list, b_list, threshold=80):
    """
    Create a mapping from elements in A to their best-matching elements in B.
    """
    mapping = {}

    for a in a_list:
        # Get the best match from B for each element in A
        best_match, similarity = process.extractOne(a, b_list)

        # Check if the similarity is above the threshold
        if similarity >= threshold:
            mapping[a] = best_match

    return mapping


