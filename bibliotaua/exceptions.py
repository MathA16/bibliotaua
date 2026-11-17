"""
Módulo de Exceções de Domínio - BiblioTauá
Define as exceções de negócio mapeadas a partir dos Fluxos de Exceção da DUC UC04.

Instruções para o Aluno (Aula 24):
Consulte o Slide 12 e o guia_desenvolvedor.md para implementar as classes de exceção
que herdam de CupomInvalidoError.
"""

class BiblioTauaException(Exception):
    """Exceção base para regras de negócio do BiblioTauá."""
    pass


class CupomInvalidoError(BiblioTauaException):
    """Exceção geral disparada quando um cupom viola regras de negócio ou elegibilidade."""
    pass


# ==============================================================================
# TODO: [ALUNO - TAREFA 1] Implementar as subclasses de exceção da DUC UC04
# ==============================================================================

class CupomInexistenteError(CupomInvalidoError):
    """Lançada quando o código de cupom informado não consta na base de dados (FE01)."""
    def __init__(self, codigo: str):
        super().__init__(f"Cupom '{codigo}' não encontrado no sistema.")
        self.codigo = codigo

# TODO: 2. CupomInativoError(CupomInvalidoError)
# Mensagem: "O cupom '{codigo}' encontra-se desativado temporariamente."
class CupomInativoError(CupomInvalidoError):
    """Lançada quando o cupom existe mas foi desativado (FE01)."""
    def __init__(self, codigo: str):
        super().__init__(f"O cupom '{codigo}' encontra-se desativado temporariamente.")
        self.codigo = codigo


# TODO: 3. CupomExpiradoError(CupomInvalidoError)
# Mensagem: "O cupom '{codigo}' expirou em {validade_ate}."
class CupomExpiradoError(CupomInvalidoError):
    """Lançada quando a data atual ultrapassa a data limite (FE02)."""
    def __init__(self, codigo: str, validade_ate: str):
        super().__init__(f"O cupom '{codigo}' expirou em {validade_ate}.")
        self.codigo = codigo
        self.validade_ate = validade_ate


# TODO: 4. CupomEsgotadoError(CupomInvalidoError)
# Mensagem: "O cupom '{codigo}' atingiu a quantidade máxima de {limite} usos e esgotou."
class CupomEsgotadoError(CupomInvalidoError):
    """Lançada quando a cota máxima de utilizações foi atingida (FE03)."""
    def __init__(self, codigo: str, limite: int):
        super().__init__(f"O cupom '{codigo}' atingiu a quantidade máxima de {limite} usos e esgotou.")
        self.codigo = codigo
        self.limite = limite


# TODO: 5. ValorMinimoNaoAtingidoError(CupomInvalidoError)
# Mensagem: "O cupom '{codigo}' exige pedido mínimo de R$ {valor_minimo:.2f}. Subtotal atual: R$ {subtotal_atual:.2f}."
class ValorMinimoNaoAtingidoError(CupomInvalidoError):
    """Lançada quando o subtotal é inferior ao exigido (FE04)."""
    def __init__(self, codigo: str, valor_minimo: float, subtotal_atual: float):
        super().__init__(
            f"O cupom '{codigo}' exige pedido mínimo de R$ {valor_minimo:.2f}. "
            f"Subtotal atual: R$ {subtotal_atual:.2f}."
        )
        self.codigo = codigo
        self.valor_minimo = valor_minimo
        self.subtotal_atual = subtotal_atual


# ==============================================================================
# Exceções Pré-existentes (v0.3.0)
# ==============================================================================
class EstoqueInsuficienteError(BiblioTauaException):
    """Lançada quando a quantidade solicitada de um livro supera o estoque disponível."""
    def __init__(self, livro_titulo: str, estoque_atual: int, solicitado: int):
        super().__init__(
            f"Estoque insuficiente para '{livro_titulo}'. Disponível: {estoque_atual}, Solicitado: {solicitado}."
        )
        self.livro_titulo = livro_titulo
        self.estoque_atual = estoque_atual
        self.solicitado = solicitado
