# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:58:17 2019

@author: Douglas Violante
@author: Samuel Santos 
"""

import serial as com
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import queue

print(matplotlib.get_backend())



fig = plt.figure()
fig.canvas.draw()
plt.pause(0.001)
plt.show(block=False)



# Plota em tempo real a altitude do foguete
def altimeterPloter(value, alt):
    
    plt.plot(value,alt, 'r.')

    

# Salva os dados em um arquivo externo, a cada leitura	
def dataSafeGuard(receivedDataFloat):
    
    # Label : latitude   , Longitude  , Altitude , Date-Time, Velocidade, Direção    , Temperatura, Pressão  , Altitude2, Tempo de Execução
    # Format: Double-Grau, Double-Grau, Double-Cm, 2*uint32 , Double-m/s, Double-grau, Float-C    , Float-HPA, Float-M  , Unsigned Long-micro segundo
    
    save_filename = "EquipeRocket-Ground_ReceivedData.txt"
    
            
    file = open(save_filename, "a+")
    file.writelines(str(receivedDataFloat).strip("[").strip("]") + "\n")
        
    
    file.close()


# Implementação de testes voltado para redução de gargalo
def serialReading(comport_usb):


    serial_received = comport_usb.readline().decode('latin-1').strip()
    		
    receivedRawData = list(serial_received.split(","))
            
            
    if(len(receivedRawData) == 2):
        print(receivedRawData)
        receivedDataFloat = list(map(float, receivedRawData))

        returnFromReading.put(receivedDataFloat)
    


# Escuta a conexão serial, executado apenas uma vez
def serialConnector():

	try: 
		comport_usb = com.Serial(port = 'COM4',
								baudrate = 115200,
								timeout = 1,
								bytesize = 8,
								stopbits = 1,
								parity = 'N')
			

	except ValueError:
		print("\n Configurações de serial incorretas!")

	except IOError:
		print("\n Problemas com a porta serial, COM em uso, ou desconectada!")
		
	return comport_usb
	
# -----------------------------------------------------------------------------

def main():

    receivedDataFloat = []
    #expectedLenghtDataReceived = 2
    valueTest = 0

    #threadCriticalControl = threading.Lock()


    print("\n Equipe ROCKET - Ground Basic Station Software V2.0")
    input("\n ----------- Pressione Enter para iniciar ----------- \n")
    input("\n Tem certeza?")

    comport_usb = serialConnector()

    try:
        while(True):
    			
            
            reading = threading.Thread(name = "serialreader", target = serialReading, args = (comport_usb,))
            reading.daemon = True
            reading.start()

            receivedDataFloat = returnFromReading.get()


            safeguard = threading.Thread(name = "safeguard", target = dataSafeGuard, args = (receivedDataFloat,))
            safeguard.daemon = True
            safeguard.start()

            
            altimeter = threading.Thread(name = "altimeter", target = altimeterPloter, args = (valueTest, receivedDataFloat[0]))
            altimeter.daemon = True
            altimeter.start()

            valueTest = valueTest + 1

            fig.canvas.draw()
            plt.pause(0.0001)


    except KeyboardInterrupt:
        comport_usb.close()
        exit()	
		
			
			
if __name__ == "__main__":
    main()
