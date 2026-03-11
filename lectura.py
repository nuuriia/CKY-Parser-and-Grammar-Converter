from pytokr import item, items 
def llegir():
    tots=[]
    for arxiu in items():
        jocs_de_prova={}
        nom=item()
        while nom !='fi':
            paraules=[]
            i=item()
            if i=='[':
                i=item()
                if i=="''":
                    i=''
                while i!=']':
                    paraules.append(i)
                    i=item()
                    if i=="''":
                        i=''
            inicial=item()
            terminals=set()
            i=item()
            if i=='[':
                i=item()
                while i!=']':
                    terminals.add(i)
                    i=item()
            else:
                print('Error de lectura')

            gramatica={}
            fi = False
            seguent=item()
            while not fi:
                clau=seguent
                gramatica[clau]=[]

                ha_estat_clau=item()
                if ha_estat_clau== '>':
                    valor=item()
                    if arxiu=='PCKY':
                        prob=float(item())
                        if valor=='eps':
                            gramatica[clau].append((tuple(),prob))
                        else:
                            gramatica[clau].append((tuple(valor),prob))
                    else:
                        if valor=='eps':
                            gramatica[clau].append(tuple())
                        else:
                            gramatica[clau].append(tuple(valor))
                    

                    seguent= item()
                    fi = seguent=='fi'
                    while seguent =='|':
                        valor=item()
                        if arxiu=='PCKY':
                            prob=float(item())
                            if valor=='eps':
                                gramatica[clau].append((tuple(),prob))
                            else:
                                gramatica[clau].append((tuple(valor),prob))
                        else:
                            if valor=='eps':
                                gramatica[clau].append(tuple())
                            else:
                                gramatica[clau].append(tuple(valor))
                        seguent= item() 
                        fi = seguent=='fi'  
            jocs_de_prova[nom]=((gramatica,inicial,terminals),paraules)
            nom=item()
        tots.append(jocs_de_prova)
    return tots
     