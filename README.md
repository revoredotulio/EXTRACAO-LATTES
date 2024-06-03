
# EXTRACAO-LATTES

Projeto desenvolvido para extração de grandes volumes de currículos Lattes.

## Índice
- [Sobre o Projeto](#sobre-o-projeto)
- [Estrutura dos Arquivos](#estrutura-dos-arquivos)
- [Requisitos do Projeto](#requisitos-do-projeto)
- [Instruções de Instalação](#instruções-de-instalação)
- [Como Utilizar](#como-utilizar)
- [Exemplos de Uso](#exemplos-de-uso)
- [Problemas Comuns e Soluções](#problemas-comuns-e-soluções)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## Sobre o Projeto

Este projeto foi desenvolvido para facilitar a extração de informações de currículos Lattes, abrangendo diversas categorias de dados acadêmicos e científicos. A extração automatizada permite a coleta eficiente de grandes volumes de dados, útil para análise acadêmica, criação de bases de dados e outras aplicações.

## Estrutura dos Arquivos

Este repositório contém scripts para a extração de diversas informações de currículos Lattes. Abaixo está a descrição de cada arquivo:

- **EXTRAÇÃO DE ARTIGOS.py**: Script para extração de artigos de periódicos.
- **EXTRAÇÃO DE CAP DE LIVRO.py**: Script para extração de capítulos de livros.
- **EXTRAÇÃO DE DISCIPLINAS.py**: Script para extração de disciplinas ministradas.
- **EXTRAÇÃO DE LIVROS.py**: Script para extração de livros publicados.
- **EXTRAÇÃO DE ORIENTAÇÕES.py**: Script para extração de orientações de alunos.
- **EXTRAÇÃO DE OUTRAS PUBLICAÇÕES.py**: Script para extração de outras publicações.
- **EXTRAÇÃO DE PRODUÇÃO TÉCNICA.py**: Script para extração de produções técnicas.
- **EXTRAÇÃO DE PROJETOS DE PESQUISA.py**: Script para extração de projetos de pesquisa.

## Requisitos do Projeto

Certifique-se de ter as seguintes bibliotecas Python instaladas:
- requests
- pandas
- BeautifulSoup
- lxml

Você pode instalar as dependências necessárias usando o comando:

pip install -r requirements.txt


## Instruções de Instalação

1. Clone o repositório para sua máquina local:
 
    git clone https://github.com/revoredotulio/EXTRACAO-LATTES.git


2. Navegue até o diretório do repositório:

    cd EXTRACAO-LATTES


3. Instale as dependências necessárias:

    pip install -r requirements.txt


## Como Utilizar

Cada script é independente e pode ser executado separadamente. Para executar um script, utilize o Python seguido do nome do arquivo. Por exemplo, para executar o script de extração de artigos, utilize:

python EXTRAÇÃO DE ARTIGOS.py


## Exemplos de Uso

### Extração de Artigos

Para extrair artigos de currículos Lattes, execute o seguinte comando:

python EXTRAÇÃO DE ARTIGOS.py

### Extração de Capítulos de Livro

Para extrair capítulos de livros de currículos Lattes, execute o seguinte comando:

python EXTRAÇÃO DE CAP DE LIVRO.py

### Extração de Disciplinas Ministradas

Para extrair disciplinas ministradas de currículos Lattes, execute o seguinte comando:

python EXTRAÇÃO DE DISCIPLINAS.py


### Extração de Livros Publicados

Para extrair livros publicados de currículos Lattes, execute o seguinte comando:

python EXTRAÇÃO DE LIVROS.py

### Extração de Orientações

Para extrair orientações de alunos de currículos Lattes, execute o seguinte comando:

python EXTRAÇÃO DE ORIENTAÇÕES.py

### Extração de Outras Publicações

Para extrair outras publicações de currículos Lattes, execute o seguinte comando:

python EXTRAÇÃO DE OUTRAS PUBLICAÇÕES.py

### Extração de Produções Técnicas

Para extrair produções técnicas de currículos Lattes, execute o seguinte comando:

python EXTRAÇÃO DE PRODUÇÃO TÉCNICA.py

### Extração de Projetos de Pesquisa

Para extrair projetos de pesquisa de currículos Lattes, execute o seguinte comando:

python EXTRAÇÃO DE PROJETOS DE PESQUISA.py

## Problemas Comuns e Soluções

### Problema: Erro de Conexão
**Solução**: Verifique sua conexão com a internet e certifique-se de que o servidor do Lattes está acessível.

### Problema: Erro de Autenticação
**Solução**: Verifique suas credenciais e certifique-se de que você tem permissão para acessar os dados necessários.

### Problema: Dependência Não Encontrada
**Solução**: Certifique-se de que todas as bibliotecas necessárias estão instaladas corretamente usando o comando `pip install -r requirements.txt`.

## Contribuindo

Para contribuir com este projeto, por favor siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça o push para a branch (`git push origin feature/nova-feature`).
5. Crie um novo Pull Request.

## Licença

Este projeto está licenciado sob os termos da licença MIT. Veja o arquivo LICENSE para mais detalhes.
