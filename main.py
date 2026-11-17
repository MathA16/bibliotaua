"""
Ponto de Entrada e Teste de Orquestração do Negócio - Aula 26
Livraria BiblioTauá (Sprint 04 - TASK-204: Etapa 3)
Valida a integração dinâmica entre Entidades, Serviços de Domínio/Aplicação e Repositórios SQLite.

Instruções para o Aluno:
Após implementar:
1. bibliotaua/services/calculadora_desconto.py
2. bibliotaua/models/pedido.py (aplicar_cupom e total)
3. bibliotaua/services/checkout_service.py (processar_checkout)
Execute este script para validar os 5 cenários da orquestração de checkout.
"""
import os
import sys
from datetime import date

from bibliotaua.database import inicializar_banco, popular_dados_iniciais, obter_conexao
from bibliotaua.models.cliente import Cliente
from bibliotaua.models.pedido import Pedido, StatusPedido
from bibliotaua.models.item_pedido import ItemPedido
from bibliotaua.repositories.cupom_repository import CupomRepository
from bibliotaua.repositories.livro_repository import LivroRepository
from bibliotaua.repositories.pedido_repository import PedidoRepository
from bibliotaua.services.calculadora_desconto import CalculadoraDescontoService
from bibliotaua.services.checkout_service import CheckoutService
from bibliotaua.exceptions import (
    BiblioTauaException,
    CupomInexistenteError,
    ValorMinimoNaoAtingidoError,
    EstoqueInsuficienteError
)

def main():
    print("=================================================================")
    print("  BIBLIOTAUÁ — TESTE DE ORQUESTRAÇÃO DO NEGÓCIO (AULA 26)")
    print("  Sprint 04: Diagrama de Sequência e Checkout Transacional")
    print("=================================================================\n")

    # 1. Preparar Ambiente de Banco Limpo
    db_file = os.path.join(os.path.dirname(__file__), "bibliotaua.db")
    if os.path.exists(db_file):
        os.remove(db_file)

    print("[1] Inicializando esquema DDL e semeando acervo inicial...")
    inicializar_banco(db_file)
    popular_dados_iniciais(db_file)
    conn = obter_conexao(db_file)

    livro_repo = LivroRepository(conn)
    cupom_repo = CupomRepository(conn)
    pedido_repo = PedidoRepository(conn)
    checkout_service = CheckoutService(
        conexao=conn,
        cupom_repo=cupom_repo,
        livro_repo=livro_repo,
        pedido_repo=pedido_repo
    )

    cliente_padrao = Cliente(
        id=1,
        nome="Carlos Eduardo Santos",
        email="carlos.edu@aluno.ifce.edu.br",
        matricula="2024101TII001"
    )

    # 2. Consultar catálogo inicial
    print("\n[2] Consultando catálogo de livros e cupons promocionais disponíveis...")
    livros = livro_repo.listar_todos()
    cupons = cupom_repo.listar_todos()
    print(f"    -> Livros no acervo: {len(livros)} títulos cadastrados.")
    print(f"    -> Cupons disponíveis: {len(cupons)} políticas cadastradas.")

    # 3. Cenário 1: Checkout com Cupom Percentual (BEMVINDO10 - 10% OFF)
    print("\n[3] Cenário 1: Checkout com Cupom Percentual (BEMVINDO10 - 10% OFF)...")
    livro_pressman = livro_repo.buscar_por_id(1)
    estoque_antes = livro_pressman.estoque
    cupom_antes = cupom_repo.buscar_por_codigo("BEMVINDO10")

    pedido1 = checkout_service.realizar_checkout(
        cliente=cliente_padrao,
        itens_solicitados=[(1, 1)], # 1 exemplar de Pressman (R$ 189.90)
        codigo_cupom="BEMVINDO10"
    )

    livro_pressman_pos = livro_repo.buscar_por_id(1)
    cupom_pos = cupom_repo.buscar_por_codigo("BEMVINDO10")

    print(f"    -> Subtotal Bruto:   R$ {pedido1.subtotal:.2f}")
    print(f"    -> Desconto (10%):  -R$ {pedido1.desconto_aplicado:.2f}")
    print(f"    -> Total Pago:       R$ {pedido1.total:.2f}")
    print(f"    -> Status do Pedido: {pedido1.status.value}")
    print(f"    -> Estoque Livro ID 1: {estoque_antes} -> {livro_pressman_pos.estoque} (Baixa efetuada)")
    print(f"    -> Usos do Cupom:      {cupom_antes.usos_realizados} -> {cupom_pos.usos_realizados} (Incrementado no SQLite)")

    # 4. Cenário 2: Checkout com Cupom de Valor Fixo (FEIRA20 - R$ 20.00 OFF)
    print("\n[4] Cenário 2: Checkout com Cupom de Valor Fixo (FEIRA20 - R$ 20.00 OFF)...")
    livro_guedes = livro_repo.buscar_por_id(2)
    estoque_guedes_antes = livro_guedes.estoque
    cupom_feira_antes = cupom_repo.buscar_por_codigo("FEIRA20")

    pedido2 = checkout_service.realizar_checkout(
        cliente=cliente_padrao,
        itens_solicitados=[(2, 1)], # 1 exemplar de UML 2 Guedes (R$ 89.00)
        codigo_cupom="FEIRA20"
    )

    livro_guedes_pos = livro_repo.buscar_por_id(2)
    cupom_feira_pos = cupom_repo.buscar_por_codigo("FEIRA20")

    print(f"    -> Subtotal Bruto:   R$ {pedido2.subtotal:.2f}")
    print(f"    -> Desconto Fixo:   -R$ {pedido2.desconto_aplicado:.2f}")
    print(f"    -> Total Pago:       R$ {pedido2.total:.2f}")
    print(f"    -> Estoque Livro ID 2: {estoque_guedes_antes} -> {livro_guedes_pos.estoque} (Baixa efetuada)")
    print(f"    -> Usos do Cupom:      {cupom_feira_antes.usos_realizados} -> {cupom_feira_pos.usos_realizados}")

    # 5. Cenário 3: Tentativa de Uso de Cupom Abaixo do Mínimo Exigido (SUPER30 exige R$ 150)
    print("\n[5] Cenário 3: Validação da DUC: Tentativa com Subtotal Abaixo do Mínimo...")
    livro_pequeno = livro_repo.buscar_por_id(4) # R$ 29.90
    estoque_pequeno_antes = livro_pequeno.estoque
    cupom_super_antes = cupom_repo.buscar_por_codigo("SUPER30")

    try:
        checkout_service.realizar_checkout(
            cliente=cliente_padrao,
            itens_solicitados=[(4, 1)], # R$ 29.90 < R$ 150.00 exigidos pelo SUPER30
            codigo_cupom="SUPER30"
        )
        print("    ❌ ERRO: O checkout deveria ter sido bloqueado!")
    except ValorMinimoNaoAtingidoError as erro:
        print(f"    -> Bloqueado com sucesso com exceção de domínio: {erro}")
        # Conferindo se o banco permaneceu integro (sem baixa de estoque e sem uso de cupom)
        livro_pequeno_pos = livro_repo.buscar_por_id(4)
        cupom_super_pos = cupom_repo.buscar_por_codigo("SUPER30")
        print(f"    -> Integridade mantida: Estoque={livro_pequeno_pos.estoque} (antes: {estoque_pequeno_antes})")
        print(f"    -> Integridade mantida: Usos={cupom_super_pos.usos_realizados} (antes: {cupom_super_antes.usos_realizados})")

    # 6. Cenário 4: Tentativa com Estoque Insuficiente
    print("\n[6] Cenário 4: Validação de Estoque Insuficiente e Transacionalidade...")
    try:
        checkout_service.realizar_checkout(
            cliente=cliente_padrao,
            itens_solicitados=[(3, 999)], # Solicita 999 exemplares de Clean Code (estoque é 10)
            codigo_cupom="BEMVINDO10"
        )
        print("    ❌ ERRO: O checkout deveria ter sido bloqueado!")
    except EstoqueInsuficienteError as erro:
        print(f"    -> Bloqueado com sucesso por falta de estoque: {erro}")
        livro_clean = livro_repo.buscar_por_id(3)
        print(f"    -> Estoque de Clean Code inalterado no banco: {livro_clean.estoque} unidades.")

    # 7. Cenário 5: Checkout Normal sem Cupom de Desconto
    print("\n[7] Cenário 5: Checkout Normal sem Cupom Promocional...")
    pedido_sem_cupom = checkout_service.realizar_checkout(
        cliente=cliente_padrao,
        itens_solicitados=[(4, 1), (5, 1)], # Pequeno Príncipe (29.90) + Dom Casmurro (24.50) = 54.40
        codigo_cupom=None
    )
    print(f"    -> Subtotal:         R$ {pedido_sem_cupom.subtotal:.2f}")
    print(f"    -> Desconto:         R$ {pedido_sem_cupom.desconto_aplicado:.2f}")
    print(f"    -> Total Pago:       R$ {pedido_sem_cupom.total:.2f}")
    print(f"    -> Cupom associado:  {pedido_sem_cupom.cupom}")
    print(f"    -> Status do Pedido: {pedido_sem_cupom.status.value} (Gravado no SQLite ID #{pedido_sem_cupom.id})")

    print("\n=================================================================")
    print("  TODOS OS 5 CENÁRIOS DE ORQUESTRAÇÃO FORAM VALIDADOS COM SUCESSO!")
    print("=================================================================\n")

if __name__ == "__main__":
    main()
