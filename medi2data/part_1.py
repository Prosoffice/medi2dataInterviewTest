test_data = [
    {'name': 'Prosper', 'age': 30},
    {'name': 'Paul', 'age': 25},
    {'name': 'Romeo', 'age': 35}
]


def sort_dict_list(dict_list, key, ascending=True):
    """
    Sort a list of dictionaries based on a specified key.
    Returns:
    list: A sorted list of dictionaries.
    """
    if not dict_list:
        return []
    if key not in dict_list[0]:
        raise KeyError(f"'{key}' not found in dictionary keys")
    return sorted(dict_list, key=lambda x: x[key], reverse=not ascending)

"""
Code Quality: The function name <sort_dict_list> is well written and self explanatory as to what the func does.
              Code quality is generally okay, but could be better, also the code works
              It raises a KeyError if the specified key is not found in the dictionaries, which is good error handling.
              
Correctness: I have tested the code and it works in sorting a list of dictionaries based on a specified key.

Efficiency: The code has a time complexity of O(n*log(n)) due to the sorting operation, 
            where 'n' is the number of dictionaries in the list.  Which is good. 
            And the space complexity is O(n).
            
Documentation and Comments: On a good side the code includes a docstring that provides a brief description of what the 
                            function does, its parameters, and the return value. 
                            
                            Would be better to add a few more comments within the code to explain the fairly complex 
                            logic section at line 13 to make it more readable for the team

Error Handling: The code handles the case where the specified key is not found in the dictionaries and raises a KeyError
                which is a good practice.


Suggestions for Improvement: For starters, adding type hints to the function signature (e.g., List[Dict[str, Any]]) 
                would improve code readability and make it easier to maintain
                
                Adding more comment to the complex logic part
"""

print(sort_dict_list(test_data, 'age', ascending=True))