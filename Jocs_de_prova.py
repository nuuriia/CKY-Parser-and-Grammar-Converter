from CKY import CKY
from PCKY import PCKY
from CFGtoCNF import converttoCNF
from lectura import llegir

def prova(jocs,funcio):
    i=0
    for joc in jocs.keys():
        print(f"    Joc de proves {joc}:")
        if funcio== converttoCNF:
            print(f"   Gramàtica CNF:")
            converttoCNF(jocs[joc][0])
        else:
            for paraula in jocs[joc][1]:
                print(f"Paraula: {paraula}")
                funcio(paraula, jocs[joc][0])
                print()
    print()
jp_CKY,jp_CNF, jp_PCKY = llegir()

prova(jp_CKY, CKY)
prova(jp_CNF, converttoCNF)
prova(jp_PCKY, PCKY)