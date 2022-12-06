from game import *
# this file contains the main code to the entire game


g = Game()
g.connect_to_server()
while g.running:
    g.menu()
    g.new()


pg.quit()