import os
import hashlib

def calcular_hash_arquivo_completo(caminho_arquivo, tamanho_bloco=4096):
    """Calcula o hash SHA-256 de um arquivo inteiro, lendo em blocos."""
    sha256 = hashlib.sha256()
    with open(caminho_arquivo, 'rb') as f:
        # Lê o arquivo em blocos até o final
        for bloco in iter(lambda: f.read(tamanho_bloco), b""):
            sha256.update(bloco)
    return sha256.hexdigest()

def listar_arquivos_com_hash_completo(caminho_pasta, tamanho_bloco=4096):
    """Lista todos os arquivos de uma pasta e seus hashes completos."""
    arquivos_com_hash = {}
    for raiz, _, arquivos in os.walk(caminho_pasta):
        for nome_arquivo in arquivos:
            caminho_completo = os.path.join(raiz, nome_arquivo)
            hash_arquivo = calcular_hash_arquivo_completo(caminho_completo, tamanho_bloco)
            if hash_arquivo in arquivos_com_hash:
                arquivos_com_hash[hash_arquivo].append(caminho_completo)
            else:
                arquivos_com_hash[hash_arquivo] = [caminho_completo]
    return arquivos_com_hash

def comparar_pastas_diferentes(pasta1, pasta2, tamanho_bloco=4096):
    """Compara duas pastas usando o hash completo dos arquivos e lista arquivos que estão na pasta 2 e não existem ou são diferentes da pasta 1."""
    arquivos_pasta1 = listar_arquivos_com_hash_completo(pasta1, tamanho_bloco)
    arquivos_pasta2 = listar_arquivos_com_hash_completo(pasta2, tamanho_bloco)

    arquivos_diferentes = []

    # Conjuntos de hashes das duas pastas
    hash_pasta1 = set(arquivos_pasta1.keys())
    hash_pasta2 = set(arquivos_pasta2.keys())

    # Hashes que estão apenas na pasta2 (ou seja, que não existem na pasta1)
    hashes_unicos_pasta2 = hash_pasta2 - hash_pasta1

    # Listar os caminhos dos arquivos diferentes na pasta2
    for hash_arquivo in hashes_unicos_pasta2:
        caminhos_pasta2 = arquivos_pasta2[hash_arquivo]
        arquivos_diferentes.extend(caminhos_pasta2)

    # Contagem de arquivos na pasta2 e arquivos diferentes encontrados
    total_arquivos_pasta1 = sum(len(caminhos) for caminhos in arquivos_pasta1.values())
    total_arquivos_pasta2 = sum(len(caminhos) for caminhos in arquivos_pasta2.values())
    total_arquivos_diferentes = len(hashes_unicos_pasta2)

    return arquivos_diferentes, total_arquivos_pasta1, total_arquivos_pasta2, total_arquivos_diferentes

# Exemplo de uso:
pasta1 = r'D:\comparar\pastaA'
pasta2 = r'D:\comparar\pastaB'
arquivos_diferentes, total_pasta1, total_pasta2, total_diferentes = comparar_pastas_diferentes(pasta1, pasta2, tamanho_bloco=4096)

# Exibir arquivos que estão na pasta2 e são diferentes da pasta1
print("Arquivos que estão na pasta 2 e não existem ou são diferentes da pasta 1:")
for caminho in arquivos_diferentes:
    print(f"  - {caminho}")

# Exibir as contagens de arquivos
print(f"\nTotal de arquivos na pasta 1: {total_pasta1}")
print(f"Total de arquivos na pasta 2: {total_pasta2}")
print(f"Total de arquivos que são diferentes ou não existem na pasta 1: {total_diferentes}")
