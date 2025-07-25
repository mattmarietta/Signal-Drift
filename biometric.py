#Bonus challenge


import random
#We will use this function to generate HRV data and use the base score to generate a synthetic HRV reading
#Main drift calculation will be performed in scoring_engine.py, this will be defined in main.py

def get_hrv(base_drift_score):
    """
    Generates a synthetic Heart Rate Variability (HRV) reading in ms.
    A healthy, coherent state has high HRV. Stress or drift lowers it.
    """
    #Healthy baseline HRV in ms, adjust based on context
    baseline_hrv = 65
    
    #The more linguistic drift we detect then our HRV should drop
    #We will multiply by a factor to make the effect noticeable 
    drift_impact = base_drift_score * 30 
    
    #Because this is a simulation, we are going to add some random noise to our reading
    random_noise = random.uniform(-5, 5)
    
    #Calculate the final HRV by subtracting the drift impact and adding random noise
    final_hrv = baseline_hrv - drift_impact + random_noise
    
    #Return it as a clean integer value for the engine
    return int(final_hrv)
