import json
import os
import ast
import logging

def split_json_file(data, output_dir, base_filename, chunk_size=1024*1024*5):
    """
    Divide um objeto JSON em partes menores e salva como arquivos.

    Args:
        data (dict): Dados JSON.
        output_dir (str): Diretório onde as partes menores serão salvas.
        base_filename (str): Nome base dos arquivos.
        chunk_size (int): Tamanho de cada parte em bytes. Padrão é 5MB.
    """
    os.makedirs(output_dir, exist_ok=True)
    serialized_data = json.dumps(data, indent=4)
    total_size = len(serialized_data)
    num_chunks = total_size // chunk_size + (1 if total_size % chunk_size != 0 else 0)

    for i in range(num_chunks):
        chunk_data = serialized_data[i * chunk_size:(i + 1) * chunk_size]
        output_file_path = os.path.join(output_dir, f"{base_filename}_part{i+1}.json")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(chunk_data)
        logging.info(f"Saved {output_file_path}")

def summarize_json_file(data):
    """
    Gera um resumo do objeto JSON.

    Args:
        data (dict): Dados JSON.

    Returns:
        dict: Resumo dos dados.
    """
    summary = {
        "total_items": len(data),
        "sample_item": next(iter(data.items())) if data else "Empty"
    }
    return summary

def save_summary(summary, output_file_path):
    """
    Salva o resumo em um arquivo JSON.

    Args:
        summary (dict): Dados do resumo.
        output_file_path (str): Caminho para o arquivo onde o resumo será salvo.
    """
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(summary, file, indent=4)
    logging.info(f"Saved summary to {output_file_path}")

def analyze_python_files(project_path):
    """
    Analisa arquivos Python no projeto para coletar importações e outras informações.

    Args:
        project_path (str): Caminho para o projeto.

    Returns:
        dict: Dados de análise dos arquivos Python.
    """
    analysis = {}
    venv_folders = {'venv', '.venv', 'env', '.env'}

    for root, _, files in os.walk(project_path):
        if any(venv_folder in root for venv_folder in venv_folders):
            continue  # Ignorar diretórios de ambientes virtuais

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            tree = ast.parse(f.read(), filename=file_path)
                        except UnicodeDecodeError:
                            with open(file_path, 'r', encoding='latin-1') as f:
                                tree = ast.parse(f.read(), filename=file_path)
                    imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
                    imports_from = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
                    analysis[file_path] = {
                        "imports": imports,
                        "imports_from": imports_from
                    }
                except (SyntaxError, UnicodeDecodeError) as e:
                    logging.warning(f"Skipped file {file_path} due to parsing error: {e}")
    return analysis

def save_analysis(analysis, output_file_path):
    """
    Salva a análise dos arquivos Python em um arquivo JSON.

    Args:
        analysis (dict): Dados da análise.
        output_file_path (str): Caminho para o arquivo onde a análise será salva.
    """
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(analysis, file, indent=4)
    logging.info(f"Saved analysis to {output_file_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    project_path = "C:/AutoNoCode"
    output_dir = os.path.join(project_path, "tests", "project_summary")
    summary_output_path = os.path.join(output_dir, "summary.json")

    # Geração de resumo e análise do projeto
    logging.info("Analyzing Python files...")
    analysis = analyze_python_files(project_path)

    analysis_output_path = os.path.join(output_dir, "python_analysis.json")
    save_analysis(analysis, analysis_output_path)

    summary = summarize_json_file(analysis)
    save_summary(summary, summary_output_path)

    # Divisão do arquivo JSON em partes menores
    logging.info("Splitting JSON files into smaller parts...")
    split_json_file(analysis, output_dir, "directory_structure")
