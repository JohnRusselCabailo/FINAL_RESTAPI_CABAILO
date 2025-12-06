CREATE DATABASE IF NOT EXISTS gymdb;
USE gymdb;


CREATE TABLE IF NOT EXISTS memberships (
    membership_id INT AUTO_INCREMENT PRIMARY KEY,
    membership_type VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2),
    duration_months INT
);

CREATE TABLE IF NOT EXISTS workouts (
    workout_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    workout_type VARCHAR(50),
    duration INT
);

CREATE TABLE IF NOT EXISTS member (
    memberId INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    membership_id INT,
    Memberships_membership_id INT,
    Workouts_workout_id INT,
    FOREIGN KEY (Memberships_membership_id) REFERENCES memberships(membership_id),
    FOREIGN KEY (Workouts_workout_id) REFERENCES workouts(workout_id)
);

ALTER TABLE workouts ADD CONSTRAINT fk_member FOREIGN KEY (member_id) REFERENCES members(memberId);

INSERT INTO memberships (membership_type, price, duration_months) VALUES
('Regular', 60.00, 1),
('Student', 50.00, 2),
('Senior', 40.00, 3);

INSERT INTO workouts (member_id, workout_type, duration) VALUES
(1, 'Cardio', 1),
(2, 'Push', 2),
(3, 'Pull', 3),
(4, 'Legs', 4);

INSERT INTO members (first_name, last_name, membership_id, Memberships_membership_id, Workouts_workout_id) VALUES
('John', 'Doe', 1, 1, 1),
('Jane', 'Smith', 2, 2, 2);

SELECT 'Database initialized successfully!' AS Status;
