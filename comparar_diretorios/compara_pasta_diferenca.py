import os
import hashlib

def calcular_hash_inicial_arquivo(caminho_arquivo, tamanho_bloco=4096):
    """Calcula o hash SHA-256 de um bloco inicial de um arquivo."""
    sha256 = hashlib.sha256()
    with open(caminho_arquivo, 'rb') as f:
        bloco = f.read(tamanho_bloco)
        sha256.update(bloco)
    return sha256.hexdigest()

def listar_arquivos_com_hash_inicial(caminho_pasta, tamanho_bloco=4096):
    """Lista todos os arquivos de uma pasta e seus hashes iniciais."""
    arquivos_com_hash = {}
    for raiz, _, arquivos in os.walk(caminho_pasta):
        for nome_arquivo in arquivos:
            caminho_completo = os.path.join(raiz, nome_arquivo)
            hash_arquivo = calcular_hash_inicial_arquivo(caminho_completo, tamanho_bloco)
            if hash_arquivo in arquivos_com_hash:
                arquivos_com_hash[hash_arquivo].append(caminho_completo)
            else:
                arquivos_com_hash[hash_arquivo] = [caminho_completo]
    return arquivos_com_hash

def comparar_pastas_diferentes(pasta1, pasta2, tamanho_bloco=4096):
    """Compara duas pastas usando o hash de blocos iniciais e lista arquivos que possuem conteúdo diferente."""
    arquivos_pasta1 = listar_arquivos_com_hash_inicial(pasta1, tamanho_bloco)
    arquivos_pasta2 = listar_arquivos_com_hash_inicial(pasta2, tamanho_bloco)

    arquivos_diferentes = []

    # Encontrar hashes únicos na pasta1 e pasta2
    hash_pasta1 = set(arquivos_pasta1.keys())
    hash_pasta2 = set(arquivos_pasta2.keys())

    # Hashes que estão apenas em uma das pastas
    hashes_unicos_pasta1 = hash_pasta1 - hash_pasta2
    hashes_unicos_pasta2 = hash_pasta2 - hash_pasta1

    # Listar os caminhos dos arquivos diferentes na pasta1
    for hash_arquivo in hashes_unicos_pasta1:
        caminhos_pasta1 = arquivos_pasta1[hash_arquivo]
        arquivos_diferentes.extend(caminhos_pasta1)

    # Listar os caminhos dos arquivos diferentes na pasta2
    for hash_arquivo in hashes_unicos_pasta2:
        caminhos_pasta2 = arquivos_pasta2[hash_arquivo]
        arquivos_diferentes.extend(caminhos_pasta2)

    # Contagem de arquivos em cada pasta
    total_arquivos_pasta1 = sum(len(caminhos) for caminhos in arquivos_pasta1.values())
    total_arquivos_pasta2 = sum(len(caminhos) for caminhos in arquivos_pasta2.values())
    total_arquivos_diferentes = len(hashes_unicos_pasta1) + len(hashes_unicos_pasta2)

    return arquivos_diferentes, total_arquivos_pasta1, total_arquivos_pasta2, total_arquivos_diferentes

# Exemplo de uso:
pasta1 = r'D:\teste\pasta1'
pasta2 = r'D:\teste\pasta2'
arquivos_diferentes, total_pasta1, total_pasta2, total_diferentes = comparar_pastas_diferentes(pasta1, pasta2, tamanho_bloco=4096)

# Exibir arquivos diferentes
print("Arquivos que possuem conteúdo diferente:")
for caminho in arquivos_diferentes:
    print(f"  - {caminho}")

# Exibir as contagens de arquivos
print(f"\nTotal de arquivos na pasta 1: {total_pasta1}")
print(f"Total de arquivos na pasta 2: {total_pasta2}")
print(f"Total de arquivos que possuem conteúdo diferente: {total_diferentes}")
