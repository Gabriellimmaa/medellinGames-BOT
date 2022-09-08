import re

# Split the string at the first white-space character:

messageResponse = "<@742592151875223658>  123123123123  <@721260428293963837> <@745336319533908132><@721260428293963837><@721260428293963837><@721260428293963837><@721260428293963837><@721260428293963837><@721260428293963837><@721260428293963837>"
listaMencoes = re.split("\<([^\>]+)\>", messageResponse)
listaMencoesManipulada = []
for idMember in listaMencoes:
    try:        
        idMember = idMember.strip('\n')
        idMember = idMember.strip('\t') 
        if idMember[0] == "@":
            listaMencoesManipulada.append(int(idMember.strip("@")))
            listaMencoes.remove(idMember)
        else:
            print
            listaMencoes.remove(idMember)
            pass
    except:
        pass

listaMencoesManipulada = sorted(set(listaMencoesManipulada))

if len(listaMencoesManipulada) < 10:
    print('nao bateu a quantidade de membro, nao pode valores repetidos')

for membro in listaMencoesManipulada:
    membro = interaction.client.get_user(membro)


