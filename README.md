# 🏷️ Chaveiro 3D Python

Bem-vindo ao **Chaveiro 3D Python**! Este projeto é uma ferramenta poderosa e simples para gerar modelos 3D de placas de identificação e chaveiros personalizados, prontos para impressão 3D multicor.

---

## 🚀 O que este projeto faz?

Este projeto automatiza a criação de arquivos `.3mf` (3D Manufacturing Format) para chaveiros. Ele permite que você insira uma lista de nomes e sobrenomes e gera automaticamente modelos 3D com:

* **Base Sólida**: O corpo principal do chaveiro.
* **Contorno (Rim)**: Uma borda elevada para acabamento estético.
* **Texto em Relevo**: Nome e sobrenome modelados geometricamente.
* **Multimaterial**: As partes são separadas logicamente para facilitar a impressão com duas cores (ex: base de uma cor, texto e borda de outra).

Ideal para quem possui impressoras 3D e deseja produzir brindes, etiquetas ou identificadores personalizados em massa!

---

## 📂 Estrutura do Projeto

Aqui estão os arquivos principais que fazem a mágica acontecer:

| Arquivo | Descrição |
| :--- | :--- |
| `generate_nameplates.ipynb` | 📓 **O Cérebro**: Um Jupyter Notebook interativo onde você insere os dados, escolhe as cores e gera os arquivos. |
| `nameplate_utils.py` | 🛠️ **O Motor**: Contém toda a lógica de modelagem 3D usando a biblioteca `build123d`. Define geometria, extrusões e exportação. |

---

## 🛠️ Dependências e Requisitos

Para rodar este projeto, você precisará de **Python 3.10+** e das seguintes bibliotecas:

* **[build123d](https://github.com/gumyr/build123d)**: Para a modelagem CAD paramétrica via código.
* **ipykernel**: Para executar o notebook Jupyter.
* **tkinter**: (Geralmente nativo no Python) Para a janela de seleção de pasta.

### Instalação Rápida

Você pode instalar as dependências principais executando o comando abaixo ou rodando a primeira célula do notebook:

```bash
pip install build123d ipykernel
```

---

## 🎨 Como Usar

1. **Abra o Notebook**: Inicie o arquivo `generate_nameplates.ipynb` no seu editor favorito (VS Code, JupyterLab, etc).
2. **Execute as Células**:
    * Rode a célula de **instalação** (se for a primeira vez).
    * Rode a célula de **importação** das bibliotecas.
    * Rode a função `main()`.
3. **Interaja**:
    * Digite a quantidade de placas (1 a 5).
    * Para cada placa, insira o **Nome** (texto maior) e o **Sobrenome** (texto menor, opcional).
    * Escolha um esquema de **Cores** pré-definido (ex: Azul e Branco, Vermelho e Amarelo).
4. **Salve**:
    * Uma janela abrirá pedindo para selecionar a pasta de destino.
    * Os arquivos `.3mf` serão gerados automaticamente lá!

---

## 🌈 Esquemas de Cores Disponíveis

O gerador já vem com combinações testadas para garantir alto contraste na impressão:

* 🔵 **Azul & Branco**
* 🔴 **Vermelho & Amarelo**
* ⚫ **Preto & Branco**
* 🟢 **Verde & Preto**
* ⚪ **Branco & Preto**
* 🟠 **Laranja & Azul**

---

*Desenvolvido para facilitar a vida de makers e entusiastas da impressão 3D!* 🖨️✨
