# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:58:17 2019

@author: Douglas Violante
"""

import serial as com
import threading


# Plota em tempo real a altitude do foguete
def altimeterPloter(data):
	
    print("\n Para implementar!")    
    

# Salva os dados em um arquivo externo, a cada leitura	
def dataSafeGuard(receivedDataFloat):     
        
    # Label : latitude   , Longitude  , Altitude , Date-Time, Velocidade, Direção    , Temperatura, Pressão  , Altitude2, Tempo de Execução
    # Format: Double-Grau, Double-Grau, Double-Cm, 2*uint32 , Double-m/s, Double-grau, Float-C    , Float-HPA, Float-M  , Unsigned Long-micro segundo
    
    save_filename = "EquipeRocket-Ground_ReceivedData.txt"
    
            
    file = open(save_filename, "a+")
    

    file.writelines(str(receivedDataFloat).strip("[").strip("]") + "\r\n")
        
    
    file.close()
    
    
    
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
		print("\n Problemas com a porta serial, ou COM em uso!")
		
	return comport_usb
	
# -----------------------------------------------------------------------------

def main():

    receivedDataFloat = []
    expectedLenghtDataReceived = 2

    print("\n Equipe ROCKET - Ground Basic Station Software V2.0")
    input("\n ----------- Pressione Enter para iniciar ----------- \n")
    input("\n Tem certeza?")

    comport_usb = serialConnector()

    try:
        while(KeyboardInterrupt):
    			
            serial_received = comport_usb.readline().decode('latin-1').strip()
    		
            receivedRawData = list(serial_received.split(","))
            
            
            if(len(receivedRawData) != expectedLenghtDataReceived):
                continue
            else:
                print(receivedRawData)
                receivedDataFloat = list(map(float, receivedRawData))
    
            
            safeguard = threading.Thread(target = dataSafeGuard, args = (receivedDataFloat,))
            safeguard.start()
            
            
    except KeyboardInterrupt:
        
        comport_usb.close()
        exit()	
		
			
			
if __name__ == "__main__":
    main()
