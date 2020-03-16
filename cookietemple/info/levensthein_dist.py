AVAILABLE_HANDLES = ['cli', 'web', 'gui', 'cli-python', 'cli-java', 'cli-kotlin', 'web-website-python',
                     'web-restapi-python',
                     'gui-python', 'gui-java']

SIMILARITY_FACTOR = (1 / 3)


def levensthein_dist(input_command: str, candidate: str) -> int:
    """
    This function implements the Levenshtein algorithm to determine, in case of a non-existing handle,
    if theres a very similar command to suggest.

    TODO: SPACE-OPTIMIZATION (currently O(n^2) could be done in O(n) using only two arrays)

    :param input_command: The non-existing handle the user gave as input
    :param candidate: The (possible similar) alternative command
    :return: The similarity between the two strings measured by the levensthein distance
    """

    if not input_command or not candidate:
        return max(len(input_command), len(candidate))  # at least one string is empty

    dp_table = [[0 for col in range(len(input_command) + 1)] for row in range(len(candidate) + 1)]

    dp_table[0] = list(range(0, len(input_command) + 1))
    for i in range(1, len(candidate) + 1):
        dp_table[i][0] = i

    # now choose minimum levensthein distance from the three option delete/replace/insert
    # if chars are the same -> levensthein distance is the same as for those substring without these chars of input_command
    # and candidate

    for i in range(1, len(candidate) + 1):
        for j in range(1, len(input_command) + 1):
            # choose minimum edit distance from delete, replace or insert at current substring
            if input_command[j - 1] == candidate[i - 1]:
                dp_table[i][j] = dp_table[i - 1][j - 1]
            else:
                dp_table[i][j] = min(min(dp_table[i][j - 1], dp_table[i - 1][j - 1]), dp_table[i - 1][j]) + 1

    return dp_table[len(candidate)][len(input_command)]


def most_similar_command(command: str) -> str:
    """
    This function determines whether its possible to suggest a similar command.
    The similarity is determined by the levensthein distance and a factor (currently 1/3)
    sets a limit where a similar command is useful to be suggested.

    :param command: The command given by the user
    :return: A similar command or the empty string if there's none
    """
    min = 999999  # some random large integer -> we will never have handles that are larger than 1000 character
    sim_command = ""

    # for each valid handle calculate the levensthein distance and if one is found that is a new minimal distance,
    # replace it and take this handle as the most similar command.
    for handle in AVAILABLE_HANDLES:
        dist = levensthein_dist(command, handle)
        lim = int(len(command) * SIMILARITY_FACTOR)

        if lim >= dist and min >= dist:
            min = dist
            sim_command = handle

    return sim_command
