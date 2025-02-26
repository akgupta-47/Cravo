import enum

class Category(enum.Enum):
    FOOD = "food"
    ELECTRICAL = "electrical"
    RECREATION = "recreation"
    PLUMBING = "plumbing"
    
class SubCategory(enum.Enum):
    F_DAIRY = "dairy"
    F_BAKERY = "bakery"
    F_SNACKS = "snacks"
    F_POULTRY = "poultry"
    F_VEGETABLE = "vegetables"
    F_FRUIT = "fruits"