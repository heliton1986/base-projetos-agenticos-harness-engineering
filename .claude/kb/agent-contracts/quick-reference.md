# Agent Contracts — Quick Reference

## Template de contrato por agente

```python
class [Nome]Agent:

    def [operacao](self, [entrada_tipada], user: str = "system") -> [TipoResponse]:
        start = time.monotonic()

        try:
            # logica do agente

            duration = int((time.monotonic() - start) * 1000)
            audit_entry = build_audit_entry(
                operation="[operacao]",
                user=user,
                agent="[Nome]Agent",
                status="success",
                input_summary="[resumo sem dados sensiveis]",
                output_summary="[resumo do resultado]",
                duration_ms=duration,
            )
            _audit.log(audit_entry)
            return [TipoResponse](status="success", ...)

        except Exception as e:
            duration = int((time.monotonic() - start) * 1000)
            _audit.log(build_audit_entry(
                "[operacao]", user, "[Nome]Agent", "error",
                error_message=str(e), duration_ms=duration
            ))
            raise
```

## Campos obrigatorios em audit_log

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `operation` | str | nome da operacao (ingest, consolidate, detect, report) |
| `user` | str | quem acionou |
| `agent` | str | nome do agente |
| `status` | str | success / partial / error |
| `input_summary` | str | resumo da entrada — SEM dados sensiveis |
| `output_summary` | str | resumo do resultado |
| `duration_ms` | int | tempo de execucao em ms |
| `error_message` | str | detalhes do erro (apenas em status=error) |

## Regras de handoff (orquestrador → subagente)

```
OrchestratorAgent
  → recebe input do usuario
  → chama SubagenteA(entrada_tipada)
  → recebe SubagenteAResponse
  → passa contexto necessario para SubagenteB
  → nao compartilha estado mutavel entre agentes
  → agrega resultados e retorna resposta final
```

## Tipos de response (padrao)

```python
class [Nome]Response(BaseModel):
    status: str          # "success" | "partial" | "error"
    # campos especificos da capacidade
    audit_log_id: str | None = None
```

## Checklist de contrato

- [ ] Entrada tipada com Pydantic ou dataclass
- [ ] Saida tipada com campo `status`
- [ ] audit_log registrado em sucesso E em erro
- [ ] input_summary sem dados sensiveis
- [ ] duration_ms calculado com time.monotonic()
- [ ] Contrato documentado em `contracts/[capacidade].md`
