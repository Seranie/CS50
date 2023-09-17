CREATE TABLE students (
    id INTEGER NOT NULL,
    student_name,
    PRIMARY KEY(id)
);

CREATE TABLE houses(
    student_id INTEGER NOT NULL,
    house TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
);

CREATE TABLE house_assignments(
    student_id INTEGER NOT NULL,
    head TEXT,
    FOREIGN KEY(student_ID) REFERENCES students(id)
);