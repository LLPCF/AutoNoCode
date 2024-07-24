# instrument_collect.py
from pyannotate_runtime import collect_types

def main():
    # Substitua 'your_main_module' pelo módulo principal do seu projeto
    from src import your_main_module
    your_main_module.main()

if __name__ == "__main__":
    collect_types.init_types_collection()
    with collect_types.collect():
        main()
