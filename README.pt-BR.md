# Project Management AI Toolkit

v0.1.1 — prévia pública independente. Código e orientações originais sob licença MIT. Motor determinístico de caminho crítico, valor agregado, riscos e responsabilidades RACI. Sem dependências externas nem chamadas de rede no motor. **Somente dados fictícios ou públicos expressamente autorizados. Não aprovado para informações institucionais sigilosas.** Uma skill não constitui uma barreira de segurança.

Python 3.11 ou superior, atualizado e com suporte. Execute `python -B -m unittest discover -s tests -v` e `python scripts/validate_package.py` na raiz. Crie uma pasta de saída privada fora do repositório e execute:

```powershell
python plugins/project-management-ai/skills/project-management-ai/scripts/review.py --input plugins/project-management-ai/skills/project-management-ai/examples/project.json --out "$HOME/pm-demo/demo.json"
```

O exemplo é fictício. Entrada JSON estrita e valores monetários em centavos. A saída exige sistema de arquivos com hard links. Não realiza ações externas nem certificações. Leia SECURITY.md e docs/INSTALL.md antes de instalar. O ambiente de IA pode ser remoto mesmo que o script seja executado localmente dentro dele.

Consulte docs/SOURCES.md, docs/THREAT-MODEL.md, docs/INSTITUTIONAL-GATES.md e docs/VALIDATION.md. Projeto sem vínculo com PMI, PM4NGOs, União Europeia ou qualquer empregador.
