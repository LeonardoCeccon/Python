import forca
import adivinhacao

def escolhe_jogo():

    print("**************************")
    print("Bem vindo ao menu de jogos")
    print("******Escolha seu jogo*****")

print("1 para forca")
print("2 para adivinhacao")

jogo = int(input("Qual jogo?"))

if(jogo == 1):
    print("Jogando forca")
    forca.jogar_forca()
elif(jogo == 2):
    print("Jogando adivinhacao")
    adivinhacao.jogar_adivinhacao()

if(__name__ == "__main__"):
    escolhe_jogo()