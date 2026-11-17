# BiblioTauá — Projeto Prático do Aluno (Sprint 04 - Aula 26)
## TASK-204 (Etapa 3): Diagrama de Sequência e Orquestração do Negócio no Checkout

Bem-vindo(a) ao Encontro 3 da Sprint 04 do sistema **BiblioTauá Livraria Web**!

Nas Aulas 24 e 25, você projetou o domínio de cupons (`models/cupom.py`), a hierarquia de exceções de negócio (`exceptions.py`), o esquema físico relacional e o repositório de persistência SQLite (`repositories/cupom_repository.py`).

Hoje, nossa missão é orquestrar a compra completa de ponta a ponta: converter o **Diagrama de Sequência UML** em código vivo, implementando o serviço desacoplado de cálculo (`CalculadoraDescontoService`), integrando o cupom ao agregado `Pedido` e construindo o serviço orquestrador `CheckoutService` com controle transacional e baixa de estoque no SQLite!

---

## 🌿 Fluxo Git & GitHub do Estudante

Você segue desenvolvendo no seu **próprio repositório no GitHub** (fork):

*   **Opção A (Continuar da Aula 25):**
    ```bash
    git checkout feature/task-204-motor-cupons
    ```
*   **Opção B (Ponto Homologado da Aula 26):**
    ```bash
    git fetch upstream
    git checkout -b feature/task-204-aula26 upstream/aula-26
    ```

---

## 🎯 Suas Tarefas Hoje

1. **`bibliotaua/services/calculadora_desconto.py` (Domain Service de Cálculo):**
   - Implementar o método estático `calcular(subtotal, tipo_desconto, valor_desconto)` respeitando percentual e valor fixo limitado ao subtotal.
   - Implementar o método `validar_e_calcular(cupom, subtotal, data_referencia)` disparando as exceções da DUC UC04.

2. **`bibliotaua/models/pedido.py` (Integração do Cupom no Agregado Pedido):**
   - Adicionar os atributos `cupom: Optional[Cupom]` e `desconto_aplicado: float`.
   - Implementar o método `aplicar_cupom(self, cupom: Cupom)` invocando a validação de regras da DUC e registrando o desconto.
   - Atualizar a propriedade dinâmica `total`: $\text{total} = \max(\text{subtotal} - \text{desconto\_aplicado}, 0.0)$.
   - Implementar `remover_cupom(self)` para resetar o desconto caso o cupom seja cancelado.

3. **`bibliotaua/services/checkout_service.py` (Application Service Orquestrador):**
   - Implementar o construtor `__init__` recebendo a conexão SQLite e inicializando os repositórios.
   - Implementar `processar_checkout(self, pedido, codigo_cupom)` orquestrando as 4 etapas do Diagrama de Sequência:
     1. Busca do cupom no `CupomRepository` e aplicação no `Pedido`.
     2. Validação e débito de estoque para cada livro com `item.livro.debitar_estoque(qtd)`.
     3. Transação atômica (`with self.conn`): atualização de estoques no banco, incremento do cupom (`registrar_uso`) e salvamento do pedido (`PedidoRepository.salvar`).
     4. Definição do status como `PAGO` e retorno do pedido finalizado.

4. **`main.py` (Script de Verificação Integrada):**
   - Executar os 5 cenários práticos no terminal e verificar a conformidade com as regras da Sprint.

---

## 🚀 Como Executar

No terminal, dentro da pasta do projeto, execute:

```bash
python3 main.py
```

**Critério de Aceite:**
Todos os 5 blocos de teste devem ser executados com sucesso, confirmando a correta aplicação de cupons percentuais e fixos, o recálculo do total, o débito no estoque dos livros, o incremento de usos no SQLite e a transacionalidade ao barrar cupons inválidos ou pedidos sem estoque.

---

## 💾 Versionamento e Entrega no GitHub

Ao concluir os testes com sucesso, envie o código para seu repositório pessoal:

```bash
git add bibliotaua/models/pedido.py bibliotaua/services/ main.py
git commit -m "feat(services): implementa calculo de desconto e CheckoutService transacional (Aula 26)"
git push origin HEAD
```
