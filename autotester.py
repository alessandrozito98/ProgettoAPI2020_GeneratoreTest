import subprocess as sp
import json

# gcc -DEVAL -std=gnu11 -O2 -pipe -static -s -o timeforachange timeforachange.c -lm

with open('autotester_settings.json') as settings:
    count = 0
    json_file = json.load(settings)

    while True:
        count += 1

        compileProcess = sp.run(
            ['gcc', *json_file['gccArgs'],
             '-o', 'executable', json_file['source']],
            text=True,  stdout=sp.PIPE)

        if compileProcess.stderr != None:
            print(compileProcess.stderr)

        generatorProcess = sp.run(
            ['python', 'generatore.py'],
            input=('\n'.join((json_file['generatorArgs'] + ['\n']))),
            text=True,  stdout=sp.PIPE)

        print(f'try number: {count}... ', end='')

        output = open('your_output.txt', 'w')

        runProcess = sp.run(
            ['./executable'],
            input=open('test.txt', 'rb').read(),
            stdout=output)

        # print(runProcess.stdout)

        diffProcess = sp.run(
            ['diff',  'your_output.txt', 'sol.txt',
             '--brief', '--ignore-trailing-space'],
            stdout=sp.PIPE)

        if len(diffProcess.stdout) == 0:
            print('OK')
        else:
            print('KO')
            print(diffProcess.stdout.decode())
            print("Please run 'diff your_output.txt sol.txt' to find differences.")
            exit(1)
