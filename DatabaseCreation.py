import sqlite3
import pandas as pd
import os

def setup_database(cursor: sqlite3.Cursor):

	cursor.execute("PRAGMA foreign_keys = ON")

	cursor.executescript(
		"""
		CREATE TABLE IF NOT EXISTS inspections (
			inspection_id INTEGER PRIMARY KEY,
			license_number REAL,
			dba_name TEXT,
			risk TEXT,
			inspection_date DATETIME,
			inspection_type TEXT,
			results TEXT,
			facility_type TEXT,
			address TEXT,
			zip INTEGER,
			city TEXT,
			state TEXT,
			latitude REAL,
			longitude REAL,
			location TEXT
		);

		CREATE TABLE IF NOT EXISTS violations (
			violation_id INTEGER PRIMARY KEY AUTOINCREMENT,
			inspection_id INTEGER,
			violations TEXT,
			FOREIGN KEY (inspection_id) REFERENCES inspections (inspection_id)
		);

		CREATE TABLE IF NOT EXISTS licenses (
			license_number REAL PRIMARY KEY,
			dba_name TEXT,
			inspection_date TEXT
		);

		CREATE TABLE IF NOT EXISTS other_names (
			license_number REAL,
			aka_name TEXT,
			PRIMARY KEY (license_number, aka_name)
		);

		CREATE VIEW IF NOT EXISTS license_view AS
			SELECT license_number,
				dba_name,
				inspection_date
			FROM licenses;

		CREATE TRIGGER IF NOT EXISTS license_upsert
		INSTEAD OF INSERT ON license_view
		FOR EACH ROW
		BEGIN
			INSERT INTO licenses (
				license_number,
				dba_name,
				inspection_date
			)
			SELECT NEW.license_number,
				NEW.dba_name,
				NEW.inspection_date
			WHERE NOT EXISTS (
				SELECT 1
				FROM licenses
				WHERE license_number = NEW.license_number
			);

			UPDATE licenses
			SET inspection_date = NEW.inspection_date
			WHERE license_number = NEW.license_number
				AND dba_name = NEW.dba_name
				AND NEW.inspection_date > inspection_date;

			INSERT INTO other_names (license_number, aka_name)
			SELECT license_number,
				dba_name
			FROM licenses
			WHERE license_number = NEW.license_number
				AND dba_name != NEW.dba_name
				AND NEW.inspection_date > inspection_date
				AND dba_name IS NOT NULL
				AND dba_name != ''
				AND NOT EXISTS (
					SELECT 1
					FROM other_names
					WHERE license_number = licenses.license_number
						AND aka_name = licenses.dba_name
				);

			UPDATE licenses
			SET dba_name = NEW.dba_name,
				inspection_date = NEW.inspection_date
			WHERE license_number = NEW.license_number
				AND dba_name != NEW.dba_name
				AND NEW.inspection_date > inspection_date;

			INSERT INTO other_names (license_number, aka_name)
			SELECT NEW.license_number,
				NEW.dba_name
			FROM licenses
			WHERE license_number = NEW.license_number
				AND dba_name != NEW.dba_name
				AND NEW.inspection_date < inspection_date
				AND NEW.dba_name IS NOT NULL
				AND NEW.dba_name != ''
				AND NOT EXISTS (
					SELECT 1
					FROM other_names
					WHERE license_number = NEW.license_number
						AND aka_name = NEW.dba_name
				);

		END;
		"""
	)

def load():

	inspections = pd.read_csv(r'Data/Step 2 - Tables/inspections_table.csv')
	violations = pd.read_csv(r'Data/Step 2 - Tables/violations_table.csv')
	licenses = pd.read_csv(r'Data/Step 2 - Tables/licenses_table.csv')
	other_names = pd.read_csv(r'Data/Step 2 - Tables/other_names_table.csv')

	database = r'Data/ChicagoFoodInspection.db'

	if os.path.exists(database):
		os.remove(database)

	conn = sqlite3.connect(database)
	cursor = conn.cursor()
	setup_database(cursor)

	inspections.to_sql(
		"inspections", conn, if_exists="append", index=False
	)

	violations.to_sql(
		"violations", conn, if_exists="append", index=False
	)

	other_names.drop_duplicates(subset=["license_number", "aka_name"]).to_sql(
		"other_names", conn, if_exists="append", index=False
	)

	licenses.to_sql(
		"license_view", conn, if_exists="append", index=False
	)

	conn.commit()
	conn.close()

load()