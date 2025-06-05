import PyPDF2


def dividir_pdf(arquivo_origem, pagina_inicial, pagina_final, arquivo_saida):
    """
    Extrai páginas de um PDF e salva em outro arquivo.

    :param arquivo_origem: Caminho do PDF original.
    :param pagina_inicial: Página inicial (começa em 1).
    :param pagina_final: Página final (inclusive, começa em 1).
    :param arquivo_saida: Caminho do novo PDF gerado.
    """
    with open(arquivo_origem, 'rb') as pdf_file:
        leitor = PyPDF2.PdfReader(pdf_file)
        escritor = PyPDF2.PdfWriter()

        total_paginas = len(leitor.pages)

        # Ajustar para índice baseado em zero
        for i in range(pagina_inicial - 1, min(pagina_final, total_paginas)):
            escritor.add_page(leitor.pages[i])

        with open(arquivo_saida, 'wb') as saida:
            escritor.write(saida)
        print(f"Novo PDF criado: {arquivo_saida}")


# Exemplo de uso
dividir_pdf("IA-307.pdf", 93, 105, "pragas_e_doencas.pdf")
