"""
Serviço de Domínio: CalculadoraDescontoService (TASK-204)
Encapsula o cálculo matemático de abatimento financeiro e validação de regras de cupons.

Instruções para o Aluno (Aula 26):
Consulte os Slides 13 e 14 e o guia_desenvolvedor.md para implementar:
1. Método estático calcular(subtotal, tipo_desconto, valor_desconto)
2. Método estático validar_e_calcular(cupom, subtotal, data_referencia)
"""
from datetime import date
from typing import Optional
from bibliotaua.models.cupom import Cupom, TipoDesconto

class CalculadoraDescontoService:
    """Serviço de domínio puro para cálculo e validação de descontos."""

    @staticmethod
    def calcular(subtotal: float, tipo_desconto: TipoDesconto, valor_desconto: float) -> float:
        """
        TODO: [ALUNO - TAREFA 1.1]
        1. Se subtotal <= 0 -> retorna 0.0
        2. Se tipo_desconto == PERCENTUAL -> desconto = subtotal * (valor_desconto / 100.0)
        3. Se tipo_desconto == VALOR_FIXO -> desconto = min(valor_desconto, subtotal)
        4. Senão -> lança ValueError
        5. Retorna round(desconto, 2)
        (Consulte o Slide 13 do Beamer)
        """
        raise NotImplementedError("TODO: Implementar CalculadoraDescontoService.calcular()")

    @staticmethod
    def validar_e_calcular(
        cupom: Cupom,
        subtotal: float,
        data_referencia: Optional[date] = None
    ) -> float:
        """
        TODO: [ALUNO - TAREFA 1.2]
        1. Invoca cupom.pode_ser_aplicado_ao_pedido(subtotal, data_referencia)
        2. Retorna CalculadoraDescontoService.calcular(subtotal, cupom.tipo_desconto, cupom.valor_desconto)
        """
        raise NotImplementedError("TODO: Implementar CalculadoraDescontoService.validar_e_calcular()")
