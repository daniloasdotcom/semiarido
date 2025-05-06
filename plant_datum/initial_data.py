from plant_datum.plant_database import adicionar_planta, listar_plantas

def dados_iniciais():
    if len(listar_plantas()) == 0:
        adicionar_planta(
            "Spondias tuberosa", "Umbu", "Nordeste do Brasil",
            "Alimentício (fruto), sucos, geleias",
            "Sistema radicular profundo com caule subterrâneo que armazena água",
            "Planta símbolo da Caatinga, resistente à seca"
        )
        adicionar_planta(
            "Passiflora cincinnata", "Maracujá do Mato", "Caatinga brasileira",
            "Alimentício (fruto), produção de sucos, potencial medicinal",
            "Trepadeira nativa adaptada ao semiárido, folhas grossas e raízes profundas",
            "Rústico, resistente a pragas, potencial para melhoramento genético"
        )