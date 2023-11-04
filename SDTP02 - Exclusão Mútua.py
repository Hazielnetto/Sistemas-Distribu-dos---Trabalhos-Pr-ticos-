
import threading
import random
import time

class GerenciadorDeProcessos:
    def __init__(self, intervalo, tempo_de_processamento_minimo, 
                 tempo_de_processamento_maximo, 
                 intervalo_de_consumo_minimo, 
                 intervalo_de_consumo_maximo):
        
        self.intervalo = intervalo
        self.tempo_de_processamento_minimo = tempo_de_processamento_minimo
        self.tempo_de_processamento_maximo = tempo_de_processamento_maximo
        self.intervalo_de_consumo_minimo = intervalo_de_consumo_minimo
        self.intervalo_de_consumo_maximo = intervalo_de_consumo_maximo
        self.coordenador_vivo = True
        self.fila_viva = True
        self.processos = {}
        self.ultimo_id = 0        

    def gerar_id(self):        
            novo_id = random.randint(1, 1000000)
            while novo_id in self.processos:
                novo_id = random.randint(1, 1000000)
            return novo_id

    def criar_processo(self):        
        id_do_processo = self.gerar_id()
        tempo_de_processamento = random.uniform(self.tempo_de_processamento_minimo, 
                                                self.tempo_de_processamento_maximo)
        
        intervalo_de_consumo = random.uniform(self.intervalo_de_consumo_minimo, 
                                            self.intervalo_de_consumo_maximo)
        
        processo = threading.Thread(target=self.executar_processo, args=(id_do_processo, 
                                                                        tempo_de_processamento, 
                                                                        intervalo_de_consumo))
        processo.start()
        self.processos[id_do_processo] = processo 
        print(f'Processo {id_do_processo} criado')  

    def executar_processo(self, id_do_processo, 
                          tempo_de_processamento, 
                          intervalo_de_consumo):
        while True:
            if not self.coordenador_vivo:
                break
            time.sleep(intervalo_de_consumo)
            if not self.coordenador_vivo:
                break
            print(f'Processando recurso pelo processo {id_do_processo}...')
            time.sleep(tempo_de_processamento)

    def iniciar(self):
        while True:
            time.sleep(self.intervalo)
            if not self.coordenador_vivo:
                break
            print('Coordenador morreu.')
            self.coordenador_vivo = False
            print('Interrompendo a fila...')
            self.fila_viva = False                        
            for id_do_processo in list(self.processos.keys()):
                processo = self.processos[id_do_processo]
                processo.join()
                del self.processos[id_do_processo]
            quit(0)
            

    def iniciar_geracao_de_processos(self):
        while True:
            if not self.coordenador_vivo:
                break           
            print('Criando novo processo...')
            self.criar_processo()            
            time.sleep(40)

print(f'Iniciando threads...')
gerenciador = GerenciadorDeProcessos(60, 5, 15, 10, 25)
gerenciador_thread = threading.Thread(target=gerenciador.iniciar)
gerenciador_thread.start()
gerenciador.iniciar_geracao_de_processos()
