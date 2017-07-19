A = LOAD 'weather.csv' USING PigStorage(',');
B = FOREACH A GENERATE FLATTEN(STRSPLIT($0,'-')), $2, $8, $14, $17, $21;
f1 = FILTER B BY $2 IS NOT NULL;
g1 = GROUP f1 by month; (Group by month)
m1 = FOREACH g1 {
    sum = SUM(f1.$2);
    count = COUNT(f1);
    generate group as id, sum/count as mean, sum as sum, count as count;
};
f2 = FILTER B BY $8 IS NOT NULL;
g2 = GROUP f2 by month;
m2 = FOREACH g2 {
    sum = SUM(f2.$8);
    count = COUNT(f2);
    generate group as id, sum/count as mean, sum as sum, count as count;
};
f3 = FILTER B BY $14 IS NOT NULL;
g3 = GROUP f3 by month;
m3 = FOREACH g3 {
    sum = SUM(f3.$14);
    count = COUNT(f3);
    generate group as id, sum/count as mean, sum as sum, count as count;
};
f4 = FILTER B BY $17 IS NOT NULL;
g4 = GROUP f4 by month;
m4 = FOREACH g4 {
    sum = SUM(f4.$14);
    count = COUNT(f4);
    generate group as id, sum/count as mean, sum as sum, count as count;
};
C = FOREACH A GENERATE $0, (($2 IS NULL) ? 0 : m1), (($8 IS NULL) ? 0 : m2) , (($14 IS NULL) ? 0 : m3) , (($17 IS NULL) ? 0 : m4), $21;
STORE C INTO 'output_weather_replace_avg';
