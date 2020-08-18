#!/usr/bin/env python3
from random import choice

'''
Precisazione: Nei commenti, viene chiamato "file" l'insieme delle
linee di testo che l'editor produce, a prescindere dalla struttura
dati utilizzata
'''

'''
Maxfilelen è una lista che tiene traccia continuamente della
lunghezza del file, in modo da avere un riferimento da usare
nelle Change
'''
maxfilelen = [0]

'''
Index viene spostato da Undo e Redo, e serve come indice di
maxfilelen per sapere qual è la dimensione del file attuale
'''
index = 0


'''
INPUT
'''

# Lunghezza massima del file
maxlen = int(input("Massima lughezza del file? [default 1024] ") or "1024")

# Numero di comandi del test
length = int(input("Quanti comandi? [default 1000] ") or "1000")

# Categoria di test
category = int(input("Che modalità di test?\n\
        0. Test con tutti i comandi possibili, in ordine casuale\n\
        1. Test simile a RollingBack, c, d e p all'inizio, u, r e p alla fine (ultimo 10%)\n\
        Scegliere il numero corrispondente [default 0] ") or "0")


# Crea un array con le frasi da usare nelle Change
quotes = []
f = open("quotes.txt", "r")
for line in f:
    quotes.append(line)
f.close()

# Crea il test
f = open("test.txt", "w")

letters = ['c', 'p', 'd', 'u', 'r']
letters1 = ['c', 'p', 'd']
letters2 = ['u', 'r', 'p']

# Ciclo principale
tenpercent = length - (length * (1/10))
for i in range(length - 1):
    # sceglie a caso una lettera tra le 5
    if category == 0:
        letter = choice(letters)
    else:
        if i < tenpercent:
            letter = choice(letters1)
        else:
            letter = choice(letters2)

    # Undo o Redo
    if letter == 'u' or letter == 'r':
        # sceglie un numero a caso tra 0 e maxlen
        num = choice(range(maxlen))
        # crea il comando e lo mette nella stringa s
        s = '{}{}'.format(num, letter)

        # tiene traccia dell'indice: per le Undo si sposta
        # indietro, per le Redo avanti
        if letter == 'u':
            index -= num
            if index < 0:
                index = 0
        else:
            index += num
            if index > len(maxfilelen) - 1:
                index = len(maxfilelen) - 1

    # Delete o Print
    elif letter == 'd' or letter == 'p':
        # sceglie due numeri a caso tra 0 e maxlen, dove il secondo
        # è maggiore del primo
        num0 = choice(range(maxlen))
        num1 = choice(range(num0, maxlen))
        # crea il comando e lo mette nella stringa s
        s = '{},{}{}'.format(num0, num1, letter)

        # se è una Delete, tiene traccia della nuova lunghezza del file
        if letter == 'd':
            # se non è alla fine della lista maxfilelen, vuol dire che
            # c'è stata un'Undo precedentemente, ma ora elimina tutto
            # quello che viene dopo l'indice attuale
            if index != len(maxfilelen) - 1:
                maxfilelen = maxfilelen[:index + 1]

            # se non viene eliminato niente (il file era di lunghezza
            # 0 precedentemente o sta cercando di eliminare qualcosa che
            # viene dopo il file), la lunghezza rimane invariata
            if (maxfilelen[index] == 0 or num0 > maxfilelen[index]):
                maxfilelen.append(maxfilelen[index])
            # se sta eliminando tutto il file, la lunghezza è 0
            elif maxfilelen[index] <= num1 and (num0 == 1 or num0 == 0):
                maxfilelen.append(0)
            # altrimenti, scrive la lunghezza, quella precedente meno
            # il numero di righe cancellate
            else:
                num1 = min(maxfilelen[index], num1)
                maxfilelen.append(maxfilelen[index] - (num1 - num0 + 1))
            index += 1

    # Change
    else:
        # se la lunghezza attuale del file è 0, il comando deve per forza
        # iniziare da 1
        if maxfilelen[index] == 0:
            num0 = 1
        # altrimenti, numero casuale tra 1 e la lunghezza attuale + 1
        else:
            num0 = choice(range(1, maxfilelen[index] + 1))
        num1 = choice(range(num0, maxlen))

        # crea il comando e lo mette nella stringa s
        s = '{},{}{}\n'.format(num0, num1, letter)
        # aggiunge alla stringa il numero stabilito di frasi, e il . finale
        for j in range(num1 - num0 + 1):
            s += choice(quotes)
        s += '.'

        # se non è alla fine della lista maxfilelen, vuol dire che
        # c'è stata un'Undo precedentemente, ma ora elimina tutto
        # quello che viene dopo l'indice attuale e aggiunge il nuovo
        # valore di lunghezza del file
        if index != len(maxfilelen) - 1:
            maxfilelen = maxfilelen[:index + 1]
        maxfilelen.append(max(num1, maxfilelen[index]))
        index += 1

    # scrive il comando s nel test
    f.write(s + '\n')

# Scrive il q finale nel test e chiude il file di test
f.write('q\n')
f.close()
