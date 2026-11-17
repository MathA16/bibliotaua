"""
Entidade de Domínio: Pedido (Agregado Raiz da Compra de Livros)
Representa o pedido de compra, orquestrando itens, cupons de desconto e status.

Instruções para o Aluno (Aula 26):
Consulte o Slide 15 e o guia_desenvolvedor.md para implementar:
1. Propriedade total com dedução do desconto
2. Método aplicar_cupom(cupom)
3. Método remover_cupom()
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional

from bibliotaua.models.cliente import Cliente
from bibliotaua.models.cupom import Cupom
from bibliotaua.models.item_pedido import ItemPedido

class StatusPedido(str, Enum):
    CRIADO = "CRIADO"
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    PAGO = "PAGO"
    CANCELADO = "CANCELADO"
    FINALIZADO = "FINALIZADO"

@dataclass
class Pedido:
    cliente: Cliente
    itens: List[ItemPedido] = field(default_factory=list)
    cupom_aplicado: Optional[Cupom] = None
    desconto_aplicado: float = 0.0
    status: StatusPedido = StatusPedido.CRIADO
    data_criacao: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None

    @property
    def cupom(self) -> Optional[Cupom]:
        """Alias para manter compatibilidade com a modelagem do diagrama."""
        return self.cupom_aplicado

    @cupom.setter
    def cupom(self, valor: Optional[Cupom]) -> None:
        self.cupom_aplicado = valor

    def adicionar_item(self, item: ItemPedido) -> None:
        """Adiciona um item ao carrinho do pedido e recalcula desconto se houver cupom."""
        self.itens.append(item)
        if self.cupom_aplicado:
            self.aplicar_cupom(self.cupom_aplicado)

    @property
    def subtotal(self) -> float:
        """Calcula o valor bruto total dos livros adicionados."""
        return round(sum(item.subtotal for item in self.itens), 2)

    @property
    def total(self) -> float:
        """
        TODO: [ALUNO - TAREFA 2.1]
        Calcula o valor final líquido a pagar pelo cliente:
        liquido = subtotal - desconto_aplicado
        Garante que o total nunca seja negativo: max(liquido, 0.0) arredondado para 2 casas decimais.
        """
        # Substitua a linha abaixo pela lógica com desconto_aplicado:
        return self.subtotal

    def aplicar_cupom(self, cupom: Cupom) -> float:
        """
        TODO: [ALUNO - TAREFA 2.2]
        1. Se not self.itens -> lança ValueError("Não é possível aplicar cupom a um pedido vazio sem itens.")
        2. Valida as regras de negócio: cupom.pode_ser_aplicado_ao_pedido(self.subtotal)
        3. Calcula o abatimento: desconto = cupom.calcular_desconto(self.subtotal)
        4. Atribui: self.desconto_aplicado = desconto e self.cupom_aplicado = cupom
        5. Retorna self.desconto_aplicado
        (Consulte o Slide 15 do Beamer)
        """
        raise NotImplementedError("TODO: Implementar Pedido.aplicar_cupom()")

    def remover_cupom(self) -> None:
        """
        TODO: [ALUNO - TAREFA 2.3]
        Restaura o pedido sem cupom:
        self.cupom_aplicado = None
        self.desconto_aplicado = 0.0
        """
        self.cupom_aplicado = None
        self.desconto_aplicado = 0.0
