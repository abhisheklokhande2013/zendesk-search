#all common util function can be added here

from pyfiglet import Figlet

def print_logo():
    """Generate and print ASCII logo on Console"""
    fig = Figlet(font='epic', width=100)
    print(fig.renderText('ZENDESK   SEARCH  -   APP'))
