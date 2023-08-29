#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import random
import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                   # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.

        comandos = {
            1: b'\x00\x00\x00\x00', #4 BYTES
            2: b'\x00\x00\xBB\x00', #4 BYTES
            3: b'\xBB\x00\x00',    #3 BYTES
            4: b'\x00\xBB\x00',    #3 BYTES
            5: b'\x00\x00\xBB',    #3 BYTES
            6: b'\x00\xAA',       #2 BYTES
            7: b'\xBB\x00',       #2 BYTES
            8: b'\x00',          #1 BYTE
            9: b'\xBB',          #1 BYTE
        }

        overhead = {
            'proximocomando':b'\xFF',
        }

        qntd_comandos = random.randint(10,30)
        txBuffer = b''
        for n in range(qntd_comandos):
            ncomando = random.randint(1,9)
            if n > 9:
                txBuffer += comandos[ncomando]+overhead['proximocomando']
            else:
                txBuffer += comandos[ncomando]

        print(f'qntd: {qntd_comandos}')
        print('\n')
        print(txBuffer)
        print('\n')
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
    

        print(f"Meu array de bytes tem tamanho {(len(txBuffer))} bytes")

            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        print('Comçando transmissão de dados:')
        com1.sendData(np.asarray(b'x00'))    #enviar byte de lixo
        time.sleep(.5)
        com1.sendData(np.asarray(bytes.fromhex(hex(len(txBuffer))[2:])))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
        time.sleep(.5)
        com1.sendData(np.asarray(txBuffer))          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))
        
        tempo_inicial = time.time()
        duracao_maxima = 5  # em segundos
        com1.rx.clearBuffer()
        print('Esperando byte de sacrificio')
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.05)
        recebeu = False
        while time.time() - tempo_inicial < duracao_maxima:
            if com1.rx.getBufferLen() > 0:
                rxBuffer, nRx = com1.getData(1)
                time.sleep(.05)
                recebeu = True
                #qntd_comandos=int.from_bytes(rxBuffer)
                break
            time.sleep(1)

        if recebeu:
            qntd = int.from_bytes(rxBuffer, byteorder='big')
            print(f"A quantidade de códgios que o server recebeu foi de {qntd}")
        else:
            print('\n')
            print("error: TIME OUT")
            print('\n')
        
        
        print('\n')
        print(rxBuffer)
        print('\n')
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
