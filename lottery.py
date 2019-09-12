from random import choice, sample
from time import sleep
from threading import Thread, Lock

"""
    O método de escalonamento por loteria busca eliminar a chance de starvation
    pois, todos os processos irão receber ao menos um ticket e dessa forma tem
    sempre uma chance de receber a vez no processador, não funciona baseado em 
    prioridades e dessa forma todos os processos podem ser chamados aleatoriamente,
    embora alguns processos possam ter mais tickets que outros todos têm uma boa
    chance de ocupar a CPU.

    Nesse algoritmo foi utilizado uma variável time para simular o tempo de CPU de
    cada processo, pois threading em python não suporta controle por tempo ou prioridade
    das threads, dessa forma foi feito um simulação mais próxima possível de escalonamento
    por loteria.
"""

rc = list(range(20))
i = 100
lottery = list(range(300))
winner = choice(lottery)
lottery_tickets = list(range(300))
num_process = 10

lock = Lock()


class ProcessBase:
    def inicia_processo(self):
        global lottery_tickets
        global lottery
        global num_process

        self.tickets = sample(lottery_tickets, int(len(lottery)/num_process))
        for number in self.tickets:
            lottery_tickets.remove(number)

    def is_empty(self):
        global rc
        if len(rc) == 0:
            print('O processs {} parou porque a regiao crítica está '
                  'vazia.'.format(self.id))
            return True

        return False

    def is_full(self):
        global rc

        if len(rc) >= 40:
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
        self.tickets = []
        self.time = 5

    def input_element(self):
        global i
        global rc
        global lottery_tickets
        global lottery
        global winner

        
        if self.time == 0:
            winner = choice(lottery)
            self.time = 5
            print('O processo {} irá entrar em espera pois o tempo dele acabou'.format(self.id))
        else:
            if self.is_full() or i == 0:
                if i == 0:
                    print('O processo {} foi encerrado porque o número de interações '
                        'foi esgotado'.format(self.id))
                winner = choice(lottery)
                self.stop()
            else:
                print('O processo {} está inicializando...'.format(self.id))
                print('Tempo de CPU: {}'.format(self.time))
                print('O processo {} vai colocar um elemento na '
                    'região crítica'.format(self.id))
                rc.append(self.id)
                i -= 1
                self.time -= 1
                print('O processo {} aumentou o tamanho da região crítica para '
                    '{}'.format(self.id, len(rc)))

    def run(self):
        global winner
        while self.running:
            with lock:
                if len(self.tickets) == 0:
                    self.inicia_processo()
                if winner in self.tickets:
                    if self.time == 5:
                        print('\nO vencedor é: {}\n'.format(winner))
                    self.input_element()
            sleep(2)


class ProcessOutput(Thread, ProcessBase):

    def __init__(self, id):
        Thread.__init__(self)
        self.id = id
        self.running = True
        self.tickets = []
        self.time = 5

    def output_element(self):
        global rc
        global i
        global lottery_tickets
        global lottery
        global winner

        if self.time == 0:
            winner = choice(lottery)
            self.time = 5
            print('O processo {} irá entrar em espera pois o tempo dele acabou'.format(self.id))

        else:
            if self.is_empty() or i == 0:
                if i == 0:
                    print('O processo {} foi encerrado porque o número de interações '
                        'foi esgotado'.format(self.id))
                winner = choice(lottery)
                self.stop()
            else:
                print('O processo {} está inicializando...'.format(self.id))
                print('Tempo de CPU: {}'.format(self.time))
                print('O processo {} vai remover um valor da '
                    'regiao critica'.format(self.id))
                rc.pop()
                i -= 1
                self.time -= 1
                print('O processo {} reduziu o tamanho da região crítica para '
                    '{}'.format(self.id, len(rc)))

    def run(self):
        global winner
        while self.running:
            with lock:
                if len(self.tickets) == 0:
                    self.inicia_processo()
                if winner in self.tickets:
                    if self.time == 5:
                        print('\nO vencedor é: {}\n'.format(winner))
                    self.output_element()
            sleep(2)


if __name__ == '__main__':
    t0 = ProcessInput(0)
    t1 = ProcessOutput(1)
    t2 = ProcessInput(2)
    t3 = ProcessOutput(3)
    t4 = ProcessOutput(4)
    t5 = ProcessInput(5)
    t6 = ProcessInput(6)
    t7 = ProcessOutput(7)
    t8 = ProcessInput(8)
    t9 = ProcessOutput(9)

    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()

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
    t5.join()
    print("O processo 5 parou!")
    t6.join()
    print("O processo 6 parou!")
    t7.join()
    print("O processo 7 parou!")
    t8.join()
    print("O processo 8 parou!")
    t9.join()
    print("O processo 9 parou!")
