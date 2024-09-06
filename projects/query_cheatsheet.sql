-- All examples are for a simple star warehouse architecture

-- Grouping Sets example
SELECT
    s.StationId,
    t.truckType,
    SUM(f.wastecollected) AS TotalWaste
FROM
    FactTrips f
INNER JOIN
    DimStation s ON f.StationId = s.StationId
INNER JOIN
	DimTruck t ON f.TruckId = t.TruckId
GROUP BY GROUPING SETS (
    (s.StationId, t.TruckType),
    s.StationId,
    t.TruckType,
    ()
)
ORDER BY
    s.Stationid,
    t.Trucktype;

-- Roll up Sets example
SELECT
    d.Year,
    s.City,
    s.stationid,
    SUM(f.wastecollected) AS TotalWaste
FROM
    FactTrips f
JOIN
    DimDate d ON f.Dateid = d.Dateid
JOIN
    DimStation s ON f.StationId = s.StationId
GROUP BY ROLLUP (d.Year, s.City, s.stationid)
ORDER BY
    d.Year DESC,
    s.City,
    s.stationid;

-- Cube grouping example
SELECT
    d.Year,
    s.City,
    s.stationid,
    AVG(f.wastecollected) AS AverageWaste
FROM
    FactTrips f
INNER JOIN
    DimDate d ON f.Dateid = d.Dateid
INNER JOIN
    DimStation s ON f.stationid = s.stationid
GROUP BY CUBE (d.Year, s.City, s.stationid);
