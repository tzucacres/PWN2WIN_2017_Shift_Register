# Pwn2Win 2017 – Shift Register  
Universidade Federal de São Carlos - UFSCar
Programa de Pós-Graduação em Ciência da Computação - PPGCC
Reprodução Completa do Desafio em Ambiente Docker  
Segurança Cibernética – Grupo de Estudos (UFSCar)

## Integrantes do Grupo

| Nome | RA |
|------|------|
| Arthur Hugo Barros Gaia | 846602 |
| Felipe Ivo da Silva | 824079 |
| Nathalia Cristina Santos | 795698 |
| Thiago Zucarelli Crestani | 850607 |
| Welison de Camargo Vieira | 850609 |

---

## Sobre o Desafio

Este projeto reproduz o desafio **Shift Register**, apresentado no **Pwn2Win CTF 2017**, que consiste em analisar a lógica de um ASIC fictício e recuperar a flag armazenada diretamente em silício. A solução envolve engenharia reversa de hardware, modelagem simbólica e uso do solver **Z3** para satisfazer a condição lógica `unlocked = 1`. O desafio fornece arquivos como `crap.txt`, `netlist.v` e um layout parcial do chip em `.gds2`. Estes foram utilizados para reconstruir a lógica e obter a flag. A execução foi completamente dockerizada para garantir reprodutibilidade.

---

## Flag Obtida

A execução do solver produz a seguinte saída:

sat
b'CTF-BR{A_fLaG_prINTeD_inTO_pUr3-SIlicOn}'
CTF-BR{A_fLaG_prINTeD_inTO_pUr3-SIlicOn}

---

## Arquivos do Projeto

crap.txt # Descrição simbólica do circuito
netlist.v # Netlist extraído do layout
solve3.py # Solver reescrito em Python 3
Dockerfile # Ambiente reprodutível em Docker
README.md # Este documento

---

## Funcionamento do Solver

O arquivo `solve3.py` realiza os seguintes passos:

1. Lê e interpreta `crap.txt`, contendo operações booleanas do circuito.  
2. Implementa portas lógicas como AND, OR, NAND, NOR e INV usando Z3.  
3. Cria um vetor simbólico de 320 bits (`key`).  
4. Constrói a árvore lógica até o sinal final `unlocked`.  
5. Envia ao solver Z3 a restrição `(var['unlocked'] & 1) == 1`.  
6. Converte a solução encontrada para ASCII, revelando a flag.

Exemplo de modelagem interna:

```python
key = BitVec('key', 320)
var[left] = var[a] & var[b]          # AND
var[left] = ~(var[a] | var[b])       # NOR
s = Solver()
s.add((var['unlocked'] & 1) == 1)

## Execução com Docker

## 1. Build da Imagem

docker build -t pwn2win-shiftreg .

## 2. Executar o Solver

docker run --rm pwn2win-shiftreg

## Saída Esperada

sat
CTF-BR{A_fLaG_prINTeD_inTO_pUr3-SIlicOn}

## Execução Sem Docker (opcional)

sudo apt install python3 python3-z3
python3 solve3.py

## Tecnologias Utilizadas

Python 3.11
Z3 SMT Solver
Docker
Netlist lógico em Verilog
Modelagem formal com Boolean Algebra

## Conceitos Envolvidos

Shift Register
Conjunto de flip-flops D que deslocam bits em série.
Células Lógicas OSU035.
Biblioteca aberta usada em síntese digital acadêmica.
SMT (Satisfiability Modulo Theories).
Método formal para resolver expressões booleanas complexas usando Z3.
Engenharia Reversa de Hardware.
Reconstrução do comportamento lógico a partir de artefatos de layout e netlist.

## Trecho do Dockerfile

FROM python:3.11-slim
WORKDIR /app
COPY crap.txt netlist.v solve3.py ./
RUN pip install --no-cache-dir z3-solver
CMD ["python", "solve3.py"]

## Referências

Q3K – Pwn2Win 2017 Shift Register. https://github.com/q3k/ctf/tree/master/Pwn2Win2017.
Dragon Sector – Write-up Oficial. https://blog.dragonsector.pl/2017/10/pwn2win-2017-shift-register.html.
Z3 Solver – Microsoft Research. https://github.com/Z3Prover/z3.
OSU035 – Oklahoma State University Standard Cell Library.
Weste, N.; Harris, D. CMOS VLSI Design. Addison Wesley, 2010.

## Licença

Uso acadêmico e educacional, relacionado à disciplina de Segurança Cibernética – UFSCar.
