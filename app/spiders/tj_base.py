import re
from slugify import slugify
from app.util import get_item, split_process_number
from app.spiders.spider_base import SpiderBase


class TjBase(SpiderBase):
    paths: list

    def get_process(self, number: str) -> list:
        number = split_process_number(number)
        result = []
        for item in self.paths:
            path = item.get('path').format(**number)
            self.run(path)
            result.append({item.get('name'): self.data()})
        return result

    def process_secao(self) -> dict:
        itens = {}
        table = get_item(1, self.soup.findAll('table', {'class': 'secaoFormBody'}))
        if table:
            for tr in table.findAll('tr'):
                i = tr.get_text(strip=True).split(':')
                if len(i) > 1:
                    itens.update({slugify(i[0], separator='_'): i[1].strip()})
        return itens

    def process_parts(self) -> dict:
        table = self.soup.find('table', {'id': 'tablePartesPrincipais'})
        author, defendant = {}, {}
        if table:
            tr = table.findAll('tr')
            if get_item(0, tr):
                item = list(filter(None, re.split(r"Advogad[oa]:|Autor[a]?:|Impetrante:", tr[0].get_text(strip=True))))
                author = {'autor': item.pop(0), 'advogados': item}
            if get_item(1, tr):
                item = list(
                    filter(None, re.split(r"Advogad[oa]:|[rR][eé][u]?:|Impetrado:|Procurador:", tr[1].get_text(strip=True)))
                )
                defendant = {'reu': item.pop(0), 'advogados': item}
        return {'partes_do_processo': [author, defendant]}

    def process_moves(self) -> dict:
        mov = []
        table = self.soup.find('tbody', {'id': 'tabelaTodasMovimentacoes'})
        if table:
            for tr in table.findAll('tr'):
                tmp = []
                for item in tr.findAll('td'):
                    item = item.get_text(strip=True)
                    if item:
                        tmp.append(item)
                mov.append(tmp)
        return {'lista_das_movimentacoes': mov}

    def data(self) -> dict:
        return {**self.process_secao(), **self.process_parts(), **self.process_moves()}
