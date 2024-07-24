import os
from collections import defaultdict

class ProjectStructureGenerator:
    def __init__(self, root_dir, max_depth=10, max_duplicates_reported=100):
        """
        Inicializa a classe com o diretório raiz do projeto.
        :param root_dir: Diretório raiz do projeto.
        :param max_depth: Profundidade máxima para busca recursiva.
        :param max_duplicates_reported: Número máximo de arquivos duplicados a serem relatados.
        """
        self.root_dir = root_dir
        self.max_depth = max_depth
        self.max_duplicates_reported = max_duplicates_reported

    def get_project_structure(self) -> str:
        """
        Gera a estrutura do projeto como uma string formatada.
        :return: String representando a estrutura de diretórios e arquivos do projeto.
        """
        print("Gerando estrutura do projeto...")
        structure = []
        file_map = defaultdict(list)  # Para rastrear arquivos com nomes iguais
        total_files = 0

        for root, dirs, files in os.walk(self.root_dir):
            # Calcula o nível de profundidade atual
            level = root.replace(self.root_dir, '').count(os.sep)
            if level > self.max_depth:
                continue  # Pula diretórios além da profundidade máxima

            # Define a indentação com base no nível
            indent = ' ' * 4 * level
            # Adiciona o nome do diretório à estrutura
            structure.append(f"{indent}{os.path.basename(root)}/")
            # Define a indentação para os arquivos
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                total_files += 1
                # Adiciona o nome do arquivo à estrutura
                structure.append(f"{subindent}{f}")
                # Adiciona o caminho completo do arquivo ao mapa de arquivos
                file_map[f].append(os.path.join(root, f))
                if total_files % 1000 == 0:
                    print(f"{total_files} arquivos processados...")

        print(f"Total de arquivos processados: {total_files}")

        # Verifica arquivos duplicados
        duplicates = {file: paths for file, paths in file_map.items() if len(paths) > 1}
        duplicates_reported = 0
        if duplicates:
            structure.append("\nArquivos duplicados encontrados:")
            for file, paths in duplicates.items():
                structure.append(f"Arquivo: {file}")
                for path in paths:
                    structure.append(f" - {path}")
                duplicates_reported += 1
                if duplicates_reported >= self.max_duplicates_reported:
                    structure.append("\nMuitos arquivos duplicados... Relatório truncado.")
                    break
        else:
            structure.append("\nNenhum arquivo duplicado encontrado.")

        # Retorna a estrutura como uma única string, com quebras de linha
        return '\n'.join(structure)

    def save_structure_to_files(self, file_path: str, max_chars: int = 1700000, num_files: int = 10):
        """
        Salva a estrutura do projeto em vários arquivos de texto, cada um com até max_chars caracteres.
        :param file_path: Caminho base do arquivo onde a estrutura será salva.
        :param max_chars: Número máximo de caracteres por arquivo.
        :param num_files: Número máximo de arquivos a serem gerados.
        """
        # Apaga os arquivos txt existentes no diretório de saída
        dir_path = os.path.dirname(file_path)
        for file in os.listdir(dir_path):
            if file.endswith(".txt"):
                os.remove(os.path.join(dir_path, file))
                print(f"Arquivo {file} apagado.")

        # Obtém a estrutura do projeto
        structure = self.get_project_structure()
        # Calcula o tamanho de cada parte
        total_length = len(structure)
        part_size = min(max_chars, total_length // num_files + (total_length % num_files > 0))

        # Divide a estrutura em partes menores
        chunks = [structure[i:i+part_size] for i in range(0, len(structure), part_size)]

        # Garante que não mais do que num_files sejam gerados
        chunks = chunks[:num_files]

        # Salva cada parte em um arquivo separado
        for i, chunk in enumerate(chunks):
            chunk_file_path = f"{file_path}_part{i+1}.txt"
            with open(chunk_file_path, 'w', encoding='utf-8') as f:
                f.write(chunk)
            print(f"Estrutura do projeto salva em {chunk_file_path}")

if __name__ == "__main__":
    # Define o diretório raiz do projeto
    root_directory = "C:\\AutoNoCode"
    # Define o diretório onde o resumo será salvo
    summary_directory = os.path.join(root_directory, "scripts", "summary")
    # Cria o diretório de resumo se ele não existir
    os.makedirs(summary_directory, exist_ok=True)
    # Define o caminho base do arquivo de saída
    file_path = os.path.join(summary_directory, "project_structure")

    # Cria uma instância da classe ProjectStructureGenerator
    generator = ProjectStructureGenerator(root_directory, max_depth=10, max_duplicates_reported=100)
    # Salva a estrutura do projeto em arquivos especificados
    generator.save_structure_to_files(file_path, max_chars=1700000, num_files=10)
    # Imprime uma mensagem confirmando que a estrutura foi salva
    print(f"Estrutura do projeto salva em arquivos separados.")
