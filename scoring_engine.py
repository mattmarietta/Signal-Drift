#Part 2 Drift Scoring Engine

from biometric import get_hrv

#Make a dictionary of signals that could be defined as drift in a conversation

#Hard coding common phrases that could include emotional drift
#Downside of this approach is that it can be taken out of context, but it is a good starting point for the scoring engine
#A lot of these signals are specific to the prompt, so they may not be applicable to other conversations. Real-time AI would be much better suited for this task. 
DRIFT_SIGNALS = {
    "a 'snag'?": (0.62, "Sarcastic questioning; challenges a colleague's statement."),
    "just circling back": (0.61, "Passive-aggressive follow-up; implies lateness."),
    "per my last message": (0.7, "Passive-aggressive; implies 'you didn't read my message'."),
    "noted.": (0.53, "Dismissive acknowledgement."),
    "making progress": (0.3, "Ambiguous update, not very informative."),
    "maybe": (0.4, "Hesitant language, indicates uncertainty."),
    "i thought": (0.72, "Potential contradiction or blame-shifting."),
    "actually": (0.54, "Corrective/Contradictory statement."),
    "it's fine": (0.66, "Passive-aggressive tone."),
    "whatever": (0.84, "Dismissive tone, can be rude to colleagues."),
    "i guess": (0.4, "Reluctance or lack of buy-in to the conversation."),
    "swamped": (0.5, "Avoiding responsibility in some cases."),
    "must be nice": (0.93, "High passive-aggressive tone detected."),
    "you know what": (0.85, "Defensive and confrontational."),
    "sure, whatever": (0.90, "Dismissive and confrontational."),
}

#Base score message is the foundation for the scoring criteria, simply checks if any of the signals are in the text
#If a signal is found, it returns the score and description of the drift signal

def base_score_message(text):
    "Score a basic message based on the drift signals defined above"
    #Lower the text to make matching case-insensitive
    text_lower = text.lower()

    for signal, (score, description) in DRIFT_SIGNALS.items():
        if signal in text_lower:
            #Need to return the signal score and description
            return score, description
            
    #If no drift signals are found then we will return a score of 0.0
    return 0.0, "No drift detected"


#Context score message is the main function that is used to score the message based on context and using the foundation as a baseline
#It will take the current message and the last score to determine the drift score
#Finally, it check for a sudden shift of the users intent

def context_score_message(current_text, last_score, synthetic_hrv=None):
    "Use the current text and last score to determine drift score by "
    #Get base score using base_score_message
    current_score, reason = base_score_message(current_text)

    #If the last score and current score are greater than 0.5, check for a pattern of negative behavior
    if current_score > 0.5 and last_score > 0.5:
        #Boost the score for repeated negative pattern and make sure it doesn't exceed 1.0
        current_score = min(1.0, current_score + 0.1)
        reason += " (Pattern of Negative Behavior from this user)"


    #Check for a sudden shift in the user's intent
    #If last score was low and current score is high, it indicates a sudden shift
    #Use a flag to indicate this by comparing both scores
    is_sudden_shift = last_score < 0.2 and current_score > 0.7
    if is_sudden_shift:
        #For simplicity, if there is a sudden shift, we will set the score to 1.0
        current_score = 1.0
        reason += " (Sudden Negative Shift)"


    #Bonus Challenge Factor in biometric signal
    #If the message is already negative and the synthetic HRV is low, this is a stronger signal of drift,
    if current_score > 0.4 and synthetic_hrv < 40:
        current_score = min(1.0, current_score + 0.1)
        reason += " (Affected by Low HRV)"


    #Return final score and reason
    return round(current_score, 2), reason


'''
"Test cases for the scoring engine, uncomment for testing purposes"
if __name__ == '__main__':
    print("\nTesting for Ben")
    score, reason = context_score_message("I'm a bit swamped right now",  0.0)
    print(f"Message: 'I'm a bit swamped right now' -> Score: {score}, Reason: {reason}")

    print("\nTesting for Sara")
    score, reason = context_score_message("Must be nice to just work around the spec.", 0.0)
    print(f"Message: 'Must be nice...' -> Score: {score}, Reason: {reason}")
    
    print("Testing for a Sudden Shift")
    score, reason = context_score_message("You know what, this isn't working.", 0.0)
    print(f"Message: 'You know what...' -> Score: {score}, Reason: {reason}")
'''