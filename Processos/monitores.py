from time import sleep
from threading import Thread, Lock

"""
    Em python não existem monitores como o synchronized do Java,
    porém existe uma sincronização primitiva utilizando o objeto
    Lock de threading do python, que oferece uma simples funcionalidade
    de exclusão mútua que funciona como um monitor.

    O objeto Lock possui dois valores possíveis que só podem ser alterados
    pelos métodos básicos acquire() e release(), quando um processo toma conta
    desse lock ele é alterado para locked e nenhum outro processo pode acessar a
    região crítica até que esse processo dê release no lock, utilizando o with(lock)
    isso é feito de forma automática.
"""

rc = list(range(5))
i = 30
lock = Lock()


class ProcessBase:
    def is_empty(self):
        global rc
        if len(rc) == 0:
            print('O processs {} parou porque a regiao crítica está '
                  'vazia.'.format(self.id))
            return True

        return False

    def is_full(self):
        global rc

        if len(rc) >= 10:
            print('O processo {} parou porque a regiao critica chegou '
                  'a 10 elementos.'.format(self.id))
            return True

        return False

    def stop(self):
        self.running = False


class ProcessInput(Thread, ProcessBase):

    def __init__(self, id):
        Thread.__init__(self)
        self.id = id
        self.running = True

    def input_element(self):
        global rc
        global i

        if self.is_full() or i == 0:
            if i == 0:
                print('O processo {} foi encerrado porque o número de interações '
                      'foi esgotado'.format(self.id))
            self.stop()
        else:
            print('O processo {} está inicializando...'.format(self.id))
            sleep(2)
            print('O processo {} vai colocar um elemento na '
                  'região crítica'.format(self.id))
            rc.append(self.id)
            i -= 1
            print('O processo {} aumentou o tamanho da região crítica para '
                  '{}'.format(self.id, len(rc)))

    def run(self):
        while self.running:
            with lock:
                self.input_element()
            sleep(5)


class ProcessOutput(Thread, ProcessBase):

    def __init__(self, id):
        Thread.__init__(self)
        self.id = id
        self.running = True

    def output_element(self):
        global rc
        global i
        if self.is_empty() or i == 0:
            if i == 0:
                print('O processo {} foi encerrado porque o número de interações '
                      'foi esgotado'.format(self.id))
            self.stop()
        else:
            print('O processo {} está inicializando...'.format(self.id))
            sleep(2)
            print('O processo {} vai remover um valor da '
                  'regiao critica'.format(self.id))
            rc.pop()
            i -= 1
            print('O processo {} reduziu o tamanho da região crítica para '
                  '{}'.format(self.id, len(rc)))

    def run(self):
        while self.running:
            with lock:
                self.output_element()
            sleep(5)


if __name__ == '__main__':
    t0 = ProcessInput(0)
    t1 = ProcessOutput(1)
    t2 = ProcessInput(2)
    t3 = ProcessOutput(3)
    t4 = ProcessOutput(4)

    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t0.join()
    print("O processo 0 parou!")
    t1.join()
    print("O processo 1 parou!")
    t2.join()
    print("O processo 2 parou!")
    t3.join()
    print("O processo 3 parou!")
    t4.join()
    print("O processo 4 parou!")
