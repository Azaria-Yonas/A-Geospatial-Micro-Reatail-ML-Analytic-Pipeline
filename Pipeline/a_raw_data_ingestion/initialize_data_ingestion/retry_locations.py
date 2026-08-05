import asyncio

from a_raw_data_ingestion.initialize_data_ingestion.initialize_locations import initialize_table, padd
from psql.raw_data.locations import get_errors, update_zcta





if __name__ == "__main__":
    zcta, state = zip(*get_errors())
    zcta = padd(zcta)
    asyncio.run(initialize_table(zcta, state, update_zcta))

