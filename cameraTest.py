from GesturesApi import GestureProcessor

def myF():
    print('It Worked!')

gp = GestureProcessor()
gp.bind('Infinity', myF())
gp.process()

