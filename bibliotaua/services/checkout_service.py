"""
Serviço de Aplicação: CheckoutService (TASK-204)
Orquestra o fluxo de fechamento da compra, integrando validação de regras de cupom,
abatimento no pedido, baixa de estoque e persistência relacional transacional no SQLite.

Instruções para o Aluno (Aula 26):
Consulte os Slides 16 a 20 e o guia_desenvolvedor.md para implementar:
1. Construtor com inicialização dos repositórios
2. Método processar_checkout(pedido, codigo_cupom)
3. Método de conveniência realizar_checkout(cliente, itens_solicitados, codigo_cupom)
"""
import sqlite3
from typing import List, Tuple, Optional

from bibliotaua.models.cliente import Cliente
from bibliotaua.models.livro import Livro
from bibliotaua.models.item_pedido import ItemPedido
from bibliotaua.models.pedido import Pedido, StatusPedido
from bibliotaua.models.cupom import Cupom
from bibliotaua.repositories.cupom_repository import CupomRepository
from bibliotaua.repositories.livro_repository import LivroRepository
from bibliotaua.repositories.pedido_repository import PedidoRepository
from bibliotaua.services.calculadora_desconto import CalculadoraDescontoService
from bibliotaua.exceptions import CupomInexistenteError

class CheckoutService:
    """
    Serviço orquestrador de checkout.
    Coordena chamadas entre entidades de domínio e repositórios de dados no SQLite.
    """

    def __init__(
        self,
        conexao: Optional[sqlite3.Connection] = None,
        cupom_repo: Optional[CupomRepository] = None,
        livro_repo: Optional[LivroRepository] = None,
        pedido_repo: Optional[PedidoRepository] = None
    ):
        """
        TODO: [ALUNO - TAREFA 3.1]
        Inicializa os repositórios a partir da conexão SQLite fornecida ou dos parâmetros:
        - self.conn
        - self.cupom_repo
        - self.livro_repo
        - self.pedido_repo
        """
        if conexao is not None:
            self.conn = conexao
            self.cupom_repo = cupom_repo or CupomRepository(conexao)
            self.livro_repo = livro_repo or LivroRepository(conexao)
            self.pedido_repo = pedido_repo or PedidoRepository(conexao)
        elif cupom_repo and livro_repo and pedido_repo:
            self.cupom_repo = cupom_repo
            self.livro_repo = livro_repo
            self.pedido_repo = pedido_repo
            self.conn = cupom_repo.conn
        else:
            raise ValueError("Forneça conexao ativa ou a tríade de repositórios.")

    def processar_checkout(
        self,
        pedido: Pedido,
        codigo_cupom: Optional[str] = None
    ) -> Pedido:
        """
        TODO: [ALUNO - TAREFA 3.2]
        Implementar as 4 etapas do Diagrama de Sequência UML:
        1. Se codigo_cupom informado:
           - cupom = self.cupom_repo.buscar_por_codigo(codigo_cupom)
           - se not cupom -> raise CupomInexistenteError(codigo_cupom)
           - pedido.aplicar_cupom(cupom)
        2. Debita estoque de cada livro no pedido:
           - for item in pedido.itens: item.livro.debitar_estoque(item.quantidade)
        3. Bloco transacional atômico (with self.conn):
           - Atualiza estoques no SQLite: self.livro_repo.atualizar_estoque(item.livro.id, item.livro.estoque)
           - Registra uso do cupom se aplicado: self.cupom_repo.registrar_uso(cupom.codigo)
           - Define status: pedido.status = StatusPedido.PAGO
           - Grava o pedido: self.pedido_repo.salvar(pedido)
        4. Retorna o pedido finalizado.
        (Consulte os Slides 18 e 19 do Beamer)
        """
        raise NotImplementedError("TODO: Implementar CheckoutService.processar_checkout()")

    def realizar_checkout(
        self,
        cliente: Cliente,
        itens_solicitados: List[Tuple[int, int]], # Lista de (livro_id, quantidade)
        codigo_cupom: Optional[str] = None
    ) -> Pedido:
        """
        Método de conveniência de alto nível:
        Recupera os livros pelo ID, monta a lista de itens e delega para processar_checkout.
        """
        itens_pedido: List[ItemPedido] = []

        for livro_id, qtd in itens_solicitados:
            livro = self.livro_repo.buscar_por_id(livro_id)
            if not livro:
                raise ValueError(f"Livro com ID {livro_id} não encontrado no acervo.")
            itens_pedido.append(ItemPedido(livro=livro, quantidade=qtd, preco_unitario=livro.preco))

        pedido = Pedido(cliente=cliente, itens=itens_pedido)
        return self.processar_checkout(pedido=pedido, codigo_cupom=codigo_cupom)
