#Part 1 Stream Simulation

import random
import time
import datetime

#These are the libraries we will use to simulate the data stream by using random time and also a timestamp for the messages.

#The full scripted conversation will be stored in a list of dictionaries, where each dictionary represents a message with a timestamp and content.

#Personalities:
#Priya: Project Lead / Proactive Communicator
#Ben: Developer / Avoidant & Overwhelmed
#Sara: Detail-Oriented QA / Passive-Aggressive

scripted_conversation = [
    #Phase 1: Team is aligned and working well
    #User: name of user x, text: what they are sending on their channel

    {"user": "Priya", "text": "Morning team! Quick check-in on the Automated Reporting Dashboard. How are we looking for the demo on Friday?"},
    {"user": "Ben", "text": "Morning! The data pipeline is mostly in place. Things are moving along."},
    {"user": "Sara", "text": "Great. Once the pipeline is stable, I can start writing the end-to-end tests."},
    {"user": "Priya", "text": "Perfect. @Ben, any blockers on your end?"},
    {"user": "Ben", "text": "Should be fine. Just need to finalize the API schema."},
    {"user": "Sara", "text": "Okay. I'll need that schema for my test stubs. Let me know when it's ready."},
    {"user": "Priya", "text": "Excellent. Sounds like we're in a good spot. Let's keep up the momentum!"},

    #Phase 2: A little friction starts to appear

    {"user": "Priya", "text": "Just circling back on that API schema, @Ben. Any update?"},
    {"user": "Ben", "text": "Making progress on it. Ran into a small snag with the database connection but I think it's sorted."},
    {"user": "Sara", "text": "A 'snag'? Is the data source not what we agreed on in the spec?"},
    {"user": "Ben", "text": "It's the same source, just a configuration issue. It's fine."},
    {"user": "Priya", "text": "Okay, keep us posted. We need to lock that down soon for Sara to get started."},
    {"user": "Sara", "text": "Noted. It would be helpful to have documentation for these 'snags' in the future."},
    {"user": "Ben", "text": "Yeah, I'll get to it when I can."},
    {"user": "Priya", "text": "Let's focus on the schema for now. Can we get a firm ETA, @Ben?"},
    {"user": "Sara", "text": "Yes, an ETA would be great. My test plan depends on it."},

    #Phase 3: Conversation becomes more tense

    {"user": "Ben", "text": "I'm a bit swamped right now, but I'm aiming for EOD tomorrow."},
    {"user": "Priya", "text": "Tomorrow EOD is too late. That leaves Sara with no time before the Friday demo."},
    {"user": "Sara", "text": "Actually, I thought the schema was supposed to be ready yesterday. Per my last message, my work is blocked."},
    {"user": "Ben", "text": "The project plan didn't account for the authentication library being deprecated."},
    {"user": "Priya", "text": "This is the first I'm hearing about a deprecated library. Why wasn't this flagged earlier?"},
    {"user": "Ben", "text": "I thought I mentioned it. I've been trying to work around it."},
    {"user": "Sara", "text": "Must be nice to just 'work around' the spec. My tests have to match the spec exactly."},
    {"user": "Priya", "text": "Okay, this isn't productive. Ben, we need that schema. What has to happen to get it done in the next 3 hours?"},
    {"user": "Ben", "text": "I guess I can drop everything else and just focus on that."},

    #Phase 4: Conversation escalates further and drift is very evident

    {"user": "Sara", "text": "Fine. I'll just be waiting here, unable to do my job."},
    {"user": "Priya", "text": "Sara, let's keep it constructive. Ben, please confirm you're working on it now."},
    {"user": "Ben", "text": "Yes. I am working on it."},
    {"user": "Priya", "text": "Thank you. Let's try to get back on track, everyone."},
    {"user": "Sara", "text": "Whatever. I'll believe it when I see the pull request."},
    {"user": "Ben", "text": "You know what, I'm doing my best here. This isn't all on me."}
]

def generate_message_stream():
    #This function will simulate the data stream by yielding messages from the scripted conversation with a random delay.

    #Set time for the clock of the stream and we will set to October 1, 2023, 9:00 AM
    simulation_clock = datetime.datetime(2023, 10, 1, 9, 0, 0)

    for message_data in scripted_conversation:

        #Set a message delay to show real conversation between 10 and 60 seconds
        #Advance clock by the message delay
        message_delay = random.uniform(10, 60)
        simulation_clock += datetime.timedelta(seconds=message_delay)


        #This will define the event which shows a timestamp, user, and text of the message
        event = {
            "timestamp": simulation_clock.isoformat(),
            "user": message_data["user"],
            "text": message_data["text"]
        }

        #Yield the event to the main loop for a real conversation feel
        yield event

        #Use time.sleep() to simulate a delay in the stream
        time.sleep(random.uniform(0.5, 1.5))