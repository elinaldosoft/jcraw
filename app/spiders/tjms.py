from app.spiders.tj_base import TjBase


class TjMs(TjBase):
    name = 'esaj.tjms.jus.br'
    url_base = 'https://esaj.tjms.jus.br'
    paths = [
        {
            'name': '1_grau',
            'path': "/cpopg5/search.do?conversationId=&dadosConsulta.localPesquisa.cdLocal=-1&cbPesquisa=NUMPROC&dadosConsulta.tipoNuProcesso=UNIFICADO&numeroDigitoAnoUnificado={ordem}-{verificador}.{ano}&foroNumeroUnificado=0001&dadosConsulta.valorConsultaNuUnificado={ordem}-{verificador}.{ano}.{digito}.{tribunal}.{origem}&dadosConsulta.valorConsulta=&uuidCaptcha=",
        },
        {
            'name': '2_grau',
            'path': '/cposg5/search.do?conversationId=&paginaConsulta=1&localPesquisa.cdLocal=-1&cbPesquisa=NUMPROC&tipoNuProcesso=UNIFICADO&numeroDigitoAnoUnificado={ordem}-{verificador}.{ano}&foroNumeroUnificado=0000&dePesquisaNuUnificado={ordem}-{verificador}.{ano}.{digito}.{tribunal}.{origem}&dePesquisa=&uuidCaptcha=',
        },
    ]
