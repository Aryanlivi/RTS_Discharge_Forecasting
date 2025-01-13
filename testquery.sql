SELECT * FROM public.forecast_galchi_to_siurenitar;
SELECT * FROM public.forecast_budhi_at_khari_to_siurenitar;
SELECT * FROM public.forecast_siurenitar_data;

SELECT * FROM public.forecast_budhi_at_khari_to_siurenitar 
WHERE datetime='2025-01-13 13:35:00'
LIMIT 1;


 SELECT dateTime, discharge FROM public.forecast_budhi_at_khari_to_siurenitar
                WHERE dateTime <= '2025-01-13 13:35:00'
                ORDER BY dateTime DESC
                LIMIT 1

SELECT dateTime FROM forecast_siurenitar_table ORDER BY dateTime ASC