A = LOAD 'game.csv' USING PigStorage(',');
B = DISTINCT A;
STORE B INTO 'output_remove_duplicate';