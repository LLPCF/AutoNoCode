
### 6. Análise de Impacto

Adicione um script `scripts/analyze_impact.py` para análise de impacto:

```python
# Filename: analyze_impact.py
# Date: 2024-07-01
# Root Project Folder: AutoNoCode

import time
import cProfile
import pstats
from pathlib import Path
import radon.complexity as cc
import radon.raw as raw

def analyze_performance(directory: Path):
    prof = cProfile.Profile()
    prof.enable()

    # Simule a execução do código principal aqui
    time.sleep(1)  # Substitua isso pela execução real do código

    prof.disable()
    stats = pstats.Stats(prof).sort_stats('cumtime')
    stats.print_stats()

def analyze_code_metrics(directory: Path):
    for file in directory.glob('**/*.py'):
        with open(file, 'r') as f:
            code = f.read()
        print(f"Análise de {file}:")
        print("Complexidade ciclomática:")
        print(cc.cc_visit(code))
        print("Métricas brutas:")
        print(raw.analyze(code))

if __name__ == "__main__":
    directory = Path('src/autonocode')
    analyze_performance(directory)
    analyze_code_metrics(directory)
