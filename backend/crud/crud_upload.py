from backend.models.upload import Upload


def create_upload(db, data):

    upload = Upload(**data)

    db.add(upload)

    db.commit()

    db.refresh(upload)

    return upload


def get_uploads(db, teacher_id):

    return (

        db.query(Upload)

        .filter(
            Upload.teacher_id == teacher_id
        )

        .order_by(
            Upload.created_at.desc()
        )

        .all()

    )


def delete_upload(db, upload):

    db.delete(upload)

    db.commit()