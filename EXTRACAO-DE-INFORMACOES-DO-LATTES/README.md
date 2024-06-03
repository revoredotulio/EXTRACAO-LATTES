
# Projeto de Extração de Informações do Currículo Lattes

Este repositório contém diversos scripts em Python para extrair informações do Currículo Lattes. Abaixo estão listados os scripts com suas respectivas descrições.

## Estrutura do Projeto

EXTRAÇÃO-DE-INFORMAÇÕES-DO-LATTES/
├── scripts/
│ ├── extracao_artigos.py
│ ├── extracao_cap_livro.py
│ ├── extracao_disciplinas.py
│ ├── extracao_livros.py
│ ├── extracao_orientacoes.py
│ ├── extracao_outras_publicacoes.py
│ ├── extracao_producao_tecnica.py
│ └── extracao_projetos_pesquisa.py
├── docs/
│ └── additional_documentation.md
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py


## Requisitos

- Python 3.x

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/revoredotulio/EXTRACAO-DE-INFORMACOES-DO-LATTES.git
    cd EXTRACAO-DE-INFORMACOES-DO-LATTES
    ```

2. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

1. Navegue até o diretório `scripts`:
    ```sh
    cd scripts
    ```

2. Execute o script desejado, por exemplo, para extrair artigos:
    ```sh
    python extracao_artigos.py
    ```

## Exemplos

### Extração de Artigos

Execute `extracao_artigos.py` para extrair informações sobre artigos publicados. O script irá carregar os dados do Currículo Lattes e processar as informações para exibir uma tabela com os artigos.

### Extração de Capítulos de Livro

Execute `extracao_cap_livro.py` para extrair informações sobre capítulos de livros. O script irá carregar os dados do Currículo Lattes e processar as informações para exibir uma tabela com os capítulos de livros.

## Contribuições

Sinta-se à vontade para contribuir com melhorias ou novas funcionalidades. Para isso, siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma branch para suas alterações:
    ```sh
    git checkout -b minha-branch
    ```
3. Faça commit das suas alterações:
    ```sh
    git commit -m "Minha contribuição"
    ```
4. Faça push para a branch:
    ```sh
    git push origin minha-branch
    ```
5. Abra um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Se você tiver alguma dúvida ou sugestão, sinta-se à vontade para abrir uma issue ou entrar em contato comigo.

---

**Observação**: Este projeto é uma demonstração de como extrair informações do Currículo Lattes utilizando Python. Certifique-se de ajustar os scripts de acordo com suas necessidades específicas.
