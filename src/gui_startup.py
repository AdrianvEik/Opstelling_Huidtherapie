
from Base_interface import *
from src.Physics_Interface.Physics_interface import Base_physics

def startup_basic_test():
    """
    Test de startup functie
    """
    gui = Base_interface()
    gui.mainloop()

    return True

if __name__ == "__main__":
    startup_basic_test()