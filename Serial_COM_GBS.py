# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:58:17 2019

@author: Douglas Violante
"""

import serial as com



def altimeterPlotting():
	
	print("\n Para Implementar")
    

    
def altimeterFileBackup():                # Salva os dados em um arquivo externo
    
    print("\n Para Implementar"); 
    

# -----------------------------------------------------------------------------

def main():

	print("\n Equipe ROCKET - Ground Telemetry Software V1.0")
	input("\n ---------- Pressione Enter para iniciar ----------")

	try: 
		comport = com.Serial(port = 'COM4',
								baudrate = 9600,
								timeout = 1,
								bytesize = 8,
								stopbits = 1,
								parity = 'N')                   # Não Alterar - Valor geralmente setado observando o baudrate
		
		if(comport.isOpen()):
			end = True
		

	except ValueError:
		print("\n Configurações de serial incorretas!")

	except IOError:
		print("\n Problemas com a porta serial, ou COM em uso!")

	else:
		
		while(end != False):           # ATENÇÃO ! Alterar
			
			value_comport = comport.readline().decode('latin-1').strip() # Decodifica Bytes em String no Padrão Latin-1
			
			if(value_comport.isdigit()):    # Checa se o conteúdo da string contém apenas números
				
				value  = int(value_comport)		# Converte o conteúdo de value_comport para Int
				
				print(value)
				
				if(value <= 1):			# Condição para testes
					
					end = False
					comport.close()		# Fecha porta serial
			
			
if __name__ == "__main__":
    main()




# =========================================================================================================================== #
# Instruções para cálculo de timeout se necessário, sabendo que baudrate indica "bits por segundo",							  #
# pelo exemplo se faz, 																										  #
# 																															  #
# baudrate = 9600 e bytesize = 8 bits, então 9600 / 8 = 1200, logo para se enviar um byte será necessário o 				  #
# tempo de 1 / 1200 = 0.00083 segundos, logo um arquivo de 16kb precisa de 16 * 0.000883 = 0.01328 segundos, atrasos		  #
# acima deste tempo devem ser observados, caso o arquivo seja sensível. 													  #
# 																															  #
# =========================================================================================================================== #

    

