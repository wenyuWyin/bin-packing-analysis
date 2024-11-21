import matplotlib.pyplot as plt
from random import sample


def set_attributes(title: str, x: str, y: str) -> None:
    '''
        Function that sets the basic attributes of a plot
    '''
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.3))


def gen_color(n: int) -> list[tuple[float]]:
    '''
        Generate a list of gradient colors
        Input: n -> number of colors
               base_color -> basic color
               pos -> change towards black/white
    '''
    colors = ['salmon', 'chocolate', 'darkorange', 'olivedrab',
              'lightblue', 'slateblue', 'orchid', 'mediumaquamarine']
    return sample(colors, n)
