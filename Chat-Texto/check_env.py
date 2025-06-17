import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print(f"sys.path: {sys.path}")

try:
    import langchain_community.document_loaders
    print("langchain_community.document_loaders FOUND!")
except ModuleNotFoundError as e:
    print(f"ModuleNotFoundError: {e}")
    print("langchain_community.document_loaders NOT FOUND!")
except Exception as e:
    print(f"Other error during import: {e}")

# Lista de pacotes que você espera ter instalado
expected_packages = [
    "langchain-community",
    "langchain",
    "pypdf",
    "chromadb",
    "streamlit"
]

print("\n--- Installed Packages (relevant) ---")
import pkg_resources
installed_packages = {d.project_name: d.version for d in pkg_resources.working_set}

for pkg_name in expected_packages:
    if pkg_name.lower() in [k.lower() for k in installed_packages.keys()]:
        # Encontra o nome exato do pacote instalado (com hífens vs underscores)
        actual_pkg_name = [k for k in installed_packages.keys() if k.lower() == pkg_name.lower()][0]
        print(f"{actual_pkg_name}: {installed_packages[actual_pkg_name]}")
    else:
        print(f"{pkg_name}: NOT FOUND")