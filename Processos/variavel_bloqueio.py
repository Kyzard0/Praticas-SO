from time import sleep
from threading import Thread

turn = 0  # Variável de bloqueio
rc = list(range(5))


class Process(Thread):

    def __init__(self, id):
        Thread.__init__(self)
        self.id = id
        self.running = True
        self.act = 0

    def critical_section(self):
        global rc

        print('O processo {} está na entrando na região crítica'.format(self.id))

        sleep(5)
        if len(rc) == 0:
            print('O processo {} está saindo da região crítica, '
                  'porque a região crítica está vazia'.format(self.id))
            self.stop()
        else:
            print('O processo {} vai dar um pop na região crítica'.format(
                  self.id))
            rc.pop()
            print('O processo {} removeu um valor da região crítica"'
                  '- novo tamanho é {}'.format(self.id, len(rc)))
            sleep(5)
            print('O processo {} está saindo da região crítica'.format(self.id))

    def process_run(self):
        global turn
        global rc

        print('O processo {} está iniciando o trabalho...'.format(self.id))

        if len(rc) == 0:
            print('O processo {} vai parar, porque a região crítica está '
                  'vazia.'.format(self.id))
            self.stop()

        else:
            while turn == 1:  # Enquanto turn = 1, a região crítica está em uso e o processo irá esperar.
                print('O processo {} está aguardando a liberação'.format(
                      self.id))
                sleep(2)

            turn = 1

            self.critical_section()
            self.act += 1
            turn = 0
            print('O processo {} está finalizando o trabalho...'.format(self.id))
            sleep(2)

    def run(self):
        while self.running:
            self.process_run()

    def stop(self):
        self.running = False
        print('O processo {} parou com {} ações'.format(self.id, self.act))


if __name__ == '__main__':
    t0 = Process(0)
    t1 = Process(1)
    t2 = Process(2)
    t3 = Process(3)
    t4 = Process(4)

    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t0.join()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
