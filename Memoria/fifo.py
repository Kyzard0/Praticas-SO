import threading
import random
import time

"""
Tentei implementar outro algoritmo pois o clock era muito parecido,
porém não consegui implementar a tempo, então optei por trocar para
o algoritmo FIFO para que de certa forma seja diferente mesmo sendo
bem simples e o second chance sendo uma melhoramento do FIFO.

Escolhi por deixar a variável de bit R para ilustrar que no FIFO,
mesmo que o processo seja bastante usado ele irá ser retirado da
lista quando ocorrer um miss e ele for o mais antigo na lista.
"""


class Manager:

    def __init__(self, main_size, virtual_size):
        self.ref = [0] * main_size
        self.main_memory = [None] * main_size
        self.virtual_memory = [None] * virtual_size
        self.processes = []

    def main_free(self):
        return self.main_memory.count(None)

    def virtual_free(self):
        return self.virtual_memory.count(None)

    def start(self, process):
        if len(process.data) <= self.virtual_free():
            self.processes.append(process)
            for item in process.data:
                print(f"Alocando {item} do processo {process.tag} na memória virtual...")
                self.virtual_memory.remove(None)
                self.virtual_memory.append(item)
        else:
            print("A memória virtal está cheia!")

    def get(self, tag):
        print("\n\n\n")
        if tag in self.main_memory:
            print(f"HIT! Page {tag}")
            index = self.main_memory.index(tag)
            self.ref[index] = 1
            self.show()
            return tag
        elif tag in self.virtual_memory:
            print(f"MISS! Page {tag}")
            self.miss(tag)
            self.show()
            return tag
        else:
            print(f"O dado {tag} não existe!")

    def miss(self, tag):

        if None in self.main_memory:
            aux = self.main_memory.index(None)
            self.main_memory.pop(aux)
            self.ref.pop(aux)
            self.main_memory.append(tag)
            self.ref.append(1)
        else:
            print(f"PROCESSO {self.main_memory[0]} REMOVIDO DA MEMÓRIA")
            self.main_memory.pop(0)
            self.ref.pop(0)
            self.main_memory.append(tag)
            self.ref.append(1)

    def run(self):
        threading.Thread(target=self.update_ref, args=()).start()
        for process in self.processes:
            threading.Thread(target=self.processing, args=(process,)).start()
            time.sleep(1.1)

    def update_ref(self):
        while True:
            time.sleep(5)
            print("\n\n\n======================================\n============ REF UPDATED! ============\n======================================\n")
            for i in range(len(self.ref)):
                if self.ref[i] != 0:
                    self.ref[i] = 0

    def processing(self, process):
        while True:
            index = random.randint(0, process.size-1)
            item = process.tag + str(index)
            result = self.get(item)

            time.sleep(2)

    def show(self):
        border1 = "=" * int(len(self.main_memory) * 13.2)
        border2 = "=" * int(len(self.virtual_memory) * 5.1)
        info1 = ""

        for i in range(len(self.main_memory)):
            if self.main_memory[i] is not None:
                info1 = info1 + "|  " + self.main_memory[i] + " R = " + str(self.ref[i]) + "  |"
            else:
                info1 = info1 + "|            |"

        info1 = info1.replace("||", "|")

        info2 = ""
        for item in self.virtual_memory:
            if item is not None:
                info2 = info2 + "| " + item + " |"
            else:
                info2 = info2 + "|    |"

        info2 = info2.replace("||", "|")

        print("VIRTUAL MEMORY STATE")
        print(border2 + "\n" + info2 + "\n" + border2)
        print("MAIN MEMORY STATE")
        print(border1 + "\n" + info1 + "\n" + border1)


class Process:
    def __init__(self, tag, size):
        self.size = size
        self.tag = tag
        self.data = [tag + str(i) for i in range(size)]


manager = Manager(main_size=8, virtual_size=16)

p1 = Process("A", 4)
p2 = Process("B", 4)
p3 = Process("C", 4)
p4 = Process("D", 4)

manager.start(p1)
manager.start(p2)
manager.start(p3)
manager.start(p4)

manager.run()
