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
import threading


def plotInitializer():

        print(matplotlib.get_backend())

        figure = plt.figure()
        figure.canvas.draw()

        plt.title("Equipe Rocket - Altimetro")
        plt.xlabel("Time - seconds")
        plt.ylabel("Altitude - meters")
        plt.ylim(0, 1200)
        plt.pause(0.001)
        plt.show(block = False)

        return figure



def altimeterPloter(value, alt):
    
    plt.plot(value,alt, 'b|')

    

def dataSafeGuard(receivedDataFloat):
    
    # Label : latitude   , Longitude  , Altitude , Date-Time, Velocidade, Direção    , Temperatura, Pressão  , Altitude2, Tempo de Execução
    # Format: Double-Grau, Double-Grau, Double-Cm, 2*uint32 , Double-m/s, Double-grau, Float-C    , Float-HPA, Float-M  , Unsigned Long-micro segundo
    
    file = open("EquipeRocket-Ground_ReceivedData.txt", "a+")
    file.writelines(str(receivedDataFloat).strip("[").strip("]") + "\n")
        
    
    file.close()


def serialConnector():

	try: 
		comport_usb = com.Serial(port = 'COM4',
							baudrate = 115200,
							timeout = 0.5,
							bytesize = 8,
							stopbits = 1,
							parity = 'N')
			

	except ValueError:
		print("\n Configurações de serial incorretas!")

	except IOError:
		print("\n Problemas com a porta serial, COM em uso, ou desconectada!")
		
	return comport_usb


def main():

    receivedDataFloat = []
    expectedLenghtDataReceived = 2
    valueTest = 0
    
    figure = plotInitializer()
    comport_usb = serialConnector()

    threadCriticalControl = threading.Lock()
    

    print("\n Equipe ROCKET - Ground Basic Station Software V2.0")
    input("\n ----------- Pressione Enter para iniciar ----------- \n")
    input("\n Tem certeza?")

    try:
        while(True):

                

                serial_received = comport_usb.readline().decode().strip()
                receivedRawData = list(serial_received.split(","))
                comport_usb.reset_input_buffer()
            
                try:
                        if(len(receivedRawData) != expectedLenghtDataReceived):
                                continue
                        else:
                                print(receivedDataFloat)
                                receivedDataFloat = list(map(float, receivedRawData))
                except:
                        print("\n Recepção Inválida, Ignorando!")
                        continue

            
                with threadCriticalControl:
                        safeguard = threading.Thread(name = "safeguard", target = dataSafeGuard, args = (receivedDataFloat,))
                        
                        
                        if (safeguard.isAlive() != True):
                                safeguard.daemon = True
                                safeguard.start()

                        

                with threadCriticalControl:
                        altimeter = threading.Thread(name = "altimeter", target = altimeterPloter, args = (valueTest, receivedDataFloat[0]))
                        
                
                        if (altimeter.isAlive() != True):
                                altimeter.daemon = True
                                altimeter.start()

                        valueTest = valueTest + 1

                        figure.canvas.draw()
                        plt.pause(0.000001)


    except KeyboardInterrupt:
        comport_usb.close()
        exit()	
		
			
			
if __name__ == "__main__":
    main()
