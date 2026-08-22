#!/usr/bin/env python3
"""
Limpa TODAS as tags (metadados) de arquivos .mp3 de uma pasta.

Depois de rodar, os arquivos ficam sem título, artista, álbum, capa, ano, etc.
Assim, a maioria dos aparelhos de som/carro passa a exibir apenas o NOME DO ARQUIVO
na tela, em vez das informações antigas.

Requisitos:
    pip install mutagen

Uso:
    python limpar_mp3.py "C:\\caminho\\da\\pasta"
    python limpar_mp3.py /caminho/da/pasta --recursivo
    python limpar_mp3.py /caminho/da/pasta --renomear "Fulano - {n:03d}"

Opções:
    --recursivo        Processa também subpastas.
    --renomear PADRAO  Renomeia os arquivos usando um padrão (ver exemplos abaixo).
    --dry-run          Mostra o que seria feito, sem alterar nada.
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3NoHeaderError
except ImportError:
    print("Erro: a biblioteca 'mutagen' não está instalada.")
    print("Instale com:  pip install mutagen")
    sys.exit(1)


def limpar_tags(caminho: Path, dry_run: bool = False) -> bool:
    """Remove todas as tags ID3 de um arquivo mp3. Retorna True se alterou algo."""
    try:
        audio = MP3(caminho)
    except Exception as e:
        print(f"  [ERRO] Não foi possível abrir {caminho.name}: {e}")
        return False

    tinha_tags = audio.tags is not None and len(audio.tags) > 0

    if not tinha_tags:
        print(f"  [OK] {caminho.name} já não tem tags.")
        return False

    if dry_run:
        print(f"  [DRY-RUN] Removeria {len(audio.tags)} tag(s) de {caminho.name}")
        return True

    try:
        audio.delete()   # remove o cabeçalho ID3 inteiro do arquivo
        audio.save()
        print(f"  [LIMPO] {caminho.name}")
        return True
    except Exception as e:
        print(f"  [ERRO] Falha ao salvar {caminho.name}: {e}")
        return False


def renomear_arquivo(caminho: Path, padrao: str, indice: int, dry_run: bool) -> Path:
    """Renomeia o arquivo conforme o padrão informado (usa {n} para o número sequencial)."""
    novo_nome = padrao.format(n=indice) + caminho.suffix
    novo_caminho = caminho.with_name(novo_nome)

    if novo_caminho.exists() and novo_caminho != caminho:
        print(f"  [AVISO] Já existe '{novo_nome}', pulando renomeação de {caminho.name}")
        return caminho

    if dry_run:
        print(f"  [DRY-RUN] Renomearia '{caminho.name}' -> '{novo_nome}'")
        return caminho

    caminho.rename(novo_caminho)
    print(f"  [RENOMEADO] '{caminho.name}' -> '{novo_nome}'")
    return novo_caminho


def main():
    parser = argparse.ArgumentParser(
        description="Remove metadados (título, artista, álbum, capa, etc.) de arquivos MP3."
    )
    parser.add_argument("pasta", help="Caminho da pasta com os arquivos .mp3")
    parser.add_argument("--recursivo", action="store_true",
                         help="Processa também as subpastas")
    parser.add_argument("--renomear", metavar="PADRAO", default=None,
                         help="Padrão para renomear os arquivos, ex: 'Faixa {n:03d}'")
    parser.add_argument("--dry-run", action="store_true",
                         help="Só mostra o que seria feito, sem alterar nada")
    args = parser.parse_args()

    pasta = Path(args.pasta).expanduser()
    if not pasta.is_dir():
        print(f"Erro: '{pasta}' não é uma pasta válida.")
        sys.exit(1)

    padrao_busca = "**/*.mp3" if args.recursivo else "*.mp3"
    arquivos = sorted(pasta.glob(padrao_busca))

    if not arquivos:
        print("Nenhum arquivo .mp3 encontrado.")
        return

    print(f"Encontrados {len(arquivos)} arquivo(s) .mp3 em '{pasta}'\n")

    alterados = 0
    for i, arquivo in enumerate(arquivos, start=1):
        print(f"Processando: {arquivo.name}")
        mudou = limpar_tags(arquivo, dry_run=args.dry_run)
        if mudou:
            alterados += 1

        if args.renomear:
            renomear_arquivo(arquivo, args.renomear, i, dry_run=args.dry_run)

        print()

    print(f"Concluído. {alterados} de {len(arquivos)} arquivo(s) tiveram tags removidas.")
    if args.dry_run:
        print("(Modo simulação — nenhum arquivo foi realmente alterado.)")


if __name__ == "__main__":
    main()
