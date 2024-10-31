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

def comparar_pastas(pasta1, pasta2, tamanho_bloco=4096):
    """Compara duas pastas usando o hash de blocos iniciais e lista arquivos que possuem o mesmo conteúdo."""
    arquivos_pasta1 = listar_arquivos_com_hash_inicial(pasta1, tamanho_bloco)
    arquivos_pasta2 = listar_arquivos_com_hash_inicial(pasta2, tamanho_bloco)

    arquivos_iguais = []

    # Comparar hashes das duas pastas
    for hash_arquivo, caminhos_pasta1 in arquivos_pasta1.items():
        if hash_arquivo in arquivos_pasta2:
            caminhos_pasta2 = arquivos_pasta2[hash_arquivo]
            arquivos_iguais.append((caminhos_pasta1, caminhos_pasta2))

    # Contagem de arquivos em cada pasta
    total_arquivos_pasta1 = sum(len(caminhos) for caminhos in arquivos_pasta1.values())
    total_arquivos_pasta2 = sum(len(caminhos) for caminhos in arquivos_pasta2.values())
    total_arquivos_iguais = len(arquivos_iguais)

    return arquivos_iguais, total_arquivos_pasta1, total_arquivos_pasta2, total_arquivos_iguais

# Exemplo de uso:
pasta1 = r'D:\teste\pasta1'
pasta2 = r'D:\teste\pasta2'
arquivos_iguais, total_pasta1, total_pasta2, total_iguais = comparar_pastas(pasta1, pasta2, tamanho_bloco=4096)

# Exibir arquivos com o mesmo conteúdo
for caminhos_pasta1, caminhos_pasta2 in arquivos_iguais:
    print("Arquivos com o mesmo conteúdo encontrados:")
    print("Na pasta 1:")
    for caminho in caminhos_pasta1:
        print(f"  - {caminho}")
    print("Na pasta 2:")
    for caminho in caminhos_pasta2:
        print(f"  - {caminho}")
    print()

# Exibir as contagens de arquivos
print(f"Total de arquivos na pasta 1: {total_pasta1}")
print(f"Total de arquivos na pasta 2: {total_pasta2}")
print(f"Total de arquivos que coincidem: {total_iguais}")
