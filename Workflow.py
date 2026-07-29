# @begin FoodInspectionPipeline

# @begin OpenRefineCleaning
# @in Data/Step_0_pre_Food-Inspections-20251023
# @out Data/Step_1_After_Open_Refine_Data.csv
# @end OpenRefineCleaning

# @begin SplitCSVFiles
# @in Data/Step_1_After_Open_Refine_Data.csv
# @out Data/Step_2_Tables/inspections.csv
# @out Data/Step_2_Tables/violations.csv
# @out Data/Step_2_Tables/licenses.csv
# @out Data/Step_2_Tables/other_names.csv
# @end SplitCSVFiles

# @begin StoreDatabase
# @in Data/Step_2_Tables/inspections.csv
# @in Data/Step_2_Tables/violations.csv
# @in Data/Step_2_Tables/licenses.csv
# @in Data/Step_2_Tables/other_names.csv
# @out Data/ChicagoFoodInspection.db
# @end StoreDatabase

# @begin CompareData
# @in Data/Step_0_pre_Food-Inspections-20251023
# @in Data/Step_1_After_Open_Refine_Data.csv
# @out Data/openrefine_changes_summary.txt
# @end CompareData

# @end FoodInspectionPipeline