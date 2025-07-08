# scripts/menu.py
import os
from scripts.eda import executar as executar_eda
from scripts.tendencias import executar as executar_tendencias
from scripts.previsao_qnt_livros import executar as executar_previsao_qnt_livros
from scripts.clustering_livros import executar as executar_clustering_livros

def menu():
    while True:
        print('\n======= Análises Livraria =======')
        print("1. Análise exploratória")
        print("2. Tendências de preço por categoria")
        print("3. Previsão de quantidade por categoria")
        print("4. Clustering")
        print("5. Sair")

        opcao = input("Escolha: de 1 a 5: ")

        try:
            if opcao == '1':
                print("\n[Análise exploratória em andamento:]")
                executar_eda()
            elif opcao == '2':
                print("\n[Analisando tendências:]")
                executar_tendencias()
            elif opcao == '3':
                print("\n[Realizando previsão para quantidade por categoria:]")
                executar_previsao_qnt_livros()
            elif opcao == '4':
                print("\n[Realizando clustering:]")
                executar_clustering_livros()
            elif opcao == '5':
                print("\n[Finalizando]")
                break
            else:
                print("\n[Erro] Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"\n❌ Erro ao executar a opção {opcao}: {e}")

if __name__ == '__main__':
    menu()
