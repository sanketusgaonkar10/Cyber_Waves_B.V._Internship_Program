WITH voyage_data AS (
    SELECT 
        id,
        event,
        DATEADD(day, dateStamp, '1899-12-30') + timeStamp AS event_utc,
        voyage_From,
        lat,
        lon,
        imo_num,
        voyage_Id
    FROM voyages
    WHERE imo_num = '9434761' AND voyage_Id = '6' AND allocatedVoyageId IS NULL
),
event_pairs AS (
    SELECT 
        a.id AS start_id,
        a.event AS start_event,
        a.event_utc AS start_utc,
        a.voyage_From AS start_port,
        a.lat AS start_lat,
        a.lon AS start_lon,
        b.id AS end_id,
        b.event AS end_event,
        b.event_utc AS end_utc,
        b.voyage_From AS end_port,
        b.lat AS end_lat,
        b.lon AS end_lon
    FROM voyage_data a
    JOIN voyage_data b ON a.id < b.id
    WHERE a.event = 'SOSP' AND b.event = 'EOSP'
    ORDER BY a.id
)
SELECT 
    start_id,
    start_event,
    start_utc,
    start_port,
    end_id,
    end_event,
    end_utc,
    end_port,
    DATEDIFF(second, start_utc, end_utc) / 3600.0 AS sailing_time,
    6371 * 2 * ASIN(SQRT(POWER(SIN((RADIANS(end_lat - start_lat)) / 2), 2) + 
    COS(RADIANS(start_lat)) * COS(RADIANS(end_lat)) * 
    POWER(SIN((RADIANS(end_lon - start_lon)) / 2), 2))) AS distance_travelled -- Distance in kilometers
FROM event_pairs;