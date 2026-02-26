# Passo a Passo de Execução

## Dependências

```bash
pip install streamlit requests
```

## Ollama (opcional)

```bash
ollama pull gpt-oss
ollama serve
```

## Execução

```bash
streamlit run .\src\app.py
```

## Observação

Sem Ollama, a aplicação continua funcional usando respostas determinísticas.
