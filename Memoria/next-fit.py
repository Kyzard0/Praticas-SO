import time

last_assignment_index = 0


class Memory:
    def __init__(self, size):
        self.size = size
        if size > 0:
            self.__data = [None] * size
            self.bitmap = [0] * size
            self.map = {}
            self.show()
        else:
            raise Exception("Size must be a positive scalar!")

    def allocate(self, tag, space):
        index = -1
        count = 0
        global last_assignment_index

        i = last_assignment_index
        print("\nÚltimo índice alocado: ", i)
        while i < self.size:
            j = i
            free = 0
            full = False

            while j < self.size:
                # print(free, self.bitmap[i], self.bitmap[j])
                if self.bitmap[j] == 0:
                    free += 1
                    j = (j + 1) % self.size
                else:
                    free = 0
                    if i == 1:
                        count += 1

                    j = (j + 1) % self.size
                    if count == 2:
                        i = self.size
                    else:
                        i = j
                    break
                if free == space:
                    index = i
                    last_assignment_index = index
                    i = self.size
                    break

        if index < 0:
            print(f"A memória está cheia e não pode alocar {space}MB para {tag}!")
            print("Tentando compactar...")

            if self.bitmap.count(0) >= space:
                self.compact()
                self.allocate(tag, space)
        else:
            for i in range(index, index+space):
                self.__data[i] = tag
                self.bitmap[i] = 1

            self.map[tag] = space
            print("Alocando", space, "MB para", tag, "no índice", index)
            self.show()

    def deallocate(self, tag):
        aux = False
        for i in range(self.size):
            if self.__data[i] == tag:
                aux = True
                self.__data[i] = None
                self.bitmap[i] = 0

        if aux:
            del self.map[tag]
            print("Desalocando ", tag)
            self.show()

    def compact(self):
        count = 0

        while 0 in self.bitmap:
            self.bitmap.remove(0)
            self.__data.remove(None)
            count += 1

        for i in range(count):
            self.bitmap.append(0)
            self.__data.append(None)

        print(f"A memoria foi compactada. A memoria possui um bloco de {count-1}MB disponivel agora!")
        self.show()

    def show(self):
        info = ""

        tags = []
        size = []
        i = -1
        while i < self.size-1:
            i += 1
            if self.__data[i] is None:
                for j in range(i, self.size):
                    if self.__data[j] is not None or j == self.size-1:
                        tags.append("FREE")
                        size.append(j-i)
                        i = j if j == self.size-1 else j - 1
                        break
            else:
                tags.append(self.__data[i])
                size.append(self.map[self.__data[i]])
                i = i + self.map[self.__data[i]] - 1

        sizeaux = [None] * len(size)
        for i in range(len(size)):
            sizeaux[i] = int((size[i]/max(size) * 20))

        for i in range(len(tags)):
            aux = ""
            m = sizeaux[i]//2
            if m == 0:
                if tags[i] is None:
                    aux += "_"
                else:
                    aux += "|" + tags[i] + " " + str(size[i]) + "MB" + "|"
            else:
                aux += "|"
                for j in range(sizeaux[i]):
                    if j == m:
                        aux = aux + tags[i] + " " + str(size[i]) + "MB"
                    else:
                        aux += " "
                aux += "|"

            info += aux

        info = "\n|" + info.replace('||', '|') + "|\n"
        border = "=" * (len(info)-2)

        print(border + info + border)

mp = Memory(512)

print("\n\n")
mp.allocate("A", 58)
time.sleep(0.5)
print("\n\n")
mp.allocate("B", 150)
time.sleep(0.5)
print("\n\n")
mp.allocate("C", 110)
time.sleep(0.5)
print("\n\n")
mp.deallocate("B")
time.sleep(0.5)
print("\n\n")
mp.allocate("E", 90)
time.sleep(0.5)
print("\n\n")
mp.allocate("F", 10)
time.sleep(0.5)
print("\n\n")
mp.allocate("G", 51)
time.sleep(0.5)
print("\n\n")
mp.allocate("H", 26)
time.sleep(0.5)
print("\n\n")
mp.allocate("I", 56)
time.sleep(0.5)
print("\n\n")
mp.allocate("J", 100)
