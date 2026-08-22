limpar_mp3.py
Script em Python para remover metadados (tags ID3) de arquivos .mp3, fazendo com que aparelhos de som exibam apenas o nome do arquivo em vez do título/artista/álbum gravados nas tags.
O intuito é auxiliar a quem utiliza fixas mixadas no qual os responsáveis alteram e colocam tags genéricas ao invés dos da faixa, dificultando assim saber o que está sendo reproduzido.


O que ele faz?
Cada arquivo MP3 pode carregar um bloco de metadados chamado ID3 com informações como:

Título da faixa
Artista(s)
Álbum
Ano
Capa (imagem)
Gênero, faixa número, compositor, etc.

Quando esse bloco existe, a maioria dos aparelhos de som (carro, rádio, caixa de som) prioriza exibir essas informações na tela. O script remove o bloco ID3 inteiro do arquivo, deixando só o áudio puro. Sem esse bloco, os aparelhos caem no fallback padrão: mostrar o nome do arquivo.
O áudio em si nunca é alterado — apenas os metadados.


Requisitos
Python 3.8 ou superior
Biblioteca mutagen

Instalação da dependência:

pip install mutagen

Uso básico
python limpar_mp3.py "CAMINHO_DA_PASTA"

Isso processa apenas os arquivos .mp3 que estão diretamente dentro da pasta indicada (não entra em subpastas).
Exemplo
python limpar_mp3.py "D:\Musicas\01 Viral TikTok"


Opções (parâmetros)
Parâmetro
O que faz
--recursivo
Entra em todas as subpastas, em qualquer nível, e processa os MP3s de cada uma.
--dry-run
Modo simulação: mostra o que seria feito, sem alterar nenhum arquivo de verdade. Útil para conferir antes.
--renomear "PADRAO"
Renomeia os arquivos seguindo um padrão com numeração sequencial. Ver seção abaixo.

Combinando opções
As opções podem ser usadas juntas:

python limpar_mp3.py "CAMINHO" --recursivo --dry-run


Detalhes de cada opção
--recursivo
Sem essa flag, o script busca com o padrão *.mp3 (só a pasta indicada). Com essa flag, ele busca com **/*.mp3, que varre qualquer profundidade de subpastas.

python limpar_mp3.py "CAMINHO" --recursivo

Processa os 3 arquivos acima, não importa em qual subpasta estejam.
--dry-run
Não apaga nem renomeia nada — só imprime no terminal o que aconteceria. Recomendado sempre rodar primeiro com essa flag antes de aplicar de verdade, especialmente em pastas grandes.
--renomear "PADRAO"
Renomeia cada arquivo processado usando um padrão com {n} (número sequencial, começando em 1, na ordem em que os arquivos foram encontrados).

Exemplos de padrão: | Padrão | Resultado | |---|---| | "Faixa {n}" | Faixa 1.mp3, Faixa 2.mp3, ... | | "Faixa {n:03d}" | Faixa 001.mp3, Faixa 002.mp3, ... | | "Rhyan CDs - {n:02d}" | Rhyan CDs - 01.mp3, Rhyan CDs - 02.mp3, ... |

⚠️ A numeração é global: se usar --recursivo, ela não reinicia a cada subpasta, continua contando em sequência por todos os arquivos encontrados.

⚠️ Se já existir um arquivo com o nome de destino, o script pula a renomeação daquele arquivo (evita sobrescrever por engano) e avisa no terminal.

Se você não passar --renomear, o script não renomeia nada — só limpa as tags, mantendo o nome original de cada arquivo.


O que aparece no terminal
Para cada arquivo processado, uma destas mensagens:

Mensagem
Significado
[LIMPO] nome.mp3
Tags removidas com sucesso
[OK] nome.mp3 já não tem tags.
Arquivo já estava sem metadados, nada a fazer
[ERRO] ...
Algo impediu a leitura ou gravação do arquivo (arquivo corrompido, sem permissão, etc.)
[RENOMEADO] 'antigo' -> 'novo'
Só aparece se --renomear foi usado
[AVISO] Já existe '...'
Renomeação pulada por já existir um arquivo com esse nome
[DRY-RUN] ...
Só aparece em modo simulação, mostrando o que seria feito


No final, um resumo:

Concluído. 18 de 18 arquivo(s) tiveram tags removidas.


Perguntas frequentes
Isso apaga a música ou só os dados escritos nela? Só os metadados (ID3). O áudio não é tocado.

Dá pra desfazer depois? Não — a remoção é definitiva. Se quiser manter uma cópia de segurança com as tags originais, faça backup da pasta antes de rodar o script.

Funciona em qualquer MP3? Sim, desde que o arquivo seja um MP3 válido. Arquivos corrompidos ou que não sejam realmente MP3 (apesar da extensão) vão aparecer como [ERRO].

Por que "Nenhum arquivo .mp3 encontrado"? Geralmente é porque os MP3s estão dentro de subpastas e você esqueceu o --recursivo, ou o caminho da pasta está errado/com erro de digitação.

Preciso rodar de novo depois de adicionar MP3s novos? Sim. O script só processa os arquivos que existem na hora em que ele roda. Arquivos adicionados depois precisam de uma nova execução.
