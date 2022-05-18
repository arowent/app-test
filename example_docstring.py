def set_numbers(numbers: str) -> list:
    """_summary_

    Args:
        numbers (str): _description_

    Returns:
        list: _description_
    """
    return list(map(int, numbers.strip()))



print(set_numbers(input('Введите какое то количество символов: ')))