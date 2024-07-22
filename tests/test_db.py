from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='Eryck', password='@Mantinha', email='eryck1@test.com'
    )
    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'eryck1@test.com')
    )

    assert result.username == 'Eryck'
