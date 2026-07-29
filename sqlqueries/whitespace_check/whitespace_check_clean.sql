SELECT COUNT(*)
  FROM inspections
  WHERE [DBA_NAME] LIKE '% '
	OR [DBA_NAME] LIKE ' %'
	OR [DBA_NAME] LIKE '%  %';