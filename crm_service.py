from database import Session, Client

def create_or_update_client(name, phone):
    session = Session()

    client = session.query(Client).filter_by(phone=phone).first()

    if not client:
        client = Client(name=name, phone=phone)
        session.add(client)

    session.commit()
    return client
