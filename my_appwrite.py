from appwrite.role import Role
import env
import server


def set_funcao(nome_funcao, runtime='python-3.9', execute=None, timeout=120, events=None, cliente=None):
    funcao(nome_funcao, runtime, execute, timeout, events)
    variable(nome_funcao=nome_funcao, cliente=cliente)
    deploy(nome_funcao, runtime=runtime)


def funcao(nome_funcao, runtime='python-3.9', execute=None, timeout=30, events=None):
    if execute is None:
        execute = [Role.users()]
    try:

        server.functions.get(nome_funcao)
        server.functions.update(nome_funcao, nome_funcao, execute=execute, timeout=timeout, events=events)
        print(f'\U0001F195 funcao {nome_funcao} atualizada')

    except:

        server.functions.create(nome_funcao, nome_funcao, execute=execute,
                                  runtime=runtime,
                                  timeout=timeout,
                                  events=events
                                  )
        print(f'\U0001F195 funcao {nome_funcao} CRIADA')


def variable(nome_funcao, cliente=None,):
    variables = server.functions.list_variables(nome_funcao)

    db = False
    projeto = False
    key = False
    host = False

    cliente_v = True
    if cliente is not None:
        cliente_v = False


    for item in variables['variables']:
        if item['key'] == 'db':
            db = True
            server.functions.update_variable(nome_funcao, item['$id'], "db", env.db)
            continue

        if item['key'] == 'host':
            host = True
            server.functions.update_variable(nome_funcao, item['$id'], "host", env.host)
            continue

        if item['key'] == 'projeto':
            projeto = True
            server.functions.update_variable(nome_funcao, item['$id'], "projeto",
                                               env.project)
            continue
        if item['key'] == 'key':
            key = True
            server.functions.update_variable(nome_funcao, item['$id'], "key",
                                               env.function_key)
            continue
        if cliente:
            if item['key'] == 'cliente':
                cliente_v = True
                server.functions.update_variable(nome_funcao, item['$id'], "cliente",
                                                   env.cliente)
                continue
            else:
                cliente_v = False


    if not host:
        server.functions.create_variable(nome_funcao, "host", env.host)

    if not db:
        server.functions.create_variable(nome_funcao, "db", env.db)

    if not projeto:
        server.functions.create_variable(nome_funcao, "projeto", env.project)

    if not key:
        server.functions.create_variable(nome_funcao, "key", env.function_key)

    if not cliente_v:
        server.functions.create_variable(nome_funcao, "cliente", env.cliente)

    print(f'\U0001F195 variables {nome_funcao} criada')


def deploy(nome_funcao, runtime='python-3.9'):
    import subprocess
    extensao = 'py'
    arquivo = f'{nome_funcao}.{extensao}'

    caminho = f'cd function/{nome_funcao}/'
    set_projeto = f'appwrite client --endpoint {env.host} --projectId {env.project} --key {env.key}'
    if 'dart' in runtime.lower():
        arquivo = 'main.dart'
    enviar = f'appwrite functions createDeployment --functionId={nome_funcao} --activate=true --entrypoint="{arquivo}" --code="."'
    p = subprocess.Popen(f'{caminho};'
                         f'{set_projeto};'
                         f'{enviar}',
                         stdout=subprocess.PIPE, shell=True)

    print(p.communicate())

def login_cli():
    import subprocess
    # Configura o cliente da plataforma Appwrite
    cmd_client = f'appwrite client --endpoint {env.host} --projectId {env.project} --key {env.key}'
    process_client = subprocess.Popen(cmd_client, stdout=subprocess.PIPE, shell=True)

    # Obtém a saída do processo de configuração do cliente
    output_client = process_client.communicate()[0]

    # Exibe a saída do processo de configuração do cliente
    print(output_client.decode('utf-8'))

    process = subprocess.Popen('appwrite login', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               shell=True)

    process.stdin.write(env.cli_email.encode('utf-8') + b'\n')

    process.stdin.write(env.cli_password.encode('utf-8') + b'\n')

    # Obtém a saída do processo
    output, errors = process.communicate()

    # Exibe a saída do processo
    print(output.decode('utf-8'))