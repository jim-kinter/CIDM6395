-- the follwoing line to disable FK checks. 
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;

CREATE SCHEMA IF NOT EXISTS construction_db;
USE construction_db  ;

CREATE TABLE USER (
  USER_ID int NOT NULL AUTO_INCREMENT,
  DEPARTMENT_ID int NOT NULL,
  ROLE_ID int not null,
  FirstName varchar(30)  NOT NULL,
  LastName varchar(30)  NOT NULL,
  PhoneNumber varchar(25),
  EMailAddress varchar(50),
  PRIMARY KEY (USER_ID)
  );

CREATE TABLE ROLE (
	ROLE_ID int NOT NULL AUTO_INCREMENT,
    Name varchar(25) NOT NULL,
    IsProjectControls boolean NOT NULL DEFAULT 0,
    IsSysAdmin boolean NOT NULL DEFAULT 0,
    PRIMARY KEY (ROLE_ID)
);

CREATE TABLE COMPANY (
	COMPANY_ID int NOT NULL AUTO_INCREMENT,
    Name varchar(100),
    PRIMARY KEY (COMPANY_ID)
);

CREATE TABLE DEPARTMENT (
	DEPARTMENT_ID int NOT NULL AUTO_INCREMENT,
    COMPANY_ID int NOT NULL,
    Name varchar(100),
    PRIMARY KEY (DEPARTMENT_ID)
);

CREATE TABLE PROJECT_CONTROLS (
	PC_ID int NOT NULL AUTO_INCREMENT,
    SUBTYPE_ID int NOT NULL,
    PRIMARY KEY (PC_ID)
);

CREATE TABLE SYSTEM_ADMIN (
	SA_ID int NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (SA_ID)
);

CREATE TABLE CONSTRAINT_MANAGER (
	CM_ID int NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (CM_ID)
);

CREATE TABLE STANDARD_USER (
	SU_ID int NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (SU_ID)
);


    


/******************************************************************

CREATE TABLE IF NOT EXISTS departments (     
         DepID       INT      NOT NULL,
         DName     TEXT   NULL        DEFAULT NULL, 
         Phone       TEXT   NULL        DEFAULT NULL, 
        College      TEXT   NULL        DEFAULT NULL,
        PRIMARY KEY (DepID )

	-- we can add FKs here, will do that later
);

CREATE TABLE courses (
  courseid             VARCHAR(9)                NOT NULL,
  Cname		TEXT   	      NOT NULL,
  Description         TEXT ,
  CONSTRAINT CoursePK PRIMARY KEY (courseid)

-- we can add FKs like DepID here, will do that later
  );
  
  CREATE TABLE IF NOT EXISTS professors (
         ProfID       INT     NOT NULL,  
         Profname  TEXT   NULL           DEFAULT NULL,
         email         TEXT   NULL           DEFAULT NULL, 
         PRIMARY KEY (ProfID) 
       
         -- we can add FKs like DepID here, will do that later

  );
  


ALTER TABLE courses 
      ADD COLUMN departments_DepID   INT        NOT NULL AFTER  Description ; -- add the FK column first
      
ALTER TABLE courses 
      ADD CONSTRAINT  fk_courses_departments     FOREIGN KEY ( departments_DepID)           
            REFERENCES  departments ( DepID)    ;

-- exercise 1 naswer
ALTER TABLE  Departments 
      ADD COLUMN  professors_ProfID_Head  INT   NULL  DEFAULT NULL AFTER  College ,
      ADD CONSTRAINT  fk_Heads  FOREIGN KEY (professors_ProfID_Head)  
      REFERENCES  professors (ProfID)  ;
      
-- Exercise 2
-- Affiliated (1-M) : Department-Professor
ALTER TABLE  professors 
      ADD COLUMN  AffDepartments_DepID  INT   NULL  DEFAULT NULL AFTER  email ,
      ADD CONSTRAINT  fk_Affiliated_dep  FOREIGN KEY (AffDepartments_DepID)  
      REFERENCES  departments (DepID)  ;

-- Minor-In (1-M): Department-Student
ALTER TABLE  students 
      ADD COLUMN  departments_DepID_Minor  INT   NULL  DEFAULT NULL AFTER  ssn ,
      ADD CONSTRAINT  Minor_dep  FOREIGN KEY (departments_DepID_Minor)  
      REFERENCES  departments (DepID)  ;

-- Major-In (1-M): Department-Student
ALTER TABLE  students 
      ADD COLUMN  departments_DepID_Major  INT   NULL  DEFAULT NULL AFTER  ssn ,
      ADD CONSTRAINT  Major_dep  FOREIGN KEY (departments_DepID_Major)  
      REFERENCES  departments (DepID)  ;
  

      
CREATE TABLE IF NOT EXISTS  Enrolls_In  (
       students_id               INT                    NOT NULL,  
       courses_CourseID   VARCHAR(9)    NOT NULL,
       Grade                       DECIMAL         NULL,
       Semester                  VARCHAR(7)    NULL, 
       Year                         VARCHAR(4)    NULL,  
       PRIMARY KEY (  students_id,  courses_CourseID),

      CONSTRAINT   fk_students_courses_student     FOREIGN KEY (students_id)    
           REFERENCES   students  ( id )   , 
      CONSTRAINT  fk_students_courses_course     FOREIGN KEY (courses_CourseID)
          REFERENCES  courses ( CourseID )   
);

-- Adding department:
INSERT INTO departments (DepID,  DName,  Phone,  College ,  professors_ProfID_Head) 
VALUES (1,'Department of Accounting, Economics and Finance','449-390-4226','Paul and Virginia Engler College of Business',NULL);

-- Adding Student record: major in department with id=1
INSERT INTO students (id,  first_name,  last_name,  email,  gender,  DoB,  Address,  SSN,  departments_DepID_Minor,  departments_DepID_Major) 
VALUES (1,'Eldridge','Mitchely','emitchely0@bing.com','Male','1985-12-09 00:00:00','3 Morning Place','ooo-03-1314', NULL,1);

-- Adding Course: (assuming this course is offered by department with id=1)
INSERT INTO courses  (CourseID,  Cname,  Description,  departments_DepID) 
  VALUES ('ACCT-5038','Cross-platform asymmetric structure', 'embrace global supply-chains, orchestrate proactive e-markets.',1);

-- Adding Professor:
INSERT INTO professors (ProfID,  Profname,  email,  AffDepartments_DepID)
VALUES (1,'Lyndell Coche','lcoche0@whitehouse.gov',NULL);
-- Making Student whose Id=1 enroll in course which id='ACCT-5038‘ in spring 2011, with no grade
INSERT INTO enrolls_in (students_id,  courses_CourseID ,  Grade ,  Semester ,  `Year`) 
VALUES (1,'ACCT-5038',NULL,'Spring','2011');

Select * from students;
Select * from courses;
Select * from professors;
Select * from departments;
Select * from enrolls_in;


-- the follwoing line to set back FK checks. 
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;