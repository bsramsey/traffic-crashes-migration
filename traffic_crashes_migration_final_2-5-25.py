#!/usr/bin/env python
# coding: utf-8

# # traffic crashes migration

# ## add fields

# In[44]:


import arcpy
import pandas as pd

# Define the workspace where your geodatabase and feature class reside
workspace = r"C:\Users\bramsey\traffic_crashes_migration_copy.gdb"
arcpy.env.workspace = workspace

# Define the input table and field details
in_table = "traffic_crashes_migration_copy"
field_name = "LOCATION_FLAG"
field_alias = "Location Flag"

arcpy.management.AddField(
    in_table="traffic_crashes_migration_copy",
    field_name="LOCATION_FLAG",
    field_type="TEXT",
    field_precision=None,
    field_scale=None,
    field_length=None,
    field_alias="Location Flag",
    field_is_nullable="NULLABLE",
    field_is_required="NON_REQUIRED",
    field_domain=""
)

# Print a success message using an f-string
print(f"Field '{field_name}' with alias '{field_alias}' created in table '{in_table}'.")


# ## change field names

# In[45]:


# List of fields to update (old field name, new field name, new alias for DAY, HOUR, and TYPE fields)
fields_to_update = [
    ("DAY", "DAY_OF_WEEK", "Day of Week"),
    ("HOUR", "HOUR_OF_DAY", "Hour of Day"),
    ("TYPE", "CRASH_SEVERITY", "Crash Severity")
]

# Loop through each field and update its name and alias
for old_field, new_field, new_alias in fields_to_update:
    arcpy.management.AlterField(
        in_table=feature_class,
        field=old_field,
        new_field_name=new_field,
        new_field_alias=new_alias
    )
    
    # Print success message
    print(f"Field '{old_field}' renamed to '{new_field}' with alias '{new_alias}' in table '{feature_class}'.")


# ## create domains

# In[46]:


# Define a list of domains to create
domains_to_create = [
    {"domain_name": "PRIVATE_PROPERTY", "domain_description": "Crashes on private property"},
    {"domain_name": "LOCATION", "domain_description": "Location of vehicle"},
    {"domain_name": "ROAD_DESCRIPTION", "domain_description": "Location on roadway"},
    {"domain_name": "DISTANCE_UNITS", "domain_description": "Distance units"},
    {"domain_name": "OFFSET_DIRECTION", "domain_description": "Offset cardinal direction"},
    {"domain_name": "FIRST_HARMFUL_EVENT", "domain_description": "The first event involved in the crash"},
    {"domain_name": "APPROACH_OVERTAKE", "domain_description": "Type of overtaking turn"},
    {"domain_name": "DIRECTION_OF_TRAVEL", "domain_description": "Cardinal direction"},
    {"domain_name": "MOVEMENT", "domain_description": "Vehicle movement"},
    {"domain_name": "VEHICLE_TYPE", "domain_description": "Vehicle type"},
    {"domain_name": "UNIT_TYPE", "domain_description": "Vehicle type including nonmotorists"},
    {"domain_name": "VIOLATION", "domain_description": "Cited vehicle violation"},
    {"domain_name": "NON_MOTORIST_ACTION", "domain_description": "Non-motorist action"},
    {"domain_name": "NON_MOTORIST_FACTOR", "domain_description": "Non-motorist factor"},
    {"domain_name": "REVIEW_STATUS", "domain_description": "Review status"},
    {"domain_name": "LOCATION_FLAG", "domain_description": "Crash locations to flag for further review"}
]

# Loop through the domains and create them
for domain in domains_to_create:
    arcpy.management.CreateDomain(
        in_workspace=workspace,
        domain_name=domain["domain_name"],
        domain_description=domain["domain_description"],
        field_type="TEXT",
        domain_type="CODED",
        split_policy="DEFAULT",
        merge_policy="DEFAULT"
    )
    print(f"{domain['domain_name']} Domain created. Description: {domain['domain_description']}") # Added domain description to f-string 


# ## add coded values to domains

# In[47]:


# Define a function to add coded values to a domain
def add_coded_values_to_domain(workspace, domain_name, coded_values):
    try:
        for value in coded_values:
            arcpy.management.AddCodedValueToDomain(
                in_workspace=workspace,
                domain_name=domain_name,
                code=value["code"],
                code_description=value["description"]
            )
        print(f"Coded values added to {domain_name} domain successfully.")
    except Exception as e:
        print(f"Error adding values to {domain_name}: {str(e)}")

# Define coded values for Private Property domain
coded_values_private_property = [
    {"code": "True", "description": "True"},
    {"code": "False", "description": "False"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for Location domain
coded_values_location = [
    {"code": "01. On Roadway", "description": "01. On Roadway"},
    {"code": "02. Ran Off Left Side", "description": "02. Ran Off Left Side"},
    {"code": "03. Ran Off Right Side", "description": "03. Ran Off Right Side"},
    {"code": "04. Ran Off T Intersection", "description": "04. Ran Off T Intersection"},
    {"code": "05. Vehicle Crossed Center Median Into Opposing Lanes", "description": "05. Vehicle Crossed Center Median Into Opposing Lanes"},
    {"code": "06. On Private Property", "description": "06. On Private Property"},
    {"code": "07. Center Median/Island", "description": "07. Center Median/Island"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for Road Description domain
coded_values_road_description = [
    {"code": "01. At Intersection", "description": "01. At Intersection"},
    {"code": "02. Driveway Access Related", "description": "02. Driveway Access Related"},
    {"code": "03. Intersection Related", "description": "03. Intersection Related"},
    {"code": "04. Non-Intersection", "description": "04. Non-Intersection"},
    {"code": "05. Crossover-related", "description": "05. Crossover-related"},
    {"code": "06. Roundabout", "description": "06. Roundabout"},
    {"code": "08. Parking Lot", "description": "08. Parking Lot"},
    {"code": "09. Ramp", "description": "09. Ramp"},
    {"code": "10. Ramp-related", "description": "10. Ramp-related"},
    {"code": "11. Alley-Related", "description": "11. Alley-Related"},
    {"code": "12. Shared-Use Path or Trail", "description": "12. Shared-Use Path or Trail"},
    {"code": "13. Auxiliary Lane", "description": "13. Auxiliary Lane"},
    {"code": "14. Mid-Block Crosswalk", "description": "14. Mid-Block Crosswalk"},
    {"code": "15. Express Managed HOV Lane", "description": "15. Express Managed HOV Lane"},
    {"code": "16. Railroad Crossing Related", "description": "16. Railroad Crossing Related"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for Distance Units domain
coded_values_distance_units = [
    {"code": "Miles", "description": "Miles"},
    {"code": "Feet", "description": "Feet"},
    {"code": "At The Intersection", "description": "At The Intersection"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for Offset Direction domain
coded_values_offset_direction = [
    {"code": "North", "description": "North"},
    {"code": "South", "description": "South"},
    {"code": "East", "description": "East"},
    {"code": "West", "description": "West"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for First Harmful Event domain
coded_values_first_harmful_event = [
    {"code": "01. Overturning/Rollover", "description": "01. Overturning/Rollover"},
    {"code": "02. Other Non-Collision", "description": "02. Other Non-Collision"},
    {"code": "03. School Age To/From School", "description": "03. School Age To/From School"},
    {"code": "05. Pedestrian", "description": "05. Pedestrian"},
    {"code": "06. Front to Front", "description": "06. Front to Front"},
    {"code": "07. Front to Rear", "description": "07. Front to Rear"},
    {"code": "08. Front to Side", "description": "08. Front to Side"},
    {"code": "09. Rear to Side", "description": "09. Rear to Side"},
    {"code": "10. Rear to Rear", "description": "10. Rear to Rear"},
    {"code": "11. Side to Side-Same Direction", "description": "11. Side to Side-Same Direction"},
    {"code": "12. Side to Side-Opposite Direction", "description": "12. Side to Side-Opposite Direction"},
    {"code": "13. Parked Motor Vehicle", "description": "13. Parked Motor Vehicle"},
    {"code": "15. Bicycle/Motorized Bicycle", "description": "15. Bicycle/Motorized Bicycle"},
    {"code": "17. Domestic Animal", "description": "17. Domestic Animal"},
    {"code": "18. Wild Animal", "description": "18. Wild Animal"},
    {"code": "19. Light Pole/Utility Pole", "description": "19. Light Pole/Utility Pole"},
    {"code": "20. Traffic Signal Pole", "description": "20. Traffic Signal Pole"},
    {"code": "21. Sign", "description": "21. Sign"},
    {"code": "23. Cable Rail", "description": "23. Cable Rail"},
    {"code": "24. Concrete Highway Barrier", "description": "24. Concrete Highway Barrier"},
    {"code": "26. Vehicle Debris or Cargo", "description": "26. Vehicle Debris or Cargo"},
    {"code": "27. Culvert or Headwall", "description": "27. Culvert or Headwall"},
    {"code": "28. Embankment", "description": "28. Embankment"},
    {"code": "29. Curb", "description": "29. Curb"},
    {"code": "30. Delineator/Milepost", "description": "30. Delineator/Milepost"},
    {"code": "31. Fence", "description": "31. Fence"},
    {"code": "32. Tree", "description": "32. Tree"},
    {"code": "33. Large Rocks or Boulder", "description": "33. Large Rocks or Boulder"},
    {"code": "34. Railroad Crossing Equipment", "description": "34. Railroad Crossing Equipment"},
    {"code": "35. Barricade", "description": "35. Barricade"},
    {"code": "36. Wall or Building", "description": "36. Wall or Building"},
    {"code": "37. Crash Cushion/Traffic Barrel", "description": "37. Crash Cushion/Traffic Barrel"},
    {"code": "38. Mailbox", "description": "38. Mailbox"},
    {"code": "39. Other Fixed Object (Describe in Narrative)", "description": "39. Other Fixed Object (Describe in Narrative)"},
    {"code": "40. Other Non-Fixed Object (Describe in Narrative)", "description": "40. Other Non-Fixed Object (Describe in Narrative)"},
    {"code": "41. Guardrail Face", "description": "41. Guardrail Face"},
    {"code": "42. Guardrail End", "description": "42. Guardrail End"},
    {"code": "43. Ditch", "description": "43. Ditch"},
    {"code": "44. Immersion, Full or Partial", "description": "44. Immersion, Full or Partial"},
    {"code": "45. Fell from Motor Vehicle", "description": "45. Fell from Motor Vehicle"},
    {"code": "46. Ground", "description": "46. Ground"},
    {"code": "47. Electrical/Utility Box", "description": "47. Electrical/Utility Box"},
    {"code": "48. Overhead Structure (Bridge)", "description": "48. Overhead Structure (Bridge)"},
    {"code": "49. Overhead Structure (Not Bridge)", "description": "49. Overhead Structure (Not Bridge)"},
    {"code": "50. Bridge Structure (Not Overhead)", "description": "50. Bridge Structure (Not Overhead)"},
    {"code": "NA", "description": "NA"}
]
    
# Define coded values for Approach/Overtake domain
coded_values_approach_overtake = [
    {"code": "01. Approach Turn", "description": "01. Approach Turn"},
    {"code": "02. Overtaking Turn", "description": "02. Overtaking Turn"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for Direction of Travel domain
coded_values_direction_of_travel = [
    {"code": "01. North", "description": "01. North"},
    {"code": "02. Northeast", "description": "02. Northeast"},
    {"code": "03. East", "description": "03. East"},
    {"code": "04. Southeast", "description": "04. Southeast"},
    {"code": "05. South", "description": "05. South"},
    {"code": "06. Southwest", "description": "06. Southwest"},
    {"code": "07. West", "description": "07. West"},
    {"code": "08. Northwest", "description": "08. Northwest"},
    {"code": "NA", "description": "NA"}
]


# Define coded values for Movement domain
coded_values_movement = [
    {"code": "01. Going Straight", "description": "01. Going Straight"},
    {"code": "02. Slowing", "description": "02. Slowing"},
    {"code": "03. Stopped in Traffic", "description": "03. Stopped in Traffic"},
    {"code": "04. Making Right Turn", "description": "04. Making Right Turn"},
    {"code": "05. Making Left Turn", "description": "05. Making Left Turn"},
    {"code": "06. Making U-Turn", "description": "06. Making U-Turn"},
    {"code": "07. Passing", "description": "07. Passing"},
    {"code": "08. Backing", "description": "08. Backing"},
    {"code": "09. Entering Leaving Parked Position", "description": "09. Entering Leaving Parked Position"},
    {"code": "10. Parked", "description": "10. Parked"},
    {"code": "11. Changing Lanes", "description": "11. Changing Lanes"},
    {"code": "12. Swerve Avoidance", "description": "12. Swerve Avoidance"},
    {"code": "13. Weaving", "description": "13. Weaving"},
    {"code": "14. Out of Control", "description": "14. Out of Control"},
    {"code": "15. Traveled Wrong Way", "description": "15. Traveled Wrong Way"},
    {"code": "16. Other (Describe in Narrative)", "description": "16. Other (Describe in Narrative)"},
    {"code": "17. Entering Traffic Way Merge", "description": "17. Entering Traffic Way Merge"},
    {"code": "18. Negotiating a Curve", "description": "18. Negotiating a Curve"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for Vehicle Type domain
coded_values_vehicle_type = [
    {"code": "01. Medium Heavy Trucks GVWR/GCWR between 10,001 and 16,000", "description": "01. Medium Heavy Trucks GVWR/GCWR between 10,001 and 16,000"},
    {"code": "02. School Bus (all school buses)", "description": "02. School Bus (all school buses)"},
    {"code": "03. Non-School Bus (9 occupants or more including driver) in commerce", "description": "03. Non-School Bus (9 occupants or more including driver) in commerce"},
    {"code": "04. Transit Bus", "description": "04. Transit Bus"},
    {"code": "05. Passenger Car Passenger Van", "description": "05. Passenger Car Passenger Van"},
    {"code": "07. Pickup Truck Utility Van", "description": "07. Pickup Truck Utility Van"},
    {"code": "09. SUV", "description": "09. SUV"},
    {"code": "11. Motor Home", "description": "11. Motor Home"},
    {"code": "12. Motorcycle", "description": "12. Motorcycle"},
    {"code": "15. Farm Equipment", "description": "15. Farm Equipment"},
    {"code": "16. Unknown (Hit and Run Only)", "description": "16. Unknown (Hit and Run Only)"},
    {"code": "17. Light Rail", "description": "17. Light Rail"},
    {"code": "18. Other Vehicle Type (Describe in Narrative)", "description": "18. Other Vehicle Type (Describe in Narrative)"},
    {"code": "20. Working Vehicle Equipment", "description": "20. Working Vehicle Equipment"},
    {"code": "21. Heavy Train", "description": "21. Heavy Train"},
    {"code": "23. Off Highway Vehicle/ATV", "description": "23. Off Highway Vehicle/ATV"},
    {"code": "24. Snowmobile", "description": "24. Snowmobile"},
    {"code": "25. Low Speed Vehicle", "description": "25. Low Speed Vehicle"},
    {"code": "27. Medium/Heavy Trucks GVWR/GCWR 16,001 or over", "description": "27. Medium/Heavy Trucks GVWR/GCWR 16,001 or over"},
    {"code": "28. Autocycle", "description": "28. Autocycle"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for Unit Type domain
coded_values_unit_type = [
    {"code": "Bicycle", "description": "Bicycle"},
    {"code": "Driver", "description": "Driver"},
    {"code": "NA", "description": "NA"},
    {"code": "Non Motorist", "description": "Non Motorist"},
    {"code": "Non-Contact Vehicle", "description": "Non-Contact Vehicle"},
    {"code": "Non-Vehicle", "description": "Non-Vehicle"},
    {"code": "Parked", "description": "Parked"},
    {"code": "Pedestrian", "description": "Pedestrian"},
    {"code": "Vehicle", "description": "Vehicle"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for Violation domain
coded_values_violation = [
    {"code": "00. No Contributing Action", "description": "00. No Contributing Action"},
    {"code": "02. Impeded Traffic", "description": "02. Impeded Traffic"},
    {"code": "03. Failed to Yield ROW", "description": "03. Failed to Yield ROW"},
    {"code": "04. Disregard Stop Sign", "description": "04. Disregard Stop Sign"},
    {"code": "05. Failed to Stop at Signal", "description": "05. Failed to Stop at Signal"},
    {"code": "06. Disregarded Other Device/Sign/Markings", "description": "06. Disregarded Other Device/Sign/Markings"},
    {"code": "07. Improper Turn", "description": "07. Improper Turn"},
    {"code": "08. Turned from Wrong Lane or Position", "description": "08. Turned from Wrong Lane or Position"},
    {"code": "10. Lane Violation", "description": "10. Lane Violation"},
    {"code": "11. Improper Passing on Left", "description": "11. Improper Passing on Left"},
    {"code": "12. Improper Passing on Right", "description": "12. Improper Passing on Right"},
    {"code": "13. Followed Too Closely", "description": "13. Followed Too Closely"},
    {"code": "14. Improper Backing", "description": "14. Improper Backing"},
    {"code": "15. Signaling Violation", "description": "15. Signaling Violation"},
    {"code": "16. Reckless Driving", "description": "16. Reckless Driving"},
    {"code": "17. Careless Driving", "description": "17. Careless Driving"},
    {"code": "18. Speeding", "description": "18. Speeding"},
    {"code": "19. Too Fast for Conditions", "description": "19. Too Fast for Conditions"},
    {"code": "20. Racing", "description": "20. Racing"},
    {"code": "21. Over-Correcting Over-Steering", "description": "21. Over-Correcting Over-Steering"},
    {"code": "22. Lacking Required Chains", "description": "22. Lacking Required Chains"},
    {"code": "23. Other Contributing Action (Describe in Narrative)", "description": "23. Other Contributing Action (Describe in Narrative)"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for Non-Motorist Action domain
coded_values_non_motorist_action = [
    {"code": "00. No Contributing Action", "description": "00. No Contributing Action"},
    {"code": "01. Failure to Obey Traffic Signs, Signals, or Officer", "description": "01. Failure to Obey Traffic Signs, Signals, or Officer"},
    {"code": "02. Cross Enter at Intersection", "description": "02. Cross Enter at Intersection"},
    {"code": "03. Cross Enter NOT at Intersection", "description": "03. Cross Enter NOT at Intersection"},
    {"code": "06. Soliciting Rides", "description": "06. Soliciting Rides"},
    {"code": "07. Traveling Along Roadway With Traffic (In or Adjacent to Travel Lane)", "description": "07. Traveling Along Roadway With Traffic (In or Adjacent to Travel Lane)"},
    {"code": "08. Traveling Along Roadway Against Traffic (In or Adjacent to Travel Lane)", "description": "08. Traveling Along Roadway Against Traffic (In or Adjacent to Travel Lane)"},
    {"code": "09. Entering/Exiting Parked Standing Vehicle", "description": "09. Entering/Exiting Parked Standing Vehicle"},
    {"code": "10. Disabled Vehicle Related (Working on, Pushing, Leaving/Approaching)", "description": "10. Disabled Vehicle Related (Working on, Pushing, Leaving/Approaching)"},
    {"code": "12. Other (Describe in Narrative)", "description": "12. Other (Describe in Narrative)"},
    {"code": "13. Traveling on Sidewalk With Traffic", "description": "13. Traveling on Sidewalk With Traffic"},
    {"code": "14. Traveling on Sidewalk Against Traffic", "description": "14. Traveling on Sidewalk Against Traffic"},
    {"code": "15. Working in Trafficway (Incident Response)", "description": "15. Working in Trafficway (Incident Response)"},
    {"code": "16. Working in Trafficway (Maintenance Activities)", "description": "16. Working in Trafficway (Maintenance Activities)"},
    {"code": "17. Improper Passing", "description": "17. Improper Passing"},
    {"code": "18. Failure to Yield Right-Of-Way", "description": "18. Failure to Yield Right-Of-Way"},
    {"code": "19. Improper Turn/Merge", "description": "19. Improper Turn/Merge"},
    {"code": "20. Dart/Dash", "description": "20. Dart/Dash"},
    {"code": "21. In Roadway Improperly (Standing, Lying, Working, Playing)", "description": "21. In Roadway Improperly (Standing, Lying, Working, Playing)"},
    {"code": "22. Panhandling", "description": "22. Panhandling"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for Non-Motorist Factor domain
coded_values_non_motorist_factor = [
    {"code": "00. No Apparent Contributing Factor", "description": "00. No Apparent Contributing Factor"},
    {"code": "01. Not Visible (Dark Clothing, No Lighting, etc.)", "description": "01. Not Visible (Dark Clothing, No Lighting, etc.)"},
    {"code": "02. Emotionally Upset", "description": "02. Emotionally Upset"},
    {"code": "03. Asleep or Fatigued", "description": "03. Asleep or Fatigued"},
    {"code": "04. Illness/Medical", "description": "04. Illness/Medical"},
    {"code": "05. Inexperience", "description": "05. Inexperience"},
    {"code": "06. Aggressive", "description": "06. Aggressive"},
    {"code": "07. Unfamiliar With Area", "description": "07. Unfamiliar With Area"},
    {"code": "08. Evading Law Enforcement Officer", "description": "08. Evading Law Enforcement Officer"},
    {"code": "09. Physical Disability", "description": "09. Physical Disability"},
    {"code": "10. Distracted/Passenger", "description": "10. Distracted/Passenger"},
    {"code": "11. Distracted/Headphones", "description": "11. Distracted/Headphones"},
    {"code": "12. Distracted/Cell Phone", "description": "12. Distracted/Cell Phone"},
    {"code": "13. Distracted - Manipulating Electronic Device", "description": "13. Distracted - Manipulating Electronic Device"},
    {"code": "14. Distracted/Other i.e., Food, Objects, Pet, etc.", "description": "14. Distracted/Other i.e., Food, Objects, Pet, etc."},
    {"code": "15. Looked/Did Not See", "description": "15. Looked/Did Not See"},
    {"code": "16. Age/Ability", "description": "16. Age/Ability"},
    {"code": "17. Sun Glare", "description": "17. Sun Glare"},
    {"code": "18. Under the Influence of Alcohol or Drugs", "description": "18. Under the Influence of Alcohol or Drugs"},
    {"code": "19. Other Factor (Describe in Narrative)", "description": "19. Other Factor (Describe in Narrative)"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for Review Status domain
coded_values_review_status = [
    {"code": "Need to review", "description": "Need to review"},
    {"code": "Review complete", "description": "Review complete"},
    {"code": "NA", "description": "NA"}
]

# Define coded values for Location Flag domain
coded_values_location_flag = [
    {"code": "I-25", "description": "I-25"},
    {"code": "US 36", "description": "US 36"},
    {"code": "NA", "description": "NA"}
]

# Loop through the dictionary and add coded values to each domain
domains_with_coded_values = {
    "PRIVATE_PROPERTY": coded_values_private_property,
    "LOCATION": coded_values_location,
    "ROAD_DESCRIPTION": coded_values_road_description,
    "DISTANCE_UNITS": coded_values_distance_units,
    "OFFSET_DIRECTION": coded_values_offset_direction,
    "FIRST_HARMFUL_EVENT": coded_values_first_harmful_event,
    "APPROACH_OVERTAKE": coded_values_approach_overtake,
    "DIRECTION_OF_TRAVEL": coded_values_direction_of_travel,
    "MOVEMENT": coded_values_movement,
    "VEHICLE_TYPE": coded_values_vehicle_type,
    "UNIT_TYPE": coded_values_unit_type,
    "VIOLATION": coded_values_violation,
    "NON_MOTORIST_ACTION": coded_values_non_motorist_action,
    "NON_MOTORIST_FACTOR": coded_values_non_motorist_factor,
    "REVIEW_STATUS": coded_values_review_status,
    "LOCATION_FLAG": coded_values_location_flag
}

# Running the function from the top of the cell
for domain_name, coded_values in domains_with_coded_values.items():
    add_coded_values_to_domain(workspace, domain_name, coded_values)


# ## assign domains to fields

# In[48]:


# Define the list of fields and their corresponding domains with updated field names
fields_and_domains = [
    {"field": "PRIVATE_PROPERTY", "domain": "PRIVATE_PROPERTY"},
    {"field": "LOCATION", "domain": "LOCATION"},
    {"field": "ROAD_DESCRIPTION", "domain": "ROAD_DESCRIPTION"},
    {"field": "DISTANCE_UNITS", "domain": "DISTANCE_UNITS"},
    {"field": "TU1_DIRECTION_OF_TRAVEL", "domain": "DIRECTION_OF_TRAVEL"},
    {"field": "TU2_DIRECTION_OF_TRAVEL", "domain": "DIRECTION_OF_TRAVEL"},
    {"field": "FIRST_HARMFUL_EVENT", "domain": "FIRST_HARMFUL_EVENT"},
    {"field": "APPROACH_OVERTAKE", "domain": "APPROACH_OVERTAKE"},
    {"field": "DIRECTION", "domain": "OFFSET_DIRECTION"},
    {"field": "TU1_MOVEMENT", "domain": "MOVEMENT"},  # Movement TU1
    {"field": "TU2_MOVEMENT", "domain": "MOVEMENT"},  # Movement TU2
    {"field": "TU1_VEHICLE_TYPE", "domain": "VEHICLE_TYPE"},  # Vehicle Type TU1
    {"field": "TU2_VEHICLE_TYPE", "domain": "VEHICLE_TYPE"},  # Vehicle Type TU2
    {"field": "TU1_UNIT_TYPE", "domain": "UNIT_TYPE"},  # Unit Type TU1
    {"field": "TU2_UNIT_TYPE", "domain": "UNIT_TYPE"},  # Unit Type TU2
    {"field": "TU1_NON_MOTORIST_ACTION", "domain": "NON_MOTORIST_ACTION"},  # Non-Motorist Action TU1
    {"field": "TU2_NON_MOTORIST_ACTION", "domain": "NON_MOTORIST_ACTION"},  # Non-Motorist Action TU2
    {"field": "TU1_NON_MOTORIST_FACTOR", "domain": "NON_MOTORIST_FACTOR"},  # Non-Motorist Factor TU1
    {"field": "TU2_NON_MOTORIST_FACTOR", "domain": "NON_MOTORIST_FACTOR"},  # Non-Motorist Factor TU2
    {"field": "VIOLATION", "domain": "VIOLATION"},
    {"field": "REVIEW_STATUS", "domain": "REVIEW_STATUS"},
    {"field": "LOCATION_FLAG", "domain": "LOCATION_FLAG"}
]

# Loop through each field and assign the domain
for field_domain in fields_and_domains:
    field_name = field_domain["field"]
    domain_name = field_domain["domain"]
    
    # Assign the domain to the field
    arcpy.management.AssignDomainToField(
        in_table= "traffic_crashes_migration_copy",
        field_name=field_name,  # Correct parameter name
        domain_name=domain_name
    )
    
    print(f"Domain '{domain_name}' assigned to field '{field_name}' in the feature class.")


# ## update existing data 

# In[49]:


import arcpy
import pandas as pd
import re

# Parameters
excel_file = r"C:\Users\bramsey\Downloads\Copy of Broomfield Crash Data 2021-2023 Final (14).xlsx"
feature_class = r"C:\Users\bramsey\traffic_crashes_migration_copy.gdb\traffic_crashes_migration_copy"
match_field_excel = "ACCIDENT_NUMBER"
match_field_fc = "ACCIDENT_NUMBER"

# List of fields to include in the update cursor
update_fields = [
    "NARRATIVE", "PRIVATE_PROPERTY", "LOCATION", "ROAD_DESCRIPTION", 
    "MAIN_STREET", "INTERSECTION_DISTANCE", "DISTANCE_UNITS", "CROSS_STREET", "COMMON_NAME", 
    "INTERSECTION_GIS_ID", "INTERSECTION_NAME", "LATITUDE", "LONGITUDE", "FIRST_HARMFUL_EVENT", 
    "SECOND_HARMFUL_EVENT", "APPROACH_OVERTAKE", "TU1_DIRECTION_OF_TRAVEL", "TU1_MOVEMENT", "TU2_DIRECTION_OF_TRAVEL", 
    "TU2_MOVEMENT", "TU1_VEHICLE_TYPE", "TU1_UNIT_TYPE", "TU2_VEHICLE_TYPE", "TU2_UNIT_TYPE", 
    "TU1_VIOLATION", "TU1_NON_MOTORIST_MOVEMENT", "TU2_NON_MOTORIST_MOVEMENT", 
    "TU1_NON_MOTORIST_ACTION", "TU2_NON_MOTORIST_ACTION", "TU1_NON_MOTORIST_FACTOR", 
    "TU2_NON_MOTORIST_FACTOR", "REVIEW_STATUS"
]

# Function to convert field values to the correct data type
def convert_value_new(value, field_name, feature_class):
    if pd.isna(value) or value == '':
        return None
    
    field_type = next((field.type for field in arcpy.ListFields(feature_class) if field.name == field_name), None)

    if field_type is not None: 
        if field_type == "String":
            return str(value)
        elif field_type == "Integer":
            return int(value) 
        elif field_type == "Double":
            return float(value) 
        elif field_type == "Date":
            return pd.to_datetime(value, errors='coerce')
        return value
    else:  
        return None

# Read Excel file into a DataFrame from the second sheet (sheet_index=1)
df = pd.read_excel(excel_file, sheet_name=1, header=0, dtype=str)

# Ensure matching field exists in Excel (directly use the match_field_excel without applying standardization)
# Check if the match_field_excel is in the columns of the Excel DataFrame
if match_field_excel not in df.columns:
    print(f"Column '{match_field_excel}' not found in the DataFrame.")
else:
    # Drop rows with missing accident numbers
    df = df.dropna(subset=[match_field_excel])

# Limit to the first 10 rows of the DataFrame
df = df.head(10)

# Get list of fields in the feature class (use field name, not alias)
fc_fields = [field.name for field in arcpy.ListFields(feature_class) if field.editable]

# Ensure match field exists in feature class
if match_field_fc not in fc_fields:
    raise KeyError(f"'{match_field_fc}' field not found in the feature class.")

# Filter update_fields to only include valid fields (based on field names, not aliases)
valid_update_fields = [field for field in update_fields if field in fc_fields and field in df.columns]

# Field Mapping Adjustment: Print actual field names from Excel and feature class
print("Field Mapping Between Excel and Feature Class:")

# Iterate over valid update fields and print the actual matching field names
for field in valid_update_fields:
    # Get the field aliases or names from both Excel and feature class
    excel_field_name = field
    feature_class_field_name = field

    # Print the mapping between Excel field and feature class field
    print(f"Excel Column: '{excel_field_name}' → Feature Class Field: '{feature_class_field_name}'")

# Compare and print missing fields
missing_fields = [field for field in update_fields if field not in valid_update_fields]
if missing_fields:
    print("Missing fields in feature class or Excel DataFrame:")
    for field in missing_fields:
        print(f"- {field}")
else:
    print("All fields are present and mapped correctly.")

# Create a search cursor to find matching accident numbers in the feature class
fc_data = {}
with arcpy.da.SearchCursor(feature_class, [match_field_fc]) as search_cursor:
    for row in search_cursor:
        accident_number = str(row[0])  # No space stripping here
        fc_data[accident_number] = row[0]

# Iterate through Excel accident numbers and update matching feature class records
updated_rows = []
updated_count = 0  # Counter for updated records
for excel_index, excel_row in df.iterrows():
    accident_number = excel_row[match_field_excel]  # No space stripping here

    if accident_number in fc_data:
        # Using UpdateCursor to update records for each match found
        with arcpy.da.UpdateCursor(feature_class, [match_field_fc] + valid_update_fields) as cursor:
            for row in cursor:
                if str(row[0]) == accident_number:  # Exact match without space stripping
                    updated_values = [convert_value_new(excel_row[field], field, feature_class) if field in excel_row else None for field in valid_update_fields]
                    row[1:] = updated_values
                    try: 
                        cursor.updateRow(row)
                        updated_rows.append((row[0], updated_values))
                        updated_count += 1  # Increment updated count
                        print(f"Updated accident number: {accident_number}")  # Print the updated accident number
                    except Exception as e:
                        print(f"Failed to update row for accident_number {accident_number}: {e}")

# Print the first updated row and the total number of updated records
if updated_rows:
    print("First updated row:")
    print(updated_rows[0])

print(f"Total number of updated records: {updated_count}")


# In[ ]:




