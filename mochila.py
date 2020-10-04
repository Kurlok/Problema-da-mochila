import numpy as npy
import random as rd
import matplotlib.pyplot as plt

#Definindo as variáveis

#mochila_peso_max = int(input("Digite o peso máximo que a mochila aguenta:\n"))
mochila_peso_max = 300
#qtd_itens = int(input("Digite a quantidade de itens que serão combinadas para colocar na mochila:\n"))
qtd_itens = 6

#peso_item_min = int(input("Digite o peso mínimo para o item:\n"))
peso_item_min = 10

#peso_item_max  = 0
#while peso_item_max  < peso_item_min:
#  peso_item_max  = int(input("Digite o peso máximo para o item:\n"))
#  if peso_item_max  < peso_item_min:
#    print('O peso máximo do item não pode ser inferior ao peso mínimo') 
peso_item_max = 100

#valor_item_min = int(input("Digite o valor mínimo para o item:\n"))
valor_item_min = 15

#valor_item_max = 0;
#while valor_item_max < valor_item_min:
#  valor_item_max = int(input("Digite o valor máximo para o item:\n"))
#  if valor_item_max < valor_item_min:
#    print('O valor máximo do item não pode ser inferior ao valor mínimo') 
valor_item_max = 150

#Vetor com o número do item
n_item = npy.arange(1,qtd_itens+1)

#Vetores com os pesos e valores aleatórios para cada item
peso = npy.random.randint(peso_item_min, peso_item_max, size = qtd_itens)
valor = npy.random.randint(valor_item_min, valor_item_max, size = qtd_itens)

#Definindo a população
#qtd_solucoes = int(input("Digite a quantidade de soluções:\n"))
qtd_solucoes = 8 #É a quantidade de indivíduos para o problema
populacao_tamanho = (qtd_solucoes, qtd_itens)
populacao_inicial = npy.random.randint(2, size = populacao_tamanho)
populacao_inicial = populacao_inicial.astype(int)
#Definindo o a quantidade de gerações
#qtd_geracoes = int(input("Digite a quantidade de gerações:\n"))
qtd_geracoes = 5
qtd_pais = 5

#Definindo Taxas:
crossover_taxa = 0.8
mutacao_taxa = 0.1

#Imprimindo as variáveis
print('PARAMÊTROS')
print('Peso máximo que a mochila é capaz de carregar: {}'.format(mochila_peso_max))
print('Quantidade de itens disponíveis: {}'.format(qtd_itens))
print('Peso mínimo que um item pode possuir: {}'.format(peso_item_min))
print('Peso máximo que um item pode possuir: {}'.format(peso_item_max))
print('Valor mínimo que um item pode possuir: {}'.format(valor_item_min))
print('Valor máximo que um item pode possuir: {}'.format(valor_item_max))
print('Quantidade de soluções por geração: {}'.format(qtd_solucoes))
print('Quantidade de gerações: {}'.format(qtd_geracoes))
print('Quantidade de pais: {}'.format(qtd_pais))
print('Taxa de crossover: {}'.format(crossover_taxa))
print('Taxa de mutação: {}'.format(mutacao_taxa))
print('\nLISTA DE ITENS')
print('Nº Item   Peso      Valor')
for i in range(qtd_itens):
    print('{0}          {1}         {2}'.format(n_item[i], peso[i], valor[i]))
print('\nFUNÇÃO FITNESS\nSe o somatório de (peso do item * gene) para todos os genes da solução da geração for menor ou igual ao peso máximo que a mochila pode aguentar então o fitness é igual o somatório (valor do item * gene) (peso do item * gene) para todos os genes da solução. Caso contrário o fitness é igual a 0.')
print('\nGERAÇÕES\n0 ou 1 significa se o item está presente ou não na solução de cada geração:')

def calcula_fitness(peso, valor, geracao, peso_max, n_geracao):
    fitness = npy.empty(geracao.shape[0])
    melhor_solucao = 0 
    melhor_fitness = 0
    for i in range(geracao.shape[0]):
        soma_valor = npy.sum(geracao[i] * valor)
        soma_peso = npy.sum(geracao[i] * peso)
        if soma_peso <= peso_max:
            fitness[i] = soma_valor
        else:
            fitness[i] = 0
        if melhor_fitness < fitness[i]: 
            melhor_fitness = fitness[i]
            melhor_solucao = i+1
        print('Geração {0}, Solução {1}, Fitness: {2}'.format(n_geracao+1, i+1, fitness[i]))
    print('---- A melhor solução da geração {0} foi a nº {1} ----'.format(n_geracao+1, melhor_solucao))
    return fitness.astype(int)

def selecao_roleta(fitness, qtd_pais, geracao):
    fitness_total = npy.sum(fitness)
    print ('\nSELEÇÃO ROLETA')
    print ('Fitness Total da Geração: {}'.format(fitness_total))
    print ('Fitness das soluções da geração: {}'.format(fitness))
    n_roleta = npy.empty([fitness.size])
    for i in range(fitness.size):
        n_roleta[i] = round(fitness[i]/fitness_total, 4)
    n_roleta_ordenados = npy.sort(n_roleta)
    indices_roleta_ordenados = npy.argsort(n_roleta)
    print('Porcentagem de cada solução ser escolhida na roleta: {}'.format(n_roleta))
    print('Porcentagem de cada solução ser escolhida na roleta ordenados: {}'.format(n_roleta_ordenados))
    print('Indices das solução correspondentes ordenados: {}'.format(indices_roleta_ordenados))    
    indice_selecionado_pai = 0
    pais = npy.empty((qtd_pais, geracao.shape[1])) #geracao.shape[1] é equivalente a qtd_itens
    matriz_roleta = [[0 for i in range(fitness.size)] for i in range(2)] #Matriz 2 x qtd_itens onde a primeira linha é o índice do indivíduo e a segunda o valor da porcentagem do fitness.
    i = 0
    soma_roleta = 0
    for i in range(fitness.size):
        soma_roleta += n_roleta_ordenados[i]
        matriz_roleta[0][i] = int(indices_roleta_ordenados[i])
        matriz_roleta[1][i] = soma_roleta
    print('Matriz roleta (índices das soluções x porcentagem somadas ordenadamente): {}'.format(matriz_roleta))
    i = 0
    for i in range(qtd_pais):
        sorteio_roleta = round(rd.random(),4)
        print('Nº Sorteado na roleta:{}'.format(sorteio_roleta))
        for j in range(fitness.size):
            if (j+1 <= fitness.size):
                if (sorteio_roleta > matriz_roleta[1][j] and sorteio_roleta < matriz_roleta[1][j+1]):
                    indice_selecionado_pai = matriz_roleta[0][j+1]
                    print('Índice do pai selecionado: {}'.format(indice_selecionado_pai))
                    pais[i,:] = geracao[indice_selecionado_pai, :] #recebe a linha i
    print('Pais selecionados:\n {}'.format(pais))
    return pais

def selecao_ranking(fitness, qtd_pais, geracao):
    print ('\nSELEÇÃO RANKING')
    print ('Fitness das soluções da geração: {}'.format(fitness))
    fitness_ordenados = npy.sort(fitness)[::-1]
    indices_fitness_ordenados = npy.argsort(fitness)[::-1]
    print('Fitness Ordenados Descrescentemente: {}'.format(fitness_ordenados))
    print('Indices Fitness Ordenados Decrescentemente: {}'.format(indices_fitness_ordenados))    
    indice_selecionado_pai = 0
    pais = npy.empty((qtd_pais, geracao.shape[1])) #geracao.shape[1] é equivalente a qtd_itens
    i = 0
    for i in range(qtd_pais):
        indice_selecionado_pai = indices_fitness_ordenados[i]
        print('Índice do pai selecionado: {}'.format(indice_selecionado_pai))
        pais[i,:] = geracao[indice_selecionado_pai, :] #recebe a linha i
    print('Pais selecionados:\n {}'.format(pais))
    return pais

def crossover_um_ponto(pais, qtd_filhos):
    print ('\nCROSSOVER EM UM PONTO')
    filhos = npy.empty((qtd_filhos, pais.shape[1])) #pais.shape[0] é a qtd_pais e pais.shape[1] é a qtd_items
    crossover_ponto = int(pais.shape[1]/2) #O ponto escolhido é a metade da solução
    i=0
    while (i < qtd_filhos):
        print ('------------------Cruzamento {}------------------'.format(i+1))    
        #Sorteando os pais que irão reproduzir
        pai1_idx = rd.randint(0, pais.shape[0]-1)
        pai2_idx = rd.randint(0, pais.shape[0]-1)
        while (pai2_idx == pai1_idx) and (pais.shape[0]!=1): 
            pai2_idx = rd.randint(0, pais.shape[0]-1)
        print ('Índice escolhido do pai 1: {}'.format(pai1_idx))
        print ('Índice escolhido do pai 2: {}'.format(pai2_idx))
        print ('Pai 1: {}'.format(pais[pai1_idx]))
        print ('Pai 2: {}'.format(pais[pai2_idx]))        
        sorteio_crossover = round(rd.random(),4)
        print('Taxa de crossver: {0}.  O número sorteado para crossover foi: {1}'.format(crossover_taxa,sorteio_crossover))
        if sorteio_crossover <= crossover_taxa:
            print('O crossover ocorreu!')
            filhos[i,0:crossover_ponto] = pais[pai1_idx,0:crossover_ponto]
            filhos[i,crossover_ponto:] = pais[pai2_idx,crossover_ponto:]
            print('O filho gerado é: {}'.format(filhos[i]))
        else:
            print('O crossover não ocorreu! Os genes de um dos pais continuará nos filhos')
            pai_escolhido = rd.choice([pai1_idx, pai2_idx])
            if (pai_escolhido == pai1_idx):
                filhos[i] = pais[pai1_idx]
                print('O filho herdou os genes do pai 1: {}'.format(filhos[i]))
            else:
                filhos[i] = pais[pai2_idx]
                print('O filho herdou os genes do pai 2: {}'.format(filhos[i]))          
        i = i+1
    print ('Filhos Gerados:\n {}'.format(filhos))
    return filhos    

def mutacao(filhos):
    print ('\nMUTAÇÃO NOS FILHOS')
    mutantes = npy.empty((filhos.shape))
    mutacao_taxa = 0.05
    for i in range(mutantes.shape[0]): #mutantes.shape[0] = qtd_filhos
        print ('------------------Mutação {}------------------'.format(i+1))
        mutantes[i,:] = filhos[i,:]
        print ('Filho antes da mutação: {}'.format(mutantes[i]))
        for j in range(mutantes.shape[1]): #mutantes.shape[1] = qtd_itens
            sorteio_mutacao = round(rd.random(),4)
            print('Taxa de mutação: {0}.  O número sorteado para a mutação foi: {1}'.format(mutacao_taxa,sorteio_mutacao))
            if sorteio_mutacao > mutacao_taxa:
                print ('A mutação do gene {} não ocorreu'.format(j+1))
                continue
            print ('A mutação do gene {} ocorreu'.format(j+1))
            if mutantes[i,j] == 1:
                mutantes[i,j] = 0
            else:
                mutantes[i,j] = 1
        print ('Filho depois da mutação: {}'.format(mutantes[i]))
    return mutantes   

def otimizar(peso, valor, geracao, qtd_solucoes, qtd_geracoes, qtd_pais, peso_max_mochila):
    fitness_historico = []
    qtd_filhos = qtd_solucoes - qtd_pais 
    max_fitness = 0
    for i in range(qtd_geracoes):
        print('\nGERAÇÃO {0}: \n{1}'.format(i, geracao)) 
        fitness = calcula_fitness(peso, valor, geracao, peso_max_mochila, i)
        fitness_historico.append(fitness)
        #Verificando qual o maior fitness até agorao
        if (npy.max(fitness) > max_fitness):
            max_fitness = npy.max(fitness)
        # pais = selecao_roleta(fitness, qtd_pais, geracao)
        pais = selecao_ranking(fitness, qtd_pais, geracao)
        filhos = crossover_um_ponto(pais, qtd_filhos)
        mutantes = mutacao(filhos)
        geracao[0:pais.shape[0], :] = pais
        geracao[pais.shape[0]:, :] = mutantes
    return fitness_historico

fitness_historico = otimizar(peso, valor, populacao_inicial, qtd_solucoes, qtd_geracoes, qtd_pais, mochila_peso_max)

# Geração do gráfico
fitness_media = [npy.mean(fitness) for fitness in fitness_historico]
fitness_maximo = [npy.max(fitness) for fitness in fitness_historico]
print('\n A MELHOR SOLUÇÃO ENCONTRADA TEM O FITNESS DE: {}'.format(npy.max(fitness_maximo)))
plt.plot(list(range(qtd_geracoes)), fitness_media, label = 'Fitness Médio')
plt.plot(list(range(qtd_geracoes)), fitness_maximo, label = 'Fitness Máximo')
plt.legend()
plt.title('Fitness através das gerações')
plt.xlabel('Gerações')
plt.ylabel('Fitness')
plt.show()
