import math


def percorrer_cilindro(cilindro, posicao_inicial, requisicoes):

    posicoes_percorridos = 0
    posicao_atual = posicao_inicial
    print('Cilindro Inicial:\n')
    imprime_cilindro(cilindro, posicao_atual)

    print('Inicio das Requisicoes:\n')
    while len(requisicoes)!= 0:
        d = calcular_menor_distancia(posicao_atual, requisicoes)
        posicoes_percorridos += int(math.fabs(requisicoes[d] - posicao_atual))
        posicao_atual = requisicoes[d]
        imprime_cilindro(cilindro, posicao_atual)
        requisicoes.pop(d)
    print('Posições percorridas: ', posicoes_percorridos)


def calcular_menor_distancia(posicao_atual, requisicoes):


    menor = int(math.fabs(posicao_atual - max(requisicoes))) + 1
    indice_menor = -1


    for indice, requisicao in enumerate(requisicoes):
        distancia = int(math.fabs(requisicao - posicao_atual))
        if distancia < menor:
            menor = distancia
            indice_menor = indice

    return indice_menor

def imprime_cilindro(cilindro, posicao):
    for i in range(0, len(cilindro)):
        if i == posicao:
            print(str(cilindro[i]) + '[X] |', end = '')
        else:
            print(str(cilindro[i]) + ' |', end = '')
    print('\n\n')


if __name__ == "__main__":

    cilindro = [i*1 for i in range(0,40)]
    posicao_inicial = 20
    requisicoes = [9, 1, 12, 10, 34, 36]
    percorrer_cilindro(cilindro, posicao_inicial, requisicoes)