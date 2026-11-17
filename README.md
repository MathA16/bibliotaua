# BiblioTauá — Livraria Web do IFCE Campus Tauá

Sistema de livraria universitária desenvolvido na disciplina de **Engenharia de Software** do curso Técnico em Informática para Internet no **IFCE Campus Tauá**.

## 📌 Visão Geral do Repositório

Este repositório contém o código-fonte base da versão estável **v0.3.0** e as branches dedicadas para cada encontro da **Sprint 04 (TASK-204: Motor de Validação e Aplicação de Cupons)**.

### 🌿 Branches Didáticas da Disciplina

- `main`: Versão base estável (v0.3.0) antes da Sprint 04.
- `aula-24`: Ponto de partida da **Aula 24** (Modelagem UML e esqueleto inicial de `exceptions.py` e `models/cupom.py`).
- `aula-25`: Ponto de partida da **Aula 25** (Persistência no SQLite e esqueleto de `repositories/cupom_repository.py`).
- `aula-26`: Ponto de partida da **Aula 26** (Orquestração do checkout, serviços e integração em `models/pedido.py`).
- `aula-27`: Ponto de partida da **Aula 27** (Garantia de Qualidade com Pytest e CLI interativo).

## 🚀 Como Iniciar

1. Faça um **Fork** deste repositório para o seu perfil no GitHub:
   - Clique no botão **Fork** no topo direito da página do GitHub.
   - Desmarque a opção *"Copy the main branch only"* para clonar todas as branches das aulas!
2. Clone o seu fork na sua máquina local:
   ```bash
   git clone https://github.com/<SEU-USUARIO>/bibliotaua.git
   cd bibliotaua
   ```
3. Configure o repositório original do professor como `upstream`:
   ```bash
   git remote add upstream https://github.com/reginaldo-pf/bibliotaua.git
   git fetch upstream
   ```
4. Navegue até a branch da aula correspondente para iniciar o desenvolvimento da etapa!
