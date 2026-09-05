import pandas as pd 
import sqlalchemy

from dotenv import load_dotenv
import os


load_dotenv(".env/.env")

DB_KEY = os.getenv("DB_KEY")
USERNAME = os.getenv("USERNAME")          
DATABASE = os.getenv("DATABASE") 

assert DB_KEY is not None and USERNAME is not None and DATABASE is not None

ENGINE = sqlalchemy.create_engine(f"postgresql+psycopg://{USERNAME}:{DB_KEY}@localhost:5432/{DATABASE}")



def clean_arcgis(engine):


    arcgis_query = """

    SELECT * FROM ( SELECT a.*, (
        (CASE WHEN a.child_population           is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.working_population         is NULL then 1 ELSE 0 END) + 
        (CASE WHEN a.senior_population          is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.total_crime_index          is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.daytime_population         is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.daytime_workers            is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.daytime_population_density is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.median_disposable_income   is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.average_disposable_income  is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.avg_college_tuition        is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.avg_value_of_stocks        is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.median_home_value          is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.average_home_value         is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.median_net_worth           is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.average_net_worth          is NULL then 1 ELSE 0 END) +
        (CASE WHEN a.total_consumer_spending    is NULL then 1 ELSE 0 END)) 
    AS null_entries FROM parsed_data.arcgis_variables AS a) AS x WHERE null_entries < 4
    """

    arcgis = pd.read_sql(arcgis_query, engine, index_col=["zcta", "state"])


    arcgis = arcgis.fillna(arcgis.median(skipna=True))




def clean_acs(engine):
    acs_query = """

    SELECT * FROM (SELECT acs.*,(
        CASE WHEN acs.total_population             IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.median_household_income      IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.per_capita_income             IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.poverty_population            IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.bachelors_degree              IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.employed_population           IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.housing_units                 IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.median_gross_rent             IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.public_transport_users        IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.total_commuters               IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.aggregate_commute_time        IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.no_vehicle_households         IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.renter_occupied               IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.owner_occupied                IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.total_occupied                IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.food_stamp_households         IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.total_households              IS NULL THEN 1 ELSE 0 END +
        CASE WHEN acs.owner_no_vehicle_households   IS NULL THEN 1 ELSE 0 END
            ) AS null_entries
        FROM parsed_data.acs_variables AS acs) AS x WHERE null_entries < 4;

    """

    acs = pd.read_sql(acs_query, engine, index_col=["zcta", "state"])
    acs = acs.mask(acs<0, pd.NA)
    acs = acs.drop(columns=["index_num", "null_entries"], errors="ignore")
    acs = acs.fillna(acs.median(skipna=True))

def clean_dhc(engine):
    dhc_query = """

        SELECT * FROM (SELECT dhc.*,(
            CASE WHEN dhc.total_population_2020         IS NULL THEN 1 ELSE 0 END +
            CASE WHEN dhc.household_population          IS NULL THEN 1 ELSE 0 END +
            CASE WHEN dhc.urban_population              IS NULL THEN 1 ELSE 0 END +
            CASE WHEN dhc.rural_population              IS NULL THEN 1 ELSE 0 END +
            CASE WHEN dhc.median_male_age               IS NULL THEN 1 ELSE 0 END +
            CASE WHEN dhc.median_female_age             IS NULL THEN 1 ELSE 0 END +
            CASE WHEN dhc.male_population               IS NULL THEN 1 ELSE 0 END +
            CASE WHEN dhc.vacant_housing_units          IS NULL THEN 1 ELSE 0 END +
            CASE WHEN dhc.vacant_housing_for_rent       IS NULL THEN 1 ELSE 0 END
                ) AS null_entries
            FROM parsed_data.dhc_variables AS dhc) AS x WHERE null_entries < 4;

    """

    dhc = pd.read_sql(dhc_query, engine, index_col=["zcta", "state"])
    dhc = dhc.drop(columns=["index_num", "null_entries"], errors="ignore")
    dhc = dhc.mask(dhc<0 , pd.NA)
    dhc = dhc.fillna(dhc.median(skipna=True))


def clean_cbp_naics(engine):
    cbp_naics_query = """
        SELECT * FROM parsed_data.cbp_naics_variables AS cbp WHERE cbp.estab_total IS NOT NULL
        AND cbp.emp_total   IS NOT NULL;
    """

    cbp_naics = pd.read_sql(cbp_naics_query, engine, index_col=["zcta", "state"])
    cbp_naics = cbp_naics.drop(columns=["index_num", "null_entries"], errors="ignore")
    cbp_naics = cbp_naics.mask((cbp_naics < 0) | (cbp_naics == pd.NA), 0)

    cbp_naics = cbp_naics.fillna(0)

    print(cbp_naics.shape)



def join_tables(*args):
    ...














if __name__ == "__main__":
    arcgis_clean = clean_arcgis(ENGINE)
    acs_clean = clean_acs(ENGINE)
    dhc_clean = clean_dhc(ENGINE)
    cbp_naics_clean = clean_cbp_naics(ENGINE)

    joined = pd.concat([arcgis_clean, acs_clean, cbp_naics_clean, dhc_clean], axis=1, join="inner")
    joined.to_sql(name="joined", schema="cleaned_data", if_exists="replace", con=engine)







