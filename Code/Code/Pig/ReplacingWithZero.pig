A = LOAD 'weather.csv' USING PigStorage(',');
B = FOREACH A GENERATE $0, (($2 IS NULL) ? 0 : $2), (($8 IS NULL) ? 0 : $8) , (($14 IS NULL) ? 0 : $14) , (($17 IS NULL) ? 0 : $17), $21;
STORE B INTO 'output_weather_replace_zero';