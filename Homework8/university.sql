CREATE TABLE groups (
    group_id SERIAL PRIMARY KEY,
    name VARCHAR(120),
    group_year SMALLINT
);


CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(120),
    lastname VARCHAR(120),
    group_id INT,
    UNIQUE (student_id, group_id),
    FOREIGN KEY (group_id) REFERENCES groups (group_id)
);


CREATE TABLE teacher (
    teacher_id SERIAL PRIMARY KEY,
    name VARCHAR(120),
    lastname VARCHAR(120)
);


CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    name VARCHAR(20),
    teacher_id INT,
    FOREIGN KEY (teacher_id) REFERENCES teacher (teacher_id)
);


CREATE TABLE marks (
    mark_id SERIAL PRIMARY KEY,
    student_id INT,
    course_id INT,
    mark_value SMALLINT,
    mark_date DATE,
    UNIQUE (mark_id, student_id, course_id, mark_value, mark_date),
    FOREIGN KEY (student_id) REFERENCES students (student_id),
    FOREIGN KEY (course_id) REFERENCES courses (course_id)
);


CREATE TABLE student_courses (
    student_course_id SERIAL PRIMARY KEY,
    student_id INT,
    course_id INT,
    UNIQUE (student_id, course_id),
    FOREIGN KEY (course_id) REFERENCES courses (course_id),
    FOREIGN KEY (student_id) REFERENCES students (student_id)
);


INSERT INTO groups (name, group_year)
VALUES ('DM21', '2002'), ('DM22', '2002'), ('DM31', '2003')
RETURNING *;


INSERT INTO teachers (name, lastname)
VALUES ('Victor', 'Petrov'), ('Sergey', 'Ivanov'), ('Andrey', 'Smirnov')
RETURNING *;


INSERT INTO courses (name, teacher_id)
VALUES ('Math', '1'), ('History', '2'), ('Geography', '2'), ('Physics', '1'), ('English', '3')
RETURNING *;


INSERT INTO students (name, lastname, group_id)
VALUES ('Mae', 'Workman', 1), ('Leona', 'Ahmad', 1), ('Jozef', 'Kavanagh', 1), ('Huseyin', 'Shaw', 1),
('Addison', 'Cook', 1), ('Aaisha', 'Huerta', 1), ('Erica', 'Little', 1), ('Pawel', 'Ryder', 1), ('Effie', 'Adams', 1),
('Kitty', 'Christie', 2), ('Clare', 'Fitzpatrick', 2), ('Arnold', 'Elliott', 2), ('Celine', 'Piper', 2),
('Emmie', 'Robbins', 2), ('Adrian', 'Muir', 2), ('Wanda', 'Mcculloch', 2), ('Iga', 'Murray', 2), ('Arnav', 'Hood', 2),
('Zakariah', 'Prentice', 2), ('Rafi', 'Kaye', 3), ('Milla', 'OGallagher', 3), ('Chad', 'Smyth', 3),
('Elouise', 'Farrow', 3), ('Cameron', 'Huff', 3), ('Leyton', 'Alston', 3), ('Jose', 'Coombes', 3),
('Shyam', 'Buckner', 3), ('Margot', 'Foster', 3), ('Caius', 'Leblanc', 3), ('Morgan', 'Clifford', 3)
RETURNING *;


INSERT INTO marks (student_id, course_id, mark_date, mark_value)
VALUES ('1', '1', '2002-10-12', '5'), ('1', '1', '2002-11-03', '4'), ('1', '1', '2003-01-25', '4'),
('1', '1', '2003-02-14', '5'), ('1', '1', '2003-11-18', '5'), ('1', '1', '2002-12-09', '3'), ('1', '1', '2003-03-13', '4'),
('1', '1', '2003-02-18', '4'), ('1', '3', '2002-10-16', '4'), ('1', '3', '2002-11-27', '5'), ('1', '3', '2003-02-26', '5'),
('1', '3', '2003-05-04', '5'), ('1', '3', '2002-12-12', '5'), ('1', '3', '2003-04-02', '5'), ('1', '5', '2003-02-06', '5'),
('1', '5', '2002-11-26', '4'), ('1', '5', '2002-09-29', '5'), ('1', '5', '2002-10-19', '4'), ('1', '5', '2003-01-30', '4'),
('1', '5', '2003-03-26', '4'), ('2', '1', '2002-10-12', '5'), ('2', '1', '2002-11-03', '4'), ('2', '1', '2003-01-25', '4'),
('2', '3', '2003-02-14', '5'), ('2', '1', '2003-11-18', '5'), ('2', '1', '2002-12-09', '3'), ('2', '1', '2003-03-13', '4'),
('2', '1', '2003-02-18', '4'), ('2', '3', '2002-10-16', '4'), ('2', '3', '2002-11-27', '5'), ('2', '3', '2003-02-26', '5'),
('2', '5', '2003-05-04', '5'), ('2', '5', '2002-12-12', '5'), ('2', '5', '2003-04-02', '5'), ('2', '5', '2003-02-06', '5'),
('2', '5', '2002-11-26', '4'), ('2', '5', '2002-09-29', '5'), ('2', '5', '2002-10-19', '4'), ('2', '3', '2003-01-30', '4'),
('2', '1', '2003-03-26', '4'), ('3', '3', '2002-10-12', '5'), ('3', '3', '2002-11-03', '4'), ('3', '3', '2003-01-25', '4'),
('3', '3', '2003-02-14', '5'), ('3', '1', '2003-11-18', '5'), ('3', '1', '2002-12-09', '3'), ('3', '3', '2003-03-13', '4'),
('3', '3', '2003-02-18', '4'), ('3', '1', '2002-10-16', '4'), ('3', '1', '2002-11-27', '5'), ('3', '1', '2003-02-26', '5'),
('3', '1', '2003-05-04', '5'), ('3', '5', '2002-12-12', '5'), ('3', '5', '2003-04-02', '5'), ('3', '5', '2003-02-06', '5'),
('3', '5', '2002-11-26', '4'), ('3', '5', '2002-09-29', '5'), ('3', '5', '2002-10-19', '4'), ('3', '5', '2003-01-30', '4'),
('3', '5', '2003-03-26', '4'), ('4', '5', '2002-10-12', '5'), ('4', '5', '2002-11-03', '4'), ('4', '5', '2003-01-25', '4'),
('4', '5', '2003-02-14', '5'), ('4', '5', '2003-11-18', '5'), ('4', '5', '2002-12-09', '3'), ('4', '3', '2003-03-13', '4'),
('4', '3', '2003-02-18', '4'), ('4', '3', '2002-10-16', '4'), ('4', '3', '2002-11-27', '5'), ('4', '3', '2003-02-26', '5'),
('4', '3', '2003-05-04', '5'), ('4', '1', '2002-12-12', '5'), ('4', '1', '2003-04-02', '5'), ('4', '3', '2003-02-06', '5'),
('4', '1', '2002-11-26', '4'), ('4', '1', '2002-09-29', '5'), ('4', '1', '2002-10-19', '4'), ('4', '1', '2003-01-30', '4'),
('4', '1', '2003-03-26', '4'), ('5', '1', '2003-03-24', '5'), ('5', '1', '2003-03-22', '5'), ('5', '1', '2003-03-26', '5'),
('5', '1', '2003-03-04', '4'), ('5', '1', '2003-04-01', '4'), ('5', '1', '2003-04-12', '4'), ('5', '3', '2003-04-10', '4'),
('5', '3', '2003-04-16', '4'), ('5', '3', '2002-11-21', '5'), ('5', '3', '2002-11-15', '5'), ('5', '3', '2002-11-28', '5'),
('5', '3', '2002-11-30', '5'), ('5', '3', '2003-03-26', '4'), ('5', '5', '2003-03-26', '4'), ('5', '5', '2003-03-26', '4'),
('5', '3', '2003-03-26', '4'), ('5', '5', '2003-01-18', '4'), ('5', '5', '2003-03-12', '4'), ('5', '5', '2003-03-03', '5'),
('5', '5', '2003-03-30', '5'), ('6', '1', '2003-02-20', '5'), ('6', '1', '2003-03-13', '5'), ('6', '1', '2003-03-11', '5'),
('6', '1', '2003-03-18', '5'), ('6', '1', '2003-03-18', '4'), ('6', '1', '2002-10-14', '3'), ('6', '3', '2002-11-11', '5'),
('6', '3', '2003-01-28', '5'), ('6', '3', '2002-09-15', '5'), ('6', '3', '2002-09-16', '4'), ('6', '3', '2002-09-28', '5'),
('6', '3', '2002-09-30', '5'), ('6', '5', '2002-10-02', '5'), ('6', '5', '2002-10-01', '5'), ('6', '3', '2002-10-03', '5'),
('6', '5', '2002-10-04', '5'), ('6', '5', '2002-11-30', '5'), ('6', '5', '2002-11-29', '4'), ('6', '5', '2002-10-30', '5'),
('6', '5', '2002-12-30', '5'), ('7', '1', '2002-11-21', '5'), ('7', '1', '2002-11-22', '5'), ('7', '1', '2002-11-23', '5'),
('7', '1', '2002-11-24', '5'), ('7', '1', '2002-12-01', '5'), ('7', '1', '2002-12-02', '5'), ('7', '1', '2002-12-03', '5'),
('7', '3', '2002-12-04', '5'), ('7', '3', '2002-12-11', '5'), ('7', '3', '2002-12-14', '5'), ('7', '3', '2002-12-15', '5'),
('7', '3', '2002-12-16', '5'), ('7', '3', '2003-02-15', '5'), ('7', '3', '2003-02-16', '5'), ('7', '5', '2003-02-17', '5'),
('7', '5', '2003-02-18', '5'), ('7', '5', '2003-03-15', '5'), ('7', '5', '2003-03-17', '5'), ('7', '5', '2003-03-18', '5'),
('7', '5', '2003-03-19', '5'), ('8', '1', '2003-04-15', '4'), ('8', '1', '2003-04-16', '4'), ('8', '1', '2003-04-17', '4'),
('8', '1', '2003-04-18', '4'), ('8', '1', '2003-05-15', '4'), ('8', '1', '2003-05-15', '4'), ('8', '1', '2003-05-15', '4'),
('8', '1', '2003-05-15', '4'), ('8', '3', '2003-01-02', '4'), ('8', '3', '2003-01-05', '4'), ('8', '3', '2003-01-06', '4'),
('8', '3', '2003-01-07', '4'), ('8', '3', '2003-02-02', '4'), ('8', '3', '2003-02-07', '4'), ('8', '5', '2003-02-08', '4'),
('8', '5', '2003-02-09', '4'), ('8', '5', '2003-03-02', '4'), ('8', '5', '2003-03-04', '4'), ('8', '5', '2003-03-05', '4'),
('8', '5', '2003-03-06', '4'), ('9', '1', '2003-03-11', '3'), ('9', '1', '2003-03-12', '3'), ('9', '1', '2003-03-13', '3'),
('9', '1', '2003-03-14', '3'), ('9', '1', '2003-04-26', '3'), ('9', '3', '2003-04-27', '3'), ('9', '3', '2003-04-28', '3'),
('9', '3', '2003-04-25', '3'), ('9', '3', '2003-04-01', '3'), ('9', '3', '2003-04-02', '3'), ('9', '3', '2003-04-03', '3'),
('9', '3', '2003-04-04', '3'), ('9', '5', '2003-04-06', '3'), ('9', '5', '2003-04-07', '3'), ('9', '5', '2003-04-08', '3'),
('9', '1', '2003-04-09', '3'), ('9', '5', '2003-05-06', '3'), ('9', '5', '2003-05-07', '3'), ('9', '5', '2003-05-08', '3'),
('9', '5', '2003-05-09', '3'), ('10', '1', '2002-10-04', '5'), ('10', '1', '2002-10-05', '5'), ('10', '1', '2002-10-06', '5'),
('10', '1', '2002-10-07', '5'), ('10', '2', '2002-10-12', '5'), ('10', '2', '2002-10-13', '5'), ('10', '2', '2002-10-14', '5'),
('10', '2', '2002-10-15', '5'), ('10', '1', '2002-11-11', '5'), ('10', '1', '2002-11-12', '5'), ('10', '2', '2002-11-13', '5'),
('10', '2', '2002-11-14', '5'), ('10', '4', '2002-12-11', '5'), ('10', '4', '2002-12-12', '5'), ('10', '4', '2002-12-13', '5'),
('10', '4', '2002-12-14', '5'), ('10', '4', '2002-12-21', '5'), ('10', '5', '2002-12-22', '5'), ('10', '5', '2002-12-23', '5'),
('10', '1', '2002-12-24', '5'), ('11', '1', '2002-09-15', '5'), ('11', '4', '2002-09-16', '4'), ('11', '4', '2002-09-17', '5'),
('11', '1', '2002-09-18', '5'), ('11', '2', '2002-09-25', '5'), ('11', '2', '2002-09-26', '5'), ('11', '2', '2002-09-27', '5'),
('11', '2', '2002-09-28', '5'), ('11', '1', '2002-10-25', '5'), ('11', '1', '2002-10-26', '5'), ('11', '2', '2002-10-27', '5'),
('11', '2', '2002-10-28', '5'), ('11', '4', '2002-10-06', '5'), ('11', '4', '2002-10-07', '5'), ('11', '4', '2002-10-08', '5'),
('11', '4', '2002-10-09', '4'), ('11', '4', '2002-10-18', '5'), ('11', '4', '2002-10-19', '5'), ('11', '1', '2002-10-20', '5'),
('11', '2', '2002-10-21', '5'), ('12', '1', '2002-10-14', '5'), ('12', '1', '2002-10-15', '5'), ('12', '1', '2002-10-16', '4'),
('12', '1', '2002-10-17', '4'), ('12', '2', '2002-10-20', '4'), ('12', '2', '2002-10-21', '5'), ('12', '2', '2002-10-22', '5'),
('12', '2', '2002-10-23', '5'), ('12', '1', '2002-11-20', '5'), ('12', '1', '2002-11-21', '4'), ('12', '1', '2002-11-22', '5'),
('12', '1', '2002-11-22', '5'), ('12', '4', '2002-11-04', '5'), ('12', '4', '2002-11-05', '4'), ('12', '4', '2002-11-06', '4'),
('12', '4', '2002-11-07', '5'), ('12', '2', '2002-12-04', '5'), ('12', '2', '2002-12-05', '5'), ('12', '4', '2002-12-06', '5'),
('12', '4', '2002-12-07', '5'), ('13', '1', '2003-02-20', '5'), ('13', '1', '2003-03-13', '3'), ('13', '1', '2003-03-11', '3'),
('13', '1', '2003-03-18', '4'), ('13', '2', '2003-03-18', '4'), ('13', '2', '2002-10-14', '4'), ('13', '2', '2002-11-11', '4'),
('13', '2', '2003-01-28', '4'), ('13', '2', '2002-09-15', '3'), ('13', '2', '2002-09-16', '3'), ('13', '2', '2002-09-28', '3'),
('13', '1', '2002-09-30', '3'), ('13', '4', '2002-10-02', '4'), ('13', '4', '2002-10-01', '4'), ('13', '4', '2002-10-03', '5'),
('13', '4', '2002-10-04', '4'), ('13', '4', '2002-11-30', '3'), ('13', '4', '2002-11-29', '4'), ('13', '4', '2002-10-30', '3'),
('13', '2', '2002-12-30', '4'), ('14', '1', '2003-02-20', '5'), ('14', '1', '2003-03-13', '5'), ('14', '1', '2003-03-11', '5'),
('14', '1', '2003-03-18', '5'), ('14', '2', '2003-03-18', '4'), ('14', '2', '2002-10-14', '3'), ('14', '2', '2002-11-11', '5'),
('14', '2', '2003-01-28', '5'), ('14', '2', '2002-09-15', '5'), ('14', '2', '2002-09-16', '4'), ('14', '1', '2002-09-28', '5'),
('14', '1', '2002-09-30', '5'), ('14', '4', '2002-10-02', '5'), ('14', '4', '2002-10-01', '5'), ('14', '4', '2002-10-03', '5'),
('14', '4', '2002-10-04', '5'), ('14', '4', '2002-11-30', '5'), ('14', '4', '2002-11-29', '4'), ('14', '4', '2002-10-30', '5'),
('14', '2', '2002-12-30', '5'), ('15', '1', '2003-02-20', '4'), ('15', '1', '2003-03-13', '4'), ('15', '1', '2003-03-11', '5'),
('15', '1', '2003-03-18', '5'), ('15', '2', '2003-03-18', '4'), ('15', '2', '2002-10-14', '3'), ('15', '2', '2002-11-11', '5'),
('15', '2', '2003-01-28', '4'), ('15', '1', '2002-09-15', '5'), ('15', '1', '2002-09-16', '4'), ('15', '2', '2002-09-28', '5'),
('15', '2', '2002-09-30', '4'), ('15', '4', '2002-10-02', '4'), ('15', '4', '2002-10-01', '5'), ('15', '4', '2002-10-03', '5'),
('15', '4', '2002-10-04', '5'), ('15', '4', '2002-11-30', '5'), ('15', '4', '2002-11-29', '4'), ('15', '4', '2002-10-30', '5'),
('15', '1', '2002-12-30', '5'), ('16', '1', '2003-02-20', '5'), ('16', '1', '2003-03-13', '5'), ('16', '1', '2003-03-11', '5'),
('16', '1', '2003-03-18', '5'), ('16', '2', '2003-03-18', '5'), ('16', '2', '2002-10-14', '5'), ('16', '2', '2002-11-11', '5'),
('16', '2', '2003-01-28', '5'), ('16', '1', '2002-09-15', '5'), ('16', '1', '2002-09-16', '4'), ('16', '1', '2002-09-28', '5'),
('16', '2', '2002-09-30', '5'), ('16', '4', '2002-10-02', '5'), ('16', '4', '2002-10-01', '5'), ('16', '4', '2002-10-03', '5'),
('16', '4', '2002-10-04', '5'), ('16', '2', '2002-11-30', '5'), ('16', '4', '2002-11-29', '5'), ('16', '4', '2002-10-30', '5'),
('16', '2', '2002-12-30', '5'), ('17', '1', '2003-02-20', '4'), ('17', '1', '2003-03-13', '4'), ('17', '1', '2003-03-11', '4'),
('17', '1', '2003-03-18', '5'), ('17', '2', '2003-03-18', '4'), ('17', '2', '2002-10-14', '4'), ('17', '2', '2002-11-11', '5'),
('17', '2', '2003-01-28', '5'), ('17', '1', '2002-09-15', '5'), ('17', '1', '2002-09-16', '4'), ('17', '1', '2002-09-28', '4'),
('17', '2', '2002-09-30', '5'), ('17', '4', '2002-10-02', '4'), ('17', '4', '2002-10-01', '5'), ('17', '4', '2002-10-03', '5'),
('17', '4', '2002-10-04', '5'), ('17', '4', '2002-11-30', '5'), ('17', '4', '2002-11-29', '4'), ('17', '4', '2002-10-30', '5'),
('17', '2', '2002-12-30', '4'), ('18', '1', '2003-02-20', '5'), ('18', '1', '2003-03-13', '5'), ('18', '1', '2003-03-11', '5'),
('18', '1', '2003-03-18', '5'), ('18', '2', '2003-03-18', '5'), ('18', '2', '2002-10-14', '5'), ('18', '2', '2002-11-11', '5'),
('18', '2', '2003-01-28', '5'), ('18', '1', '2002-09-15', '5'), ('18', '1', '2002-09-16', '5'), ('18', '2', '2002-09-28', '5'),
('18', '2', '2002-09-30', '5'), ('18', '4', '2002-10-02', '5'), ('18', '4', '2002-10-01', '5'), ('18', '4', '2002-10-03', '5'),
('18', '4', '2002-10-04', '5'), ('18', '1', '2002-11-30', '5'), ('18', '4', '2002-11-29', '4'), ('18', '4', '2002-10-30', '5'),
('18', '2', '2002-12-30', '5'), ('19', '1', '2003-02-20', '3'), ('19', '1', '2003-03-13', '5'), ('19', '1', '2003-03-11', '4'),
('19', '1', '2003-03-18', '5'), ('19', '2', '2003-03-18', '4'), ('19', '2', '2002-10-14', '3'), ('19', '2', '2002-11-11', '5'),
('19', '2', '2003-01-28', '5'), ('19', '1', '2002-09-15', '4'), ('19', '1', '2002-09-16', '4'), ('19', '2', '2002-09-28', '5'),
('19', '2', '2002-09-30', '4'), ('19', '4', '2002-10-02', '3'), ('19', '4', '2002-10-01', '5'), ('19', '4', '2002-10-03', '3'),
('19', '4', '2002-10-04', '5'), ('19', '4', '2002-11-30', '4'), ('19', '4', '2002-11-29', '4'), ('19', '4', '2002-10-30', '5'),
('19', '1', '2002-12-30', '4'), ('20', '2', '2003-02-20', '5'), ('20', '2', '2003-03-13', '5'), ('20', '2', '2003-03-11', '5'),
('20', '3', '2003-03-18', '5'), ('20', '2', '2003-03-18', '5'), ('20', '2', '2002-10-14', '5'), ('20', '2', '2002-11-11', '5'),
('20', '2', '2003-01-28', '5'), ('20', '3', '2002-09-15', '5'), ('20', '3', '2002-09-16', '5'), ('20', '3', '2002-09-28', '5'),
('20', '3', '2002-09-30', '5'), ('20', '3', '2002-10-02', '5'), ('20', '3', '2002-10-01', '5'), ('20', '5', '2002-10-03', '5'),
('20', '5', '2002-10-04', '5'), ('20', '5', '2002-11-30', '5'), ('20', '5', '2002-11-29', '5'), ('20', '5', '2002-10-30', '5'),
('20', '5', '2002-12-30', '5'), ('21', '2', '2003-02-20', '5'), ('21', '2', '2003-03-13', '5'), ('21', '2', '2003-03-11', '5'),
('21', '3', '2003-03-18', '5'), ('21', '2', '2003-03-18', '4'), ('21', '2', '2002-10-14', '5'), ('21', '2', '2002-11-11', '5'),
('21', '2', '2003-01-28', '5'), ('21', '3', '2002-09-15', '5'), ('21', '3', '2002-09-16', '5'), ('21', '3', '2002-09-28', '5'),
('21', '3', '2002-09-30', '5'), ('21', '3', '2002-10-02', '5'), ('21', '3', '2002-10-01', '4'), ('21', '5', '2002-10-03', '5'),
('21', '5', '2002-10-04', '5'), ('21', '5', '2002-11-30', '5'), ('21', '5', '2002-11-29', '5'), ('21', '5', '2002-10-30', '4'),
('21', '5', '2002-12-30', '5'), ('22', '2', '2003-02-20', '4'), ('22', '2', '2003-03-13', '5'), ('22', '2', '2003-03-11', '5'),
('22', '3', '2003-03-18', '5'), ('22', '2', '2003-03-18', '5'), ('22', '2', '2002-10-14', '4'), ('22', '2', '2002-11-11', '5'),
('22', '2', '2003-01-28', '4'), ('22', '3', '2002-09-15', '5'), ('22', '3', '2002-09-16', '5'), ('22', '3', '2002-09-28', '5'),
('22', '3', '2002-09-30', '5'), ('22', '3', '2002-10-02', '4'), ('22', '3', '2002-10-01', '4'), ('22', '5', '2002-10-03', '5'),
('22', '5', '2002-10-04', '5'), ('22', '5', '2002-11-30', '5'), ('22', '5', '2002-11-29', '4'), ('22', '5', '2002-10-30', '5'),
('22', '5', '2002-12-30', '5'), ('23', '2', '2003-02-20', '4'), ('23', '2', '2003-03-13', '5'), ('23', '2', '2003-03-11', '4'),
('23', '3', '2003-03-18', '5'), ('23', '2', '2003-03-18', '3'), ('23', '2', '2002-10-14', '4'), ('23', '2', '2002-11-11', '5'),
('23', '2', '2003-01-28', '5'), ('23', '3', '2002-09-15', '5'), ('23', '3', '2002-09-16', '5'), ('23', '3', '2002-09-28', '5'),
('23', '3', '2002-09-30', '3'), ('23', '3', '2002-10-02', '3'), ('23', '3', '2002-10-01', '5'), ('23', '5', '2002-10-03', '4'),
('23', '5', '2002-10-04', '5'), ('23', '5', '2002-11-30', '5'), ('23', '5', '2002-11-29', '3'), ('23', '5', '2002-10-30', '5'),
('23', '5', '2002-12-30', '4'), ('24', '2', '2003-02-20', '4'), ('24', '2', '2003-03-13', '5'), ('24', '2', '2003-03-11', '4'),
('24', '3', '2003-03-18', '4'), ('24', '2', '2003-03-18', '5'), ('24', '2', '2002-10-14', '4'), ('24', '2', '2002-11-11', '5'),
('24', '2', '2003-01-28', '4'), ('24', '3', '2002-09-15', '5'), ('24', '3', '2002-09-16', '5'), ('24', '3', '2002-09-28', '4'),
('24', '3', '2002-09-30', '5'), ('24', '3', '2002-10-02', '5'), ('24', '3', '2002-10-01', '4'), ('24', '5', '2002-10-03', '4'),
('24', '5', '2002-10-04', '5'), ('24', '5', '2002-11-30', '4'), ('24', '5', '2002-11-29', '4'), ('24', '5', '2002-10-30', '5'),
('24', '5', '2002-12-30', '4'), ('25', '2', '2003-02-20', '5'), ('25', '2', '2003-03-13', '5'), ('25', '2', '2003-03-11', '5'),
('25', '3', '2003-03-18', '5'), ('25', '2', '2003-03-18', '4'), ('25', '2', '2002-10-14', '5'), ('25', '2', '2002-11-11', '5'),
('25', '2', '2003-01-28', '5'), ('25', '3', '2002-09-15', '5'), ('25', '3', '2002-09-16', '5'), ('25', '3', '2002-09-28', '5'),
('25', '3', '2002-09-30', '5'), ('25', '3', '2002-10-02', '4'), ('25', '3', '2002-10-01', '5'), ('25', '5', '2002-10-03', '5'),
('25', '5', '2002-10-04', '5'), ('25', '5', '2002-11-30', '4'), ('25', '5', '2002-11-29', '5'), ('25', '5', '2002-10-30', '5'),
('25', '5', '2002-12-30', '5'), ('26', '2', '2003-02-20', '5'), ('26', '2', '2003-03-13', '5'), ('26', '2', '2003-03-11', '5'),
('26', '3', '2003-03-18', '5'), ('26', '2', '2003-03-18', '5'), ('26', '2', '2002-10-14', '5'), ('26', '2', '2002-11-11', '5'),
('26', '2', '2003-01-28', '5'), ('26', '3', '2002-09-15', '3'), ('26', '3', '2002-09-16', '3'), ('26', '3', '2002-09-28', '3'),
('26', '3', '2002-09-30', '5'), ('26', '3', '2002-10-02', '5'), ('26', '3', '2002-10-01', '5'), ('26', '5', '2002-10-03', '5'),
('26', '5', '2002-10-04', '5'), ('26', '5', '2002-11-30', '5'), ('26', '5', '2002-11-29', '3'), ('26', '5', '2002-10-30', '5'),
('26', '5', '2002-12-30', '5'), ('27', '2', '2003-02-20', '5'), ('27', '2', '2003-03-13', '5'), ('27', '2', '2003-03-11', '5'),
('27', '3', '2003-03-18', '5'), ('27', '2', '2003-03-18', '5'), ('27', '2', '2002-10-14', '5'), ('27', '2', '2002-11-11', '5'),
('27', '2', '2003-01-28', '5'), ('27', '3', '2002-09-15', '5'), ('27', '3', '2002-09-16', '5'), ('27', '3', '2002-09-28', '5'),
('27', '3', '2002-09-30', '5'), ('27', '3', '2002-10-02', '4'), ('27', '3', '2002-10-01', '5'), ('27', '5', '2002-10-03', '5'),
('27', '5', '2002-10-04', '5'), ('27', '5', '2002-11-30', '5'), ('27', '5', '2002-11-29', '5'), ('27', '5', '2002-10-30', '5'),
('27', '5', '2002-12-30', '5'), ('28', '2', '2003-02-20', '5'), ('28', '2', '2003-03-13', '4'), ('28', '2', '2003-03-11', '5'),
('28', '3', '2003-03-18', '4'), ('28', '2', '2003-03-18', '5'), ('28', '2', '2002-10-14', '5'), ('28', '2', '2002-11-11', '5'),
('28', '2', '2003-01-28', '5'), ('28', '3', '2002-09-15', '5'), ('28', '3', '2002-09-16', '5'), ('28', '3', '2002-09-28', '4'),
('28', '3', '2002-09-30', '5'), ('28', '3', '2002-10-02', '4'), ('28', '3', '2002-10-01', '5'), ('28', '5', '2002-10-03', '5'),
('28', '5', '2002-10-04', '5'), ('28', '5', '2002-11-30', '5'), ('28', '5', '2002-11-29', '5'), ('28', '5', '2002-10-30', '5'),
('28', '5', '2002-12-30', '5'), ('29', '2', '2003-02-20', '5'), ('29', '2', '2003-03-13', '5'), ('29', '2', '2003-03-11', '4'),
('29', '3', '2003-03-18', '5'), ('29', '2', '2003-03-18', '5'), ('29', '2', '2002-10-14', '5'), ('29', '2', '2002-11-11', '5'),
('29', '2', '2003-01-28', '5'), ('29', '3', '2002-09-15', '5'), ('29', '3', '2002-09-16', '5'), ('29', '3', '2002-09-28', '5'),
('29', '3', '2002-09-30', '4'), ('29', '3', '2002-10-02', '5'), ('29', '3', '2002-10-01', '5'), ('29', '5', '2002-10-03', '5'),
('29', '5', '2002-10-04', '5'), ('29', '5', '2002-11-30', '5'), ('29', '5', '2002-11-29', '5'), ('29', '5', '2002-10-30', '5'),
('29', '5', '2002-12-30', '5'), ('30', '2', '2003-02-20', '5'), ('30', '2', '2003-03-13', '5'), ('30', '2', '2003-03-11', '5'),
('30', '3', '2003-03-18', '5'), ('30', '2', '2003-03-18', '5'), ('30', '2', '2002-10-14', '5'), ('30', '2', '2002-11-11', '5'),
('30', '2', '2003-01-28', '5'), ('30', '3', '2002-09-15', '5'), ('30', '3', '2002-09-16', '5'), ('30', '3', '2002-09-28', '5'),
('30', '3', '2002-09-30', '5'), ('30', '3', '2002-10-02', '5'), ('30', '3', '2002-10-01', '5'), ('30', '5', '2002-10-03', '5'),
('30', '5', '2002-10-04', '5'), ('30', '5', '2002-11-30', '5'), ('30', '5', '2002-11-29', '5'), ('30', '5', '2002-10-30', '5'),
('30', '5', '2002-12-30', '5')
RETURNING *;


INSERT INTO student_courses (student_id, course_id)
VALUES ('1', '1'), ('1', '3'), ('1', '5'), ('2', '1'), ('2', '3'), ('2', '5'), ('3', '1'), ('3', '3'), ('3', '5'),
('4', '1'), ('4', '3'), ('4', '5'), ('5', '1'), ('5', '3'), ('5', '5'), ('6', '1'), ('6', '3'), ('6', '5'),
('7', '1'), ('7', '3'), ('7', '5'), ('8', '1'), ('8', '3'), ('8', '5'), ('9', '1'), ('9', '3'), ('9', '5'),
('10', '1'), ('10', '2'), ('10', '4'), ('11', '1'), ('11', '2'), ('11', '4'), ('12', '1'), ('12', '2'), ('12', '4'),
('13', '1'), ('13', '2'), ('13', '4'), ('14', '1'), ('14', '2'), ('14', '4'), ('15', '1'), ('15', '2'), ('15', '4'),
('16', '1'), ('16', '2'), ('16', '4'), ('17', '1'), ('17', '2'), ('17', '4'), ('18', '1'), ('18', '2'), ('18', '4'),
('19', '1'), ('19', '2'), ('19', '4'), ('20', '2'), ('20', '3'), ('20', '5'), ('21', '2'), ('21', '3'), ('21', '5'),
('22', '2'), ('22', '3'), ('22', '5'), ('23', '2'), ('23', '3'), ('23', '5'), ('24', '2'), ('24', '3'), ('24', '5'),
('25', '2'), ('25', '3'), ('25', '5'), ('26', '2'), ('26', '3'), ('26', '5'), ('27', '2'), ('27', '3'), ('27', '5'),
('28', '2'), ('28', '3'), ('28', '5'), ('29', '2'), ('29', '3'), ('29', '5'), ('30', '2'), ('30', '3'), ('30', '5')
RETURNING *;


--5 студентов с наибольшим средним баллом по всем предметам
select  marks.student_id, name, lastname, avg(mark_value) as avg_mark
from marks
join students on students.student_id = marks.student_id
group by marks.student_id, name, lastname
order by avg_mark desc limit 5;


--1 студент с наивысшим средним баллом по одному предмету
select  marks.student_id, students.name, lastname, courses.name, avg(mark_value) as avg_mark
from marks
join students on students.student_id = marks.student_id
join courses on courses.course_id = marks.course_id
where courses.name = 'English'
group by marks.student_id, students.name, lastname, marks.course_id, courses.name
order by avg_mark desc limit 1;


--средний балл в группе по одному предмету.
select marks.course_id, groups.name as group_name, courses.name as course_name, avg(mark_value) as avg_mark
from marks
join students on students.student_id = marks.student_id
join courses on courses.course_id = marks.course_id
join groups on students.group_id = groups.group_id
where courses.name = 'History' and groups.name = 'DM31'
group by group_name, marks.course_id, course_name;


--Средний балл в потоке.
select  groups.group_year, avg(mark_value) as avg_mark
from marks
join students on students.student_id = marks.student_id
join courses on courses.course_id = marks.course_id
join groups on students.group_id = groups.group_id
where  groups.group_year = '2002';


--Какие курсы читает преподаватель.
select concat(teacher.name, ' ', teacher.lastname) as teacher_fullname, courses.name as course_name
from teacher
join courses on courses.teacher_id = teacher.teacher_id
where concat(teacher.name, ' ', teacher.lastname)='Sergey Ivanov';


--Список студентов в группе.
select groups.name as group_name, concat(students.name, ' ', students.lastname) as student_fullname
from groups
join students  on students.group_id = groups.group_id
where groups.name = 'DM22';


--Оценки студентов в группе по предмету.
select concat(students.name, ' ', students.lastname) as student_fullname, groups.name as group_name, courses.name as coutrse_name, mark_value
from marks
join students on students.student_id = marks.student_id
join courses on courses.course_id = marks.course_id
join groups on students.group_id = groups.group_id
where groups.name = 'DM21' and courses.name = 'Geography';


--Оценки студентов в группе по предмету на последнем занятии.
select concat(students.name, ' ', students.lastname) as student_fullname, groups.name as group_name, courses.name as course_name, mark_value, mark_date
from marks
join students on students.student_id = marks.student_id
join courses on courses.course_id = marks.course_id
join groups on students.group_id = groups.group_id
where groups.name = 'DM21' and  courses.name = 'Math' and mark_date = (select max(mark_date) from marks)
order by mark_date desc ;


--Список курсов, которые посещает студент.
select concat(students."name",' ', students.lastname), c.name as course_name
from students
join student_courses sc on sc.student_id = students.student_id
join courses c on c.course_id = sc.course_id
where concat(students."name",' ', students.lastname) = 'Cameron Huff';


--Список курсов, которые студенту читает преподаватель.
select concat(students."name",' ', students.lastname) as student_name, c.name as course_name, concat(teacher."name",' ', teacher.lastname) as teacher_name
from students
join student_courses sc on sc.student_id = students.student_id
join courses c on c.course_id = sc.course_id
join teacher on teacher.teacher_id = c.teacher_id
where concat(students."name",' ', students.lastname) = 'Cameron Huff' and concat(teacher."name",' ', teacher.lastname) = 'Sergey Ivanov';


--Средний балл, который преподаватель ставит студенту.
select concat(students.name,' ', students.lastname) as student_name, concat(teacher.name,' ', teacher.lastname) as teacher_name, avg(mark_value) as avg_mark
from marks
join students on students.student_id = marks.student_id
join courses c on c.course_id = marks.course_id
join teacher on teacher.teacher_id = c.teacher_id
where concat(students.name,' ', students.lastname) = 'Cameron Huff' and concat(teacher.name,' ', teacher.lastname) = 'Sergey Ivanov'
group by marks.student_id, students.name, students.lastname, teacher."name" , teacher.lastname;


--Средний балл, который ставит преподаватель.
select concat(teacher.name,' ', teacher.lastname) as teacher_name, avg(mark_value) as avg_mark
from marks
join courses c on c.course_id = marks.course_id
join teacher on teacher.teacher_id = c.teacher_id
where concat(teacher.name,' ', teacher.lastname) = 'Andrey Smirnov'
group by teacher."name" , teacher.lastname;