# Consulta-CTF-CNAE
Análise de dados em Python sobre informações da Receita Federal e do IBAMA.

## Objetivo
Este repositório contém uma série de scripts para acessar e organizar dados abertos disponibilizados pela Receita Federal e pelo IBAMA. A ideia é que esses dados consolidados alimentem um painel BI que permita responder perguntas como:

_Quantas empresas de determinada atividade econômica estão registradas junto ao Cadastro Técnico Federal (CTF) do IBAMA?_
_Qual categoria de CTF é mais comum entre as empresas de determinado ramo?_

A Nova Lei de Licitações (Lei n. 14.133/2021) explicita o princípio do desenvolvimento nacional sustentável, e o Guia de Licitações Sustentáveis da AGU recomenda como boa prática a exigência do Certificado de Regularidade das empresas quanto ao registro CTF/APP do IBAMA. Dessa forma, ferramentas que facilitem a consulta a esses registros podem contribuir nas etapas de planejamento das contratações e aquisições públicas.

## Origens dos dados
### Dados da Receita Federal
São utilizados as bases do tipo 'Estabelecimentos' da Receita Federal, disponíveis em: https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj. Dessa base, são filtradas apenas as empresas **ativas**, extraindo os dados de CNPJ e CNAEs (principal e secundário) dessas empresas.

### Dados do IBAMA
A base de dados do IBAMA, disponível em https://dadosabertos.ibama.gov.br/dataset/pessoas-juridicas-inscritas-no-ctf-app, consolida a relação de pessoas jurídicas que efetuaram a inscrição no Cadastro Técnico Federal de Atividades Potencialmente Poluidoras e Utilizadoras de Recursos Naturais – CTF/APP. São filtradas as inscrições que não tenham data de vencimento registrada (ou seja, em tese, ainda válidas) e que tenham situação 'Ativa' junto ao IBAMA. Importante frisar que não necessariamente todas as empresas registradas têm Certificado de Regularidade (ver perguntas e respostas no link https://www.gov.br/ibama/pt-br/servicos/cadastros/ctf/certificado-de-regularidade#certificado-de-regularidade--cr-).

## Licença
GNU General Public License v3.0
