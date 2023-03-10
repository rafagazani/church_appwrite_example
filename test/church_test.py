from faker import Faker
from faker.providers import person, address
from appwrite.permission import Permission
from appwrite.role import Role
import env
import server
import json
from models.church_model import ChurchModel

fake = Faker('pt_BR')
fake.add_provider(person)
fake.add_provider(address)

colecao = 'churches'


def fromJson(json_str):
    json_dict = json.loads(json_str)
    return ChurchModel.parse_obj(json_dict)


empresas = []
for _ in range(10):
    empresas.append(ChurchModel.parse_obj({
        'name': fake.company(),
        'fantasyName': fake.company_suffix(),
        'cpfCnpj': fake.cnpj(),
        'status': fake.boolean(chance_of_getting_true=90),
        'zipCode': fake.postcode(),
        'city': fake.city(),
        'uf': fake.state_abbr(),
        'district': fake.neighborhood(),
        'street': fake.street_name(),
        'number': fake.building_number(),
        'complement': '',
        'contact': fake.name(),
        'email': fake.email(),
        'phone1': fake.phone_number(),
        'phone2': fake.phone_number() if fake.boolean(chance_of_getting_true=20) else None,
        'facebook': fake.uri()[:30] if fake.boolean(chance_of_getting_true=20) else None,
        'instagram': fake.uri()[:30] if fake.boolean(chance_of_getting_true=20) else None,
        'youtube': fake.uri()[:30] if fake.boolean(chance_of_getting_true=20) else None,
        'site': fake.uri()[:30] if fake.boolean(chance_of_getting_true=20) else None,
        'tiktok': fake.uri()[:30] if fake.boolean(chance_of_getting_true=20) else None,
        'responsibleId': fake.uuid4()
    }))

for item in empresas:
    server.databases.create_document(env.db, collection_id=colecao,
                                       document_id='unique()',
                                       data=item.json(),
                                       permissions=[
                                           Permission.read(Role.team('peniel')),
                                           Permission.update(Role.team('peniel', role='owner')),
                                           Permission.delete(Role.team('admin', role='owner'))
                                       ])
