from . import ma, adx
from typing import Callable, Tuple, Optional

# Define a mapping from (category, type) to the corresponding module
# Category 0: Technical Indicators
CALC_MODULES = {
    (0, 0): ma,
    (0, 1): adx,
}

def get_calc_functions(category: int, type: int) -> Tuple[Optional[Callable], Optional[Callable]]:
    """
    A factory function that returns calculation and report functions based on category and type.

    Args:
        category (int): The category of the calculation (e.g., 0 for Technical Indicators).
        type (int): The type of calculation within the category (e.g., 0 for MA, 1 for ADX).

    Returns:
        Tuple[Optional[Callable], Optional[Callable]]: A tuple containing the calc function
                                                       and the report function, or (None, None) if not found.
    """
    module = CALC_MODULES.get((category, type))
    
    if module:
        return (getattr(module, 'calc', None), getattr(module, 'report', None))
    
    return (None, None)