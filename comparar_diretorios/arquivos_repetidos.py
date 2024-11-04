import os
import sys
import hashlib
from tqdm import tqdm

def calcular_hash_arquivo(caminho_arquivo, tamanho_bloco=4096):
    """Calcula o hash SHA-256 de um arquivo inteiro, lendo em blocos."""
    sha256 = hashlib.sha256()
    with open(caminho_arquivo, 'rb') as f:
        for bloco in iter(lambda: f.read(tamanho_bloco), b""):
            sha256.update(bloco)
    return sha256.hexdigest()

def encontrar_arquivos_repetidos(caminho_pasta, tamanho_bloco=4096):
    """Varre a pasta e encontra arquivos repetidos com base no hash SHA-256."""
    arquivos_por_hash = {}
    total_arquivos = sum(len(arquivos) for _, _, arquivos in os.walk(caminho_pasta))
    
    with tqdm(total=total_arquivos, desc="Calculando hashes dos arquivos") as pbar:
        for raiz, _, arquivos in os.walk(caminho_pasta):
            for nome_arquivo in arquivos:
                caminho_completo = os.path.join(raiz, nome_arquivo)
                hash_arquivo = calcular_hash_arquivo(caminho_completo, tamanho_bloco)
                
                if hash_arquivo in arquivos_por_hash:
                    arquivos_por_hash[hash_arquivo].append(caminho_completo)
                else:
                    arquivos_por_hash[hash_arquivo] = [caminho_completo]
                
                pbar.update(1)

    # Filtrar hashes com mais de um arquivo (arquivos repetidos)
    arquivos_repetidos = {hash: caminhos for hash, caminhos in arquivos_por_hash.items() if len(caminhos) > 1}
    
    # Contagem de grupos de arquivos repetidos
    total_grupos_repetidos = len(arquivos_repetidos)
    
    return arquivos_repetidos, total_arquivos, total_grupos_repetidos

def excluir_arquivos_repetidos(arquivos_repetidos):
    """Exclui arquivos repetidos, mantendo apenas um de cada grupo."""
    todos_sim = False
    for hash_arquivo, caminhos in arquivos_repetidos.items():
        # Manter o primeiro arquivo e percorrer o restante
        for caminho in caminhos[1:]:
            if not todos_sim:
                resposta = input(f"Deseja apagar o arquivo {caminho}? (s/n/t para sim para todos): ").strip().lower()
                if resposta == 't':
                    todos_sim = True
                elif resposta != 's':
                    print(f"Arquivo mantido: {caminho}")
                    continue

            # Excluir o arquivo
            try:
                os.remove(caminho)
                print(f"Arquivo excluído: {caminho}")
            except Exception as e:
                print(f"Erro ao excluir {caminho}: {e}")

# Exemplo de uso
if __name__ == "__main__":
    # Verificar se o caminho foi passado como argumento
    if len(sys.argv) < 2:
        print("Uso: python pesquisar_arquivos_repetidos.py 'D:/caminho/do/diretorio'")
        sys.exit(1)
    
    pasta = sys.argv[1]  # Caminho da pasta fornecido como argumento
    arquivos_repetidos, total_arquivos, total_grupos_repetidos = encontrar_arquivos_repetidos(pasta)

    # Exibir arquivos repetidos
    if arquivos_repetidos:
        print("\nArquivos repetidos encontrados:")
        for hash_arquivo, caminhos in arquivos_repetidos.items():
            print(f"\nHash: {hash_arquivo}")
            for caminho in caminhos:
                print(f"  - {caminho}")
    else:
        print("\nNenhum arquivo repetido encontrado.")

    # Exibir dados estatísticos
    print(f"\nTotal de arquivos na pasta: {total_arquivos}")
    print(f"Total de grupos de arquivos repetidos: {total_grupos_repetidos}")

    # Perguntar ao usuário se deseja excluir os arquivos repetidos
    if arquivos_repetidos:
        resposta = input("\nDeseja apagar os arquivos repetidos, mantendo apenas um de cada grupo? (s/n): ").strip().lower()
        if resposta == 's':
            excluir_arquivos_repetidos(arquivos_repetidos)
            print("\nArquivos repetidos foram excluídos, mantendo apenas um de cada grupo.")
        else:
            print("\nNenhum arquivo foi excluído.")
