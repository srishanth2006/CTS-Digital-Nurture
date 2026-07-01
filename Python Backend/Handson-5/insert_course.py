from app import app
from extensions import db
from courses.models import Course

with app.app_context():
    c = Course(
        name="Python Programming",
        code="CS101",
        credits=4,
        department_id=1
    )
    db.session.add(c)
    db.session.commit()
    print("Course inserted successfully!")
    print("Total courses:", Course.query.count())
    