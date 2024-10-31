import os
import hashlib
from tqdm import tqdm

def calcular_hash_arquivo_completo(caminho_arquivo, tamanho_bloco=4096):
    """Calcula o hash SHA-256 de um arquivo inteiro, lendo em blocos."""
    sha256 = hashlib.sha256()
    with open(caminho_arquivo, 'rb') as f:
        for bloco in iter(lambda: f.read(tamanho_bloco), b""):
            sha256.update(bloco)
    return sha256.hexdigest()

def listar_arquivos_com_hash_completo(caminho_pasta, tamanho_bloco=4096):
    """Lista todos os arquivos de uma pasta e seus hashes completos, com barra de progresso."""
    arquivos_com_hash = {}
    total_arquivos = sum(len(arquivos) for _, _, arquivos in os.walk(caminho_pasta))
    
    with tqdm(total=total_arquivos, desc=f"Calculando hashes em {caminho_pasta}") as pbar:
        for raiz, _, arquivos in os.walk(caminho_pasta):
            for nome_arquivo in arquivos:
                caminho_completo = os.path.join(raiz, nome_arquivo)
                hash_arquivo = calcular_hash_arquivo_completo(caminho_completo, tamanho_bloco)
                if hash_arquivo in arquivos_com_hash:
                    arquivos_com_hash[hash_arquivo].append(caminho_completo)
                else:
                    arquivos_com_hash[hash_arquivo] = [caminho_completo]
                pbar.update(1)
    
    return arquivos_com_hash

def comparar_pastas_diferentes(pasta1, pasta2, tamanho_bloco=4096):
    """Compara duas pastas e lista arquivos exclusivos de cada uma delas, e a quantidade de arquivos iguais."""
    arquivos_pasta1 = listar_arquivos_com_hash_completo(pasta1, tamanho_bloco)
    arquivos_pasta2 = listar_arquivos_com_hash_completo(pasta2, tamanho_bloco)

    arquivos_exclusivos_pasta1 = []
    arquivos_exclusivos_pasta2 = []

    # Conjuntos de hashes das duas pastas
    hash_pasta1 = set(arquivos_pasta1.keys())
    hash_pasta2 = set(arquivos_pasta2.keys())

    # Identificar arquivos exclusivos de cada pasta
    hashes_exclusivos_pasta1 = hash_pasta1 - hash_pasta2
    hashes_exclusivos_pasta2 = hash_pasta2 - hash_pasta1

    for hash_arquivo in hashes_exclusivos_pasta1:
        caminhos_pasta1 = arquivos_pasta1[hash_arquivo]
        arquivos_exclusivos_pasta1.extend(caminhos_pasta1)
    
    for hash_arquivo in hashes_exclusivos_pasta2:
        caminhos_pasta2 = arquivos_pasta2[hash_arquivo]
        arquivos_exclusivos_pasta2.extend(caminhos_pasta2)

    # Ordenar arquivos exclusivos por caminho completo, priorizando a estrutura de diretório e nome
    arquivos_exclusivos_pasta1.sort(key=lambda x: (os.path.dirname(x), os.path.basename(x)))
    arquivos_exclusivos_pasta2.sort(key=lambda x: (os.path.dirname(x), os.path.basename(x)))

    # Contagem de arquivos em cada pasta e arquivos exclusivos
    total_arquivos_pasta1 = sum(len(caminhos) for caminhos in arquivos_pasta1.values())
    total_arquivos_pasta2 = sum(len(caminhos) for caminhos in arquivos_pasta2.values())
    total_exclusivos_pasta1 = len(arquivos_exclusivos_pasta1)
    total_exclusivos_pasta2 = len(arquivos_exclusivos_pasta2)

    # Contagem de arquivos iguais (presentes em ambas as pastas com o mesmo hash)
    arquivos_iguais = hash_pasta1 & hash_pasta2
    total_arquivos_iguais = sum(min(len(arquivos_pasta1[hash]), len(arquivos_pasta2[hash])) for hash in arquivos_iguais)

    return (arquivos_exclusivos_pasta1, arquivos_exclusivos_pasta2, 
            total_arquivos_pasta1, total_arquivos_pasta2, 
            total_exclusivos_pasta1, total_exclusivos_pasta2, 
            total_arquivos_iguais)

# Exemplo de uso:
pasta1 = r'D:\comparar\pastaA'
pasta2 = r'D:\comparar\pastaB'
(
    arquivos_exclusivos_pasta1, arquivos_exclusivos_pasta2, 
    total_pasta1, total_pasta2, 
    total_exclusivos_pasta1, total_exclusivos_pasta2, 
    total_arquivos_iguais
) = comparar_pastas_diferentes(pasta1, pasta2, tamanho_bloco=4096)

# Exibir relatórios ordenados
print("Arquivos exclusivos na pasta 1 (ordenados por diretório e nome):")
for caminho in arquivos_exclusivos_pasta1:
    print(f"  - {caminho}")

print("\nArquivos exclusivos na pasta 2 (ordenados por diretório e nome):")
for caminho in arquivos_exclusivos_pasta2:
    print(f"  - {caminho}")

# Exibir as contagens de arquivos
print(f"\nTotal de arquivos na pasta 1: {total_pasta1}")
print(f"Total de arquivos na pasta 2: {total_pasta2}")
print(f"Total de arquivos exclusivos na pasta 1: {total_exclusivos_pasta1}")
print(f"Total de arquivos exclusivos na pasta 2: {total_exclusivos_pasta2}")
print(f"Total de arquivos iguais entre as duas pastas: {total_arquivos_iguais}")
